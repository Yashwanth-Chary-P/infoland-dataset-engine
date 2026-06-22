from __future__ import annotations

import json
import logging
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import geopandas as gpd
import pandas as pd
from shapely.geometry import mapping

ROOT_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT_DIR / "data"
RAW_DIR = DATA_DIR / "raw"
LEGACY_INPUT_DIR = DATA_DIR / "geojson"
CLEANED_DIR = DATA_DIR / "cleaned"
MASTER_DIR = DATA_DIR / "master"
POI_DIR = DATA_DIR / "poi"
REPORTS_DIR = DATA_DIR / "reports"
INSPECTION_REPORT_DIR = REPORTS_DIR / "inspection"
VALIDATION_REPORT_DIR = REPORTS_DIR / "validation"
STATISTICS_REPORT_DIR = REPORTS_DIR / "statistics"
CONFIG_DIR = ROOT_DIR / "config"

REQUIRED_CLEAN_COLUMNS = [
    "source_id",
    "source_region",
    "feature_category",
    "building",
    "amenity",
    "landuse",
    "centroid_lat",
    "centroid_lon",
    "area_sq_m",
    "area_sq_ft",
    "area_sq_yd",
    "perimeter_m",
    "bbox",
    "geometry",
]


@dataclass(frozen=True)
class RegionSource:
    region: str
    path: Path


def configure_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s - %(message)s",
    )


def ensure_directories() -> None:
    for path in [
        RAW_DIR,
        CLEANED_DIR,
        MASTER_DIR,
        POI_DIR,
        INSPECTION_REPORT_DIR,
        VALIDATION_REPORT_DIR,
        STATISTICS_REPORT_DIR,
    ]:
        path.mkdir(parents=True, exist_ok=True)


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")


def normalize_region_name(path: Path) -> str:
    return path.stem.lower().replace("_clean", "")


def sync_raw_inputs() -> None:
    """Populate data/raw from the current source folder when raw is empty."""
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    if any(RAW_DIR.glob("*.geojson")):
        return
    if not LEGACY_INPUT_DIR.exists():
        return
    for path in LEGACY_INPUT_DIR.glob("*.geojson"):
        shutil.copy2(path, RAW_DIR / f"{normalize_region_name(path)}.geojson")


def discover_sources() -> list[RegionSource]:
    sync_raw_inputs()
    candidates = list(RAW_DIR.glob("*.geojson"))
    if not candidates:
        candidates = list(LEGACY_INPUT_DIR.glob("*.geojson"))
    return [
        RegionSource(region=normalize_region_name(path), path=path)
        for path in sorted(candidates, key=lambda item: item.stem.lower())
    ]


def read_geojson(path: Path) -> gpd.GeoDataFrame:
    gdf = gpd.read_file(path)
    if gdf.crs is None:
        gdf = gdf.set_crs("EPSG:4326", allow_override=True)
    return gdf


def write_geojson(gdf: gpd.GeoDataFrame, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        path.unlink()
    gdf.to_file(path, driver="GeoJSON")


def source_id_for_row(row: pd.Series, fallback_index: Any) -> str:
    for column in ("source_id", "@id", "id", "osm_id"):
        if column in row and not pd.isna(row[column]) and str(row[column]).strip():
            return str(row[column])
    return f"generated-index/{fallback_index}"


def value_counts(gdf: gpd.GeoDataFrame, column: str) -> dict[str, int]:
    if column not in gdf.columns:
        return {}
    values = gdf[column].fillna("").astype(str)
    values = values[values != ""]
    counts = values.value_counts().sort_index()
    return {str(key): int(value) for key, value in counts.items()}


def geometry_type_counts(gdf: gpd.GeoDataFrame) -> dict[str, int]:
    if gdf.empty:
        return {}
    counts = gdf.geometry.geom_type.fillna("null").value_counts().sort_index()
    return {str(key): int(value) for key, value in counts.items()}


def coordinate_bounds(gdf: gpd.GeoDataFrame) -> dict[str, float | None]:
    valid = gdf[gdf.geometry.notna() & ~gdf.geometry.is_empty]
    if valid.empty:
        return {"min_lon": None, "min_lat": None, "max_lon": None, "max_lat": None}
    min_lon, min_lat, max_lon, max_lat = valid.total_bounds
    return {
        "min_lon": float(min_lon),
        "min_lat": float(min_lat),
        "max_lon": float(max_lon),
        "max_lat": float(max_lat),
    }


def bbox_dict(geometry: Any) -> dict[str, float | None]:
    if geometry is None or geometry.is_empty:
        return {"min_lon": None, "min_lat": None, "max_lon": None, "max_lat": None}
    min_lon, min_lat, max_lon, max_lat = geometry.bounds
    return {
        "min_lon": float(min_lon),
        "min_lat": float(min_lat),
        "max_lon": float(max_lon),
        "max_lat": float(max_lat),
    }


def clean_text(value: Any) -> str:
    if value is None or pd.isna(value):
        return ""
    text = str(value).strip()
    return "" if text.lower() in {"nan", "none", "null"} else text


def geometry_json(geometry: Any) -> dict[str, Any]:
    return mapping(geometry) if geometry is not None and not geometry.is_empty else {}


def clean_for_json(value: Any) -> Any:
    if isinstance(value, dict):
        return {key: clean_for_json(item) for key, item in value.items()}
    if isinstance(value, list):
        return [clean_for_json(item) for item in value]
    if pd.isna(value):
        return None
    if hasattr(value, "item"):
        return value.item()
    return value
