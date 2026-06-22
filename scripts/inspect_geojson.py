from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

import geopandas as gpd

from geo_utils import (
    REPORTS_DIR,
    configure_logging,
    coordinate_bounds,
    discover_geojson_files,
    ensure_output_dirs,
    geometry_type_counts,
    normalize_region_name,
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
        "building_type_counts": value_counts(gdf, "building"),
        "amenity_counts": value_counts(gdf, "amenity"),
        "landuse_counts": value_counts(gdf, "landuse"),
        "coordinate_bounds": coordinate_bounds(gdf),
    }


def inspect_file(path: Path) -> dict[str, Any]:
    region = normalize_region_name(path)
    LOGGER.info("Inspecting %s", path.name)
    report = inspect_gdf(read_geojson(path), region)
    write_json(REPORTS_DIR / f"{region}_inspection.json", report)
    return report


def main() -> None:
    configure_logging()
    ensure_output_dirs()
    for path in discover_geojson_files():
        inspect_file(path)


if __name__ == "__main__":
    main()
