from __future__ import annotations

from typing import Any

import geopandas as gpd
import pandas as pd

from .common import (
    CONFIG_DIR,
    MASTER_DIR,
    clean_for_json,
    geometry_json,
    load_json,
    source_id_for_row,
    write_json,
)

PROPERTY_CATEGORIES = {"property_candidate", "residential", "apartments", "commercial"}


def _prefix_for_region(region: str) -> str:
    config = load_json(CONFIG_DIR / "region_config.json")
    return config["regions"].get(region, {}).get("property_id_prefix", f"PROP-{region[:3].upper()}")


def _master_record(row: Any, idx: Any, property_id: str) -> dict[str, Any]:
    return clean_for_json(
        {
            "property_id": property_id,
            "source_id": source_id_for_row(row, idx),
            "source_region": row.get("source_region", ""),
            "feature_category": row.get("feature_category", ""),
            "building": row.get("building", ""),
            "centroid_lat": row.get("centroid_lat"),
            "centroid_lon": row.get("centroid_lon"),
            "area_sq_m": row.get("area_sq_m"),
            "area_sq_ft": row.get("area_sq_ft"),
            "area_sq_yd": row.get("area_sq_yd"),
            "perimeter_m": row.get("perimeter_m"),
            "bbox": row.get("bbox", {}),
            "geometry": geometry_json(row.geometry),
        }
    )


def create_master_dataset(enriched_by_region: dict[str, gpd.GeoDataFrame]) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    candidates: list[dict[str, Any]] = []

    for region, gdf in sorted(enriched_by_region.items()):
        property_gdf = gdf[
            gdf.geometry.geom_type.isin(["Polygon", "MultiPolygon"])
            & gdf["feature_category"].isin(PROPERTY_CATEGORIES)
        ].copy()
        prefix = _prefix_for_region(region)
        for number, (idx, row) in enumerate(property_gdf.iterrows(), start=1):
            property_id = f"{prefix}-{number:06d}"
            record = _master_record(row, idx, property_id)
            records.append(record)
            candidates.append(record)

    write_json(MASTER_DIR / "master_properties.json", records)
    write_json(MASTER_DIR / "property_candidates.json", candidates)

    csv_rows = [{key: value for key, value in record.items() if key != "geometry"} for record in records]
    pd.DataFrame(csv_rows).to_csv(MASTER_DIR / "master_properties.csv", index=False)
    return records
