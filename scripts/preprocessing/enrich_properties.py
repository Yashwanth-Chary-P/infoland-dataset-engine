from __future__ import annotations

from typing import Any

import geopandas as gpd

from .common import CONFIG_DIR, bbox_dict, load_json

SQ_FT_PER_SQ_M = 10.76391041671
SQ_YD_PER_SQ_M = 1.1959900463


def enrich_properties(gdf: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    config = load_json(CONFIG_DIR / "region_config.json")
    projected = gdf.to_crs(config["projected_crs"])
    enriched = gdf.copy()

    centroids = projected.geometry.centroid
    centroids_wgs84 = gpd.GeoSeries(centroids, crs=config["projected_crs"]).to_crs("EPSG:4326")
    enriched["centroid_lon"] = centroids_wgs84.x.round(8)
    enriched["centroid_lat"] = centroids_wgs84.y.round(8)
    enriched["area_sq_m"] = projected.geometry.area.round(2)
    enriched["area_sq_ft"] = (projected.geometry.area * SQ_FT_PER_SQ_M).round(2)
    enriched["area_sq_yd"] = (projected.geometry.area * SQ_YD_PER_SQ_M).round(2)
    enriched["perimeter_m"] = projected.geometry.length.round(2)
    enriched["bbox"] = enriched.geometry.apply(bbox_dict)
    return enriched


def enrichment_report(gdf: gpd.GeoDataFrame, region: str) -> dict[str, Any]:
    return {
        "region": region,
        "total_features_enriched": int(len(gdf)),
        "area_sq_m_non_null": int(gdf["area_sq_m"].notna().sum()),
        "perimeter_m_non_null": int(gdf["perimeter_m"].notna().sum()),
    }
