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
    value_counts,
    write_json,
)

LOGGER = logging.getLogger(__name__)

BUILDING_CATEGORY_MAP = {
    "house": "residential",
    "residential": "residential",
    "villa": "residential",
    "detached": "residential",
    "semidetached_house": "residential",
    "apartments": "apartments",
    "apartment": "apartments",
    "school": "school",
    "hospital": "hospital",
    "temple": "religious",
    "church": "religious",
    "mosque": "religious",
    "commercial": "commercial",
    "retail": "commercial",
    "shop": "commercial",
    "office": "commercial",
    "government": "government",
    "civic": "government",
    "community_centre": "community",
}

AMENITY_CATEGORY_MAP = {
    "school": "school",
    "college": "school",
    "kindergarten": "school",
    "hospital": "hospital",
    "clinic": "hospital",
    "doctors": "hospital",
    "place_of_worship": "religious",
    "temple": "religious",
    "community_centre": "community",
    "townhall": "government",
    "police": "government",
    "fire_station": "government",
}

LANDUSE_CATEGORY_MAP = {
    "residential": "residential",
    "commercial": "commercial",
    "retail": "commercial",
    "religious": "religious",
    "cemetery": "religious",
    "recreation_ground": "park",
    "grass": "park",
    "park": "park",
    "government": "government",
}

SHOP_CATEGORY = "commercial"
OFFICE_CATEGORY = "commercial"


def _clean_value(value: Any) -> str:
    if value is None:
        return ""
    text = str(value).strip().lower()
    return "" if text in {"nan", "none", "null"} else text


def classify_row(row: Any) -> str:
    amenity = _clean_value(row.get("amenity", ""))
    building = _clean_value(row.get("building", ""))
    landuse = _clean_value(row.get("landuse", ""))
    shop = _clean_value(row.get("shop", ""))
    office = _clean_value(row.get("office", ""))
    leisure = _clean_value(row.get("leisure", ""))

    if amenity in AMENITY_CATEGORY_MAP:
        return AMENITY_CATEGORY_MAP[amenity]
    if building in BUILDING_CATEGORY_MAP:
        return BUILDING_CATEGORY_MAP[building]
    if landuse in LANDUSE_CATEGORY_MAP:
        return LANDUSE_CATEGORY_MAP[landuse]
    if shop:
        return SHOP_CATEGORY
    if office:
        return OFFICE_CATEGORY
    if leisure == "park":
        return "park"
    return "other"


def classify_gdf(gdf: gpd.GeoDataFrame, region: str) -> tuple[gpd.GeoDataFrame, dict[str, Any]]:
    classified = gdf.copy()
    classified["feature_category"] = classified.apply(classify_row, axis=1)
    report = {
        "region": region,
        "total_features": int(len(classified)),
        "feature_categories": value_counts(classified, "feature_category"),
    }
    return classified, report


def classify_file(path: Path) -> tuple[gpd.GeoDataFrame, dict[str, Any]]:
    region = normalize_region_name(path)
    LOGGER.info("Classifying %s", path.name)
    classified, report = classify_gdf(read_geojson(path), region)
    write_json(REPORTS_DIR / f"{region}_classification.json", report)
    return classified, report


def main() -> None:
    configure_logging()
    ensure_output_dirs()
    for path in discover_geojson_files():
        classify_file(path)


if __name__ == "__main__":
    main()
