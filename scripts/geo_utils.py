from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any

import geopandas as gpd
import pandas as pd
from shapely.geometry.base import BaseGeometry

ROOT_DIR = Path(__file__).resolve().parents[1]
INPUT_DIR = ROOT_DIR / "data" / "geojson"
CLEANED_DIR = ROOT_DIR / "data" / "cleaned"
REPORTS_DIR = ROOT_DIR / "data" / "reports"

GLOBAL_LAT_RANGE = (-90.0, 90.0)
GLOBAL_LON_RANGE = (-180.0, 180.0)
HYDERABAD_LAT_RANGE = (17.0, 17.8)
HYDERABAD_LON_RANGE = (78.0, 79.0)

REQUIRED_OUTPUT_COLUMNS = [
    "source_id",
    "source_region",
    "feature_category",
    "building",
    "amenity",
    "landuse",
    "geometry",
]


def configure_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s - %(message)s",
    )


def ensure_output_dirs() -> None:
    CLEANED_DIR.mkdir(parents=True, exist_ok=True)
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)


def discover_geojson_files() -> list[Path]:
    return sorted(INPUT_DIR.glob("*.geojson"), key=lambda path: path.stem.lower())


def normalize_region_name(path: Path) -> str:
    return path.stem.lower()


def read_geojson(path: Path) -> gpd.GeoDataFrame:
    gdf = gpd.read_file(path)
    if gdf.crs is None:
        gdf = gdf.set_crs("EPSG:4326", allow_override=True)
    return gdf


def json_safe(value: Any) -> Any:
    if pd.isna(value):
        return None
    if hasattr(value, "item"):
        return value.item()
    return value


def value_counts(gdf: gpd.GeoDataFrame, column: str) -> dict[str, int]:
    if column not in gdf.columns:
        return {}
    counts = gdf[column].fillna("").astype(str)
    counts = counts[counts != ""].value_counts().sort_index()
    return {str(key): int(value) for key, value in counts.items()}


def geometry_type_counts(gdf: gpd.GeoDataFrame) -> dict[str, int]:
    if gdf.empty:
        return {}
    counts = gdf.geometry.geom_type.fillna("null").value_counts().sort_index()
    return {str(key): int(value) for key, value in counts.items()}


def coordinate_bounds(gdf: gpd.GeoDataFrame) -> dict[str, float | None]:
    valid_geometry = gdf[gdf.geometry.notna() & ~gdf.geometry.is_empty]
    if valid_geometry.empty:
        return {"min_lon": None, "min_lat": None, "max_lon": None, "max_lat": None}
    min_lon, min_lat, max_lon, max_lat = valid_geometry.total_bounds
    return {
        "min_lon": float(min_lon),
        "min_lat": float(min_lat),
        "max_lon": float(max_lon),
        "max_lat": float(max_lat),
    }


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")


def source_id_for_row(row: pd.Series, fallback_index: Any) -> str:
    for column in ("@id", "id", "osm_id", "source_id"):
        if column in row and not pd.isna(row[column]) and str(row[column]).strip():
            return str(row[column])
    return f"generated-index/{fallback_index}"


def prepare_output_columns(gdf: gpd.GeoDataFrame, region: str) -> gpd.GeoDataFrame:
    output = gdf.copy()
    output["source_id"] = [
        source_id_for_row(row, idx) for idx, row in output.drop(columns="geometry").iterrows()
    ]
    output["source_region"] = region
    for column in ("building", "amenity", "landuse", "feature_category"):
        if column not in output.columns:
            output[column] = ""
        output[column] = output[column].fillna("").astype(str)
    return output[REQUIRED_OUTPUT_COLUMNS]


def write_geojson(gdf: gpd.GeoDataFrame, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        path.unlink()
    gdf.to_file(path, driver="GeoJSON")


def get_geometry_bounds(geometry: BaseGeometry | None) -> dict[str, float | None]:
    if geometry is None or geometry.is_empty:
        return {"min_lon": None, "min_lat": None, "max_lon": None, "max_lat": None}
    min_lon, min_lat, max_lon, max_lat = geometry.bounds
    return {
        "min_lon": float(min_lon),
        "min_lat": float(min_lat),
        "max_lon": float(max_lon),
        "max_lat": float(max_lat),
    }


def make_stats_payload(
    region: str,
    before_count: int,
    gdf: gpd.GeoDataFrame,
    invalid_removed: int,
    duplicates_removed: int,
) -> dict[str, Any]:
    return {
        "region": region,
        "total_features_before": int(before_count),
        "total_features_after": int(len(gdf)),
        "invalid_geometries_removed": int(invalid_removed),
        "duplicates_removed": int(duplicates_removed),
        "geometry_types": geometry_type_counts(gdf),
        "feature_categories": value_counts(gdf, "feature_category"),
        "building_types": value_counts(gdf, "building"),
        "amenity_types": value_counts(gdf, "amenity"),
        "coordinate_bounds": coordinate_bounds(gdf),
    }
