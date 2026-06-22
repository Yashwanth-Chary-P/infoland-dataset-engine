from __future__ import annotations

from typing import Any

import geopandas as gpd

from .common import VALIDATION_REPORT_DIR, source_id_for_row, write_json


def deduplicate_gdf(gdf: gpd.GeoDataFrame, region: str) -> tuple[gpd.GeoDataFrame, dict[str, Any]]:
    working = gdf.copy()
    working["_source_id"] = [source_id_for_row(row, idx) for idx, row in working.iterrows()]
    working["_geometry_wkb"] = working.geometry.apply(
        lambda geom: geom.wkb_hex if geom is not None and not geom.is_empty else ""
    )
    working["_centroid_wkb"] = working.geometry.apply(
        lambda geom: geom.centroid.wkb_hex if geom is not None and not geom.is_empty else ""
    )

    by_id = set(working.index[working["_source_id"].duplicated(keep="first")])
    by_geometry = set(
        working.index[working["_geometry_wkb"].ne("") & working["_geometry_wkb"].duplicated(keep="first")]
    )
    by_centroid = set(
        working.index[working["_centroid_wkb"].ne("") & working["_centroid_wkb"].duplicated(keep="first")]
    )
    duplicate_indices = sorted(by_id | by_geometry | by_centroid)
    duplicate_features: list[dict[str, Any]] = []
    for idx in duplicate_indices:
        reasons = []
        if idx in by_id:
            reasons.append("source_id")
        if idx in by_geometry:
            reasons.append("identical_geometry")
        if idx in by_centroid:
            reasons.append("identical_centroid")
        duplicate_features.append(
            {
                "index": int(idx),
                "source_id": str(working.loc[idx, "_source_id"]),
                "duplicate_reasons": reasons,
            }
        )

    deduped = working.drop(index=duplicate_indices).drop(
        columns=["_source_id", "_geometry_wkb", "_centroid_wkb"]
    )
    report = {
        "region": region,
        "total_features_before": int(len(gdf)),
        "total_features_after": int(len(deduped)),
        "duplicates_found": int(len(duplicate_indices)),
        "duplicates_removed": int(len(duplicate_indices)),
        "duplicates_by_source_id": int(len(by_id)),
        "duplicates_by_identical_geometry": int(len(by_geometry)),
        "duplicates_by_identical_centroid": int(len(by_centroid)),
        "duplicate_features": duplicate_features,
    }
    write_json(VALIDATION_REPORT_DIR / f"{region}_deduplication.json", report)
    return deduped, report
