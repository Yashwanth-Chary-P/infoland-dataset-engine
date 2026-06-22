from __future__ import annotations

import logging
from typing import Any

import geopandas as gpd

from .common import (
    INSPECTION_REPORT_DIR,
    coordinate_bounds,
    discover_sources,
    ensure_directories,
    geometry_type_counts,
    read_geojson,
    value_counts,
    write_json,
)

LOGGER = logging.getLogger(__name__)


def inspect_gdf(gdf: gpd.GeoDataFrame, region: str) -> dict[str, Any]:
    return {
        "region": region,
        "total_feature_count": int(len(gdf)),
        "geometry_type_counts": geometry_type_counts(gdf),
        "building_counts": value_counts(gdf, "building"),
        "amenity_counts": value_counts(gdf, "amenity"),
        "landuse_counts": value_counts(gdf, "landuse"),
        "coordinate_bounds": coordinate_bounds(gdf),
    }


def run_inspection() -> dict[str, dict[str, Any]]:
    ensure_directories()
    reports = {}
    for source in discover_sources():
        LOGGER.info("Inspecting %s", source.path.name)
        report = inspect_gdf(read_geojson(source.path), source.region)
        write_json(INSPECTION_REPORT_DIR / f"{source.region}_inspection.json", report)
        reports[source.region] = report
    return reports
