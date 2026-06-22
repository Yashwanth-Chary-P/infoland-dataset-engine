from __future__ import annotations

from typing import Any

import geopandas as gpd

from .common import POI_DIR, clean_for_json, geometry_json, source_id_for_row, write_json

POI_OUTPUTS = {
    "school": "schools.json",
    "hospital": "hospitals.json",
    "park": "parks.json",
    "religious": "temples.json",
    "commercial": "commercial.json",
    "government": "government.json",
}


def _poi_record(row: Any, idx: Any) -> dict[str, Any]:
    return clean_for_json(
        {
            "source_id": source_id_for_row(row, idx),
            "source_region": row.get("source_region", ""),
            "feature_category": row.get("feature_category", ""),
            "building": row.get("building", ""),
            "amenity": row.get("amenity", ""),
            "landuse": row.get("landuse", ""),
            "name": row.get("name", ""),
            "centroid_lat": row.get("centroid_lat"),
            "centroid_lon": row.get("centroid_lon"),
            "geometry": geometry_json(row.geometry),
        }
    )


def extract_pois(enriched_by_region: dict[str, gpd.GeoDataFrame]) -> dict[str, int]:
    grouped = {category: [] for category in POI_OUTPUTS}
    for gdf in enriched_by_region.values():
        for idx, row in gdf.iterrows():
            category = row.get("feature_category", "")
            if category in grouped:
                grouped[category].append(_poi_record(row, idx))

    counts = {}
    for category, filename in POI_OUTPUTS.items():
        records = grouped[category]
        write_json(POI_DIR / filename, records)
        counts[category] = len(records)
    return counts
