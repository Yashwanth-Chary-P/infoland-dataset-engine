from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

import geopandas as gpd

from geo_utils import (
    REPORTS_DIR,
    configure_logging,
    discover_geojson_files,
    ensure_output_dirs,
    normalize_region_name,
    read_geojson,
    source_id_for_row,
    write_json,
)

LOGGER = logging.getLogger(__name__)


def _non_empty_source_ids(gdf: gpd.GeoDataFrame) -> list[str]:
    return [source_id_for_row(row, idx) for idx, row in gdf.iterrows()]


def deduplicate_gdf(gdf: gpd.GeoDataFrame, region: str) -> tuple[gpd.GeoDataFrame, dict[str, Any]]:
    working = gdf.copy()
    working["_source_id_for_dedupe"] = _non_empty_source_ids(working)
    working["_geometry_wkb_for_dedupe"] = working.geometry.apply(
        lambda geom: geom.wkb_hex if geom is not None and not geom.is_empty else ""
    )
    working["_centroid_wkb_for_dedupe"] = working.geometry.apply(
        lambda geom: geom.centroid.wkb_hex if geom is not None and not geom.is_empty else ""
    )

    duplicate_by_id = set(
        working.index[
            working["_source_id_for_dedupe"].ne("")
            & working["_source_id_for_dedupe"].duplicated(keep="first")
        ]
    )
    duplicate_by_geometry = set(
        working.index[
            working["_geometry_wkb_for_dedupe"].ne("")
            & working["_geometry_wkb_for_dedupe"].duplicated(keep="first")
        ]
    )
    duplicate_by_centroid = set(
        working.index[
            working["_centroid_wkb_for_dedupe"].ne("")
            & working["_centroid_wkb_for_dedupe"].duplicated(keep="first")
        ]
    )
    duplicate_indices = sorted(duplicate_by_id | duplicate_by_geometry | duplicate_by_centroid)

    duplicate_features: list[dict[str, Any]] = []
    for idx in duplicate_indices:
        row = working.loc[idx]
        reasons = []
        if idx in duplicate_by_id:
            reasons.append("osm_id")
        if idx in duplicate_by_geometry:
            reasons.append("identical_geometry")
        if idx in duplicate_by_centroid:
            reasons.append("identical_centroid")
        duplicate_features.append(
            {
                "index": int(idx),
                "source_id": str(row["_source_id_for_dedupe"]),
                "duplicate_reasons": reasons,
            }
        )

    deduped = working.drop(index=duplicate_indices).drop(
        columns=[
            "_source_id_for_dedupe",
            "_geometry_wkb_for_dedupe",
            "_centroid_wkb_for_dedupe",
        ]
    )
    report = {
        "region": region,
        "total_features_before": int(len(gdf)),
        "total_features_after": int(len(deduped)),
        "duplicates_found": int(len(duplicate_indices)),
        "duplicates_removed": int(len(duplicate_indices)),
        "duplicates_by_osm_id": int(len(duplicate_by_id)),
        "duplicates_by_identical_geometry": int(len(duplicate_by_geometry)),
        "duplicates_by_identical_centroid": int(len(duplicate_by_centroid)),
        "duplicate_features": duplicate_features,
    }
    return deduped, report


def deduplicate_file(path: Path) -> tuple[gpd.GeoDataFrame, dict[str, Any]]:
    region = normalize_region_name(path)
    LOGGER.info("Deduplicating %s", path.name)
    deduped, report = deduplicate_gdf(read_geojson(path), region)
    write_json(REPORTS_DIR / f"{region}_deduplication.json", report)
    return deduped, report


def main() -> None:
    configure_logging()
    ensure_output_dirs()
    for path in discover_geojson_files():
        deduplicate_file(path)


if __name__ == "__main__":
    main()
