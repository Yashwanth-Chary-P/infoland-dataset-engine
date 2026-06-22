from __future__ import annotations

from typing import Any

import geopandas as gpd

from .common import CONFIG_DIR, clean_text, load_json, value_counts


def classify_row(row: Any, rules: dict[str, Any]) -> str:
    amenity = clean_text(row.get("amenity", "")).lower()
    building = clean_text(row.get("building", "")).lower()
    landuse = clean_text(row.get("landuse", "")).lower()
    leisure = clean_text(row.get("leisure", "")).lower()
    shop = clean_text(row.get("shop", ""))
    office = clean_text(row.get("office", ""))

    if amenity in rules["amenity"]:
        return rules["amenity"][amenity]
    if building in rules["building"]:
        return rules["building"][building]
    if landuse in rules["landuse"]:
        return rules["landuse"][landuse]
    if leisure in rules["leisure"]:
        return rules["leisure"][leisure]
    if shop:
        return rules["shop_default"]
    if office:
        return rules["office_default"]
    return rules["unknown"]


def classify_gdf(gdf: gpd.GeoDataFrame, region: str) -> tuple[gpd.GeoDataFrame, dict[str, Any]]:
    rules = load_json(CONFIG_DIR / "classification_rules.json")
    classified = gdf.copy()
    classified["feature_category"] = classified.apply(lambda row: classify_row(row, rules), axis=1)
    report = {
        "region": region,
        "total_features": int(len(classified)),
        "feature_categories": value_counts(classified, "feature_category"),
    }
    return classified, report
