from __future__ import annotations

import csv
import hashlib
import json
import logging
import math
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any

ROOT_DIR = Path(__file__).resolve().parents[2]
MASTER_PROPERTIES_PATH = ROOT_DIR / "data" / "master" / "master_properties.json"
GENERATED_DIR = ROOT_DIR / "data" / "generated"
STATISTICS_DIR = ROOT_DIR / "data" / "reports" / "statistics"

LOGGER = logging.getLogger(__name__)
EARTH_RADIUS_KM = 6371.0088
SYNTHESIS_SEED = 20260622

RESIDENTIAL_VERIFICATION_CLASSES = {"residential_plot", "villa", "apartment", "commercial"}
INSTITUTIONAL_CLASSES = {
    "school",
    "hospital",
    "clinic",
    "government",
    "community_center",
    "religious",
    "park",
    "industrial",
    "vacant_land",
}

FEATURE_CATEGORY_CLASS = {
    "apartments": "apartment",
    "commercial": "commercial",
    "school": "school",
    "hospital": "hospital",
    "government": "government",
    "park": "park",
    "religious": "religious",
    "community": "community_center",
    "other": "vacant_land",
}

CANDIDATE_CLASS_TARGETS = {
    "residential_plot": 0.68,
    "villa": 0.10,
    "apartment": 0.02,
    "commercial": 0.04,
    "school": 0.012,
    "hospital": 0.008,
    "clinic": 0.005,
    "government": 0.006,
    "community_center": 0.008,
    "religious": 0.005,
    "park": 0.018,
    "industrial": 0.004,
    "vacant_land": 0.014,
}

POI_TARGET_COUNTS = {
    "school": 18,
    "hospital": 12,
    "park": 25,
    "commercial_hub": 20,
    "government_office": 8,
    "community_center": 12,
}

POI_PROPERTY_CLASSES = {
    "school": ["school"],
    "hospital": ["hospital", "clinic"],
    "park": ["park"],
    "commercial_hub": ["commercial", "industrial"],
    "government_office": ["government"],
    "community_center": ["community_center", "religious"],
}

POI_NAMES = {
    "school": [
        "Green Valley School",
        "Sri Chaitanya School",
        "Oakridge Learning Center",
        "Silver Oaks Academy",
        "Vidya Valley School",
    ],
    "hospital": [
        "City Care Hospital",
        "Apollo Community Clinic",
        "LifeCare Hospital",
        "MedPlus Health Center",
        "Sanjeevani Clinic",
    ],
    "park": [
        "Central Park",
        "Lake View Park",
        "Green Meadows Park",
        "Urban Grove Park",
        "Sunrise Children's Park",
    ],
    "commercial_hub": [
        "Kokapet Market Hub",
        "Mokila Business Center",
        "Shankarpally Retail Plaza",
        "InfoLand Commercial Hub",
        "Metro Trade Center",
    ],
    "government_office": [
        "Municipal Service Center",
        "Revenue Assistance Office",
        "Citizen Services Center",
        "Local Administration Office",
    ],
    "community_center": [
        "Community Hall",
        "Neighborhood Activity Center",
        "Residents Welfare Center",
        "Civic Community Center",
    ],
}


@dataclass(frozen=True)
class PropertyPoint:
    property_id: str
    source_region: str
    lat: float
    lon: float
    area_sq_m: float
    feature_category: str
    building: str


def configure_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s - %(message)s",
    )


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")


def stable_unit(value: str) -> float:
    digest = hashlib.sha256(value.encode("utf-8")).hexdigest()
    return int(digest[:12], 16) / float(0xFFFFFFFFFFFF)


def load_master_properties() -> list[dict[str, Any]]:
    return json.loads(MASTER_PROPERTIES_PATH.read_text(encoding="utf-8"))


def as_points(properties: list[dict[str, Any]]) -> list[PropertyPoint]:
    return [
        PropertyPoint(
            property_id=str(item["property_id"]),
            source_region=str(item["source_region"]),
            lat=float(item["centroid_lat"]),
            lon=float(item["centroid_lon"]),
            area_sq_m=float(item["area_sq_m"]),
            feature_category=str(item.get("feature_category", "")),
            building=str(item.get("building", "")),
        )
        for item in properties
    ]


def quota_counts(total: int, shares: dict[str, float]) -> dict[str, int]:
    raw = {key: total * share for key, share in shares.items()}
    counts = {key: int(math.floor(value)) for key, value in raw.items()}
    remainder = total - sum(counts.values())
    ranked = sorted(raw, key=lambda key: (raw[key] - counts[key], key), reverse=True)
    for key in ranked[:remainder]:
        counts[key] += 1
    return counts


def class_score(point: PropertyPoint, property_class: str) -> float:
    area = point.area_sq_m
    feature = point.feature_category
    building = point.building
    score = stable_unit(f"{point.property_id}:{property_class}") * 0.01

    if property_class == "residential_plot":
        score += 3.0 if 100 <= area <= 500 else 1.0
        score += 1.0 if area < 300 else 0.0
        score += 1.5 if feature in {"property_candidate", "residential"} else 0.0
    elif property_class == "villa":
        score += 4.0 if area >= 500 else 2.0 if area >= 300 else 0.5
        score += 1.0 if building in {"residential", "house", "yes"} else 0.0
    elif property_class == "apartment":
        score += 5.0 if feature == "apartments" or building == "apartments" else 0.0
        score += 1.0 if area >= 300 else 0.5
    elif property_class == "commercial":
        score += 5.0 if feature == "commercial" or building in {"commercial", "retail"} else 0.0
        score += 2.0 if area >= 300 else 0.5
    elif property_class == "industrial":
        score += 4.0 if area >= 800 else 2.0 if area >= 500 else 0.5
    elif property_class == "vacant_land":
        score += 4.0 if area < 120 else 2.0 if area < 250 else 0.5
    elif property_class in {"government", "school", "hospital", "clinic", "park", "community_center", "religious"}:
        score += 5.0 if area >= 1000 else 2.0 if area >= 500 else 1.0 if area >= 300 else 0.0
    return score


def direct_property_class(point: PropertyPoint) -> str | None:
    feature = point.feature_category
    if feature in FEATURE_CATEGORY_CLASS:
        mapped = FEATURE_CATEGORY_CLASS[feature]
        if mapped == "vacant_land":
            return mapped
        return mapped
    if feature == "residential":
        return "villa" if point.area_sq_m >= 500 else "residential_plot"
    return None


def assign_property_classes(points: list[PropertyPoint]) -> dict[str, str]:
    assignments: dict[str, str] = {}
    remaining: list[PropertyPoint] = []

    for point in points:
        direct = direct_property_class(point)
        if direct is not None:
            assignments[point.property_id] = direct
        else:
            remaining.append(point)

    quotas = quota_counts(len(remaining), CANDIDATE_CLASS_TARGETS)
    class_order = [
        "school",
        "hospital",
        "clinic",
        "park",
        "government",
        "community_center",
        "religious",
        "industrial",
        "vacant_land",
        "commercial",
        "apartment",
        "villa",
        "residential_plot",
    ]
    pool = {point.property_id: point for point in remaining}

    for property_class in class_order:
        ranked = sorted(
            pool.values(),
            key=lambda point: (
                class_score(point, property_class),
                point.area_sq_m,
                stable_unit(f"tie:{property_class}:{point.property_id}"),
            ),
            reverse=True,
        )
        for point in ranked[: quotas[property_class]]:
            assignments[point.property_id] = property_class
            pool.pop(point.property_id, None)

    for point in pool.values():
        assignments[point.property_id] = "residential_plot"

    return assignments


def verification_workflow(property_class: str) -> str:
    if property_class in RESIDENTIAL_VERIFICATION_CLASSES:
        return "complete_property_verification"
    return "institutional_property"


def area_segment(area_sq_m: float) -> str:
    if area_sq_m < 100:
        return "small"
    if area_sq_m <= 300:
        return "medium"
    return "large"


def sale_status(property_class: str, property_id: str) -> str:
    if property_class in INSTITUTIONAL_CLASSES:
        return "not_for_sale"
    threshold = 0.15 if property_class == "commercial" else 0.20
    return "for_sale" if stable_unit(f"sale:{property_id}") < threshold else "not_for_sale"


def generate_synthetic_pois(
    points: list[PropertyPoint], classes_by_id: dict[str, str]
) -> list[dict[str, Any]]:
    by_class: dict[str, list[PropertyPoint]] = defaultdict(list)
    for point in points:
        by_class[classes_by_id[point.property_id]].append(point)

    used_property_ids: set[str] = set()
    pois: list[dict[str, Any]] = []
    sequence = 1

    for poi_type, target_count in POI_TARGET_COUNTS.items():
        eligible_classes = POI_PROPERTY_CLASSES[poi_type]
        candidates = [
            point
            for property_class in eligible_classes
            for point in by_class.get(property_class, [])
            if point.property_id not in used_property_ids
        ]
        candidates.sort(
            key=lambda point: (
                point.area_sq_m,
                stable_unit(f"poi-anchor:{poi_type}:{point.property_id}"),
            ),
            reverse=True,
        )
        selected = candidates[:target_count]
        for idx, anchor in enumerate(selected):
            used_property_ids.add(anchor.property_id)
            name_base = POI_NAMES[poi_type][idx % len(POI_NAMES[poi_type])]
            pois.append(
                {
                    "poi_id": f"POI-{sequence:05d}",
                    "poi_type": poi_type,
                    "property_id": anchor.property_id,
                    "name": f"{name_base} {idx // len(POI_NAMES[poi_type]) + 1}"
                    if idx >= len(POI_NAMES[poi_type])
                    else name_base,
                    "lat": round(anchor.lat, 8),
                    "lon": round(anchor.lon, 8),
                    "source_region": anchor.source_region,
                }
            )
            sequence += 1
    return pois


def haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    d_phi = math.radians(lat2 - lat1)
    d_lambda = math.radians(lon2 - lon1)
    a = math.sin(d_phi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(d_lambda / 2) ** 2
    return 2 * EARTH_RADIUS_KM * math.atan2(math.sqrt(a), math.sqrt(1 - a))


def distances_for(point: PropertyPoint, pois: list[dict[str, Any]], poi_types: set[str]) -> list[float]:
    return [
        haversine_km(point.lat, point.lon, float(poi["lat"]), float(poi["lon"]))
        for poi in pois
        if poi["poi_type"] in poi_types and poi["source_region"] == point.source_region
    ]


def nearest_and_count(point: PropertyPoint, pois: list[dict[str, Any]], poi_types: set[str]) -> tuple[int, float | None]:
    distances = distances_for(point, pois, poi_types)
    if not distances:
        return 0, None
    nearby_count = sum(distance <= 1.5 for distance in distances)
    return nearby_count, min(distances)


def distance_points(distance: float | None, bands: list[tuple[float, int]]) -> int:
    if distance is None:
        return 0
    for max_distance, points in bands:
        if distance <= max_distance:
            return points
    return 0


def calculate_location_scores(points: list[PropertyPoint], pois: list[dict[str, Any]]) -> list[dict[str, Any]]:
    records = []
    for point in points:
        school_count, school_distance = nearest_and_count(point, pois, {"school"})
        hospital_count, hospital_distance = nearest_and_count(point, pois, {"hospital"})
        park_count, park_distance = nearest_and_count(point, pois, {"park"})
        commercial_count, commercial_distance = nearest_and_count(point, pois, {"commercial_hub"})
        close_density_count = sum(
            distance <= 0.5
            for poi_types in [{"school"}, {"hospital"}, {"park"}, {"commercial_hub"}]
            for distance in distances_for(point, pois, poi_types)
        )
        score = 0
        score += distance_points(school_distance, [(0.25, 20), (0.50, 14), (1.00, 8), (1.50, 4)])
        score += distance_points(hospital_distance, [(0.30, 20), (0.60, 14), (1.20, 8), (1.50, 4)])
        score += distance_points(park_distance, [(0.20, 15), (0.50, 10), (1.00, 6), (1.50, 3)])
        score += distance_points(commercial_distance, [(0.20, 15), (0.50, 10), (1.00, 6), (1.50, 3)])
        score += min(30, close_density_count * 2)
        records.append(
            {
                "property_id": point.property_id,
                "nearby_school_count": school_count,
                "nearby_hospital_count": hospital_count,
                "nearby_park_count": park_count,
                "nearby_commercial_count": commercial_count,
                "distance_to_nearest_school_km": round(school_distance, 3) if school_distance is not None else None,
                "distance_to_nearest_hospital_km": round(hospital_distance, 3) if hospital_distance is not None else None,
                "distance_to_nearest_park_km": round(park_distance, 3) if park_distance is not None else None,
                "distance_to_nearest_commercial_km": round(commercial_distance, 3) if commercial_distance is not None else None,
                "location_score": int(max(0, min(100, score))),
            }
        )
    return records


def assign_risk_tiers(location_scores: dict[str, int]) -> dict[str, str]:
    property_ids = sorted(location_scores, key=lambda prop_id: (location_scores[prop_id], prop_id), reverse=True)
    quotas = quota_counts(len(property_ids), {"low": 0.60, "medium": 0.30, "high": 0.10})
    tiers = {}
    cursor = 0
    for tier in ["low", "medium", "high"]:
        for property_id in property_ids[cursor : cursor + quotas[tier]]:
            tiers[property_id] = tier
        cursor += quotas[tier]
    return tiers


def generate_property_profiles(
    points: list[PropertyPoint],
    classes: dict[str, str],
    location_records: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    score_by_property = {record["property_id"]: int(record["location_score"]) for record in location_records}
    risk_tiers = assign_risk_tiers(score_by_property)
    profiles = []
    for point in points:
        property_class = classes[point.property_id]
        profiles.append(
            {
                "property_id": point.property_id,
                "property_class": property_class,
                "verification_workflow": verification_workflow(property_class),
                "sale_status": sale_status(property_class, point.property_id),
                "area_segment": area_segment(point.area_sq_m),
                "location_score": score_by_property[point.property_id],
                "future_risk_tier": risk_tiers[point.property_id],
            }
        )
    return profiles


def score_distribution(scores: list[int]) -> dict[str, int]:
    return {
        "low_0_39": sum(score <= 39 for score in scores),
        "medium_40_69": sum(40 <= score <= 69 for score in scores),
        "high_70_100": sum(score >= 70 for score in scores),
    }


def synthesis_stats(
    profiles: list[dict[str, Any]],
    pois: list[dict[str, Any]],
    location_records: list[dict[str, Any]],
) -> dict[str, Any]:
    scores = [int(record["location_score"]) for record in location_records]
    return {
        "total_property_profiles": len(profiles),
        "property_class_distribution": dict(sorted(Counter(profile["property_class"] for profile in profiles).items())),
        "sale_status_distribution": dict(sorted(Counter(profile["sale_status"] for profile in profiles).items())),
        "future_risk_tier_distribution": dict(sorted(Counter(profile["future_risk_tier"] for profile in profiles).items())),
        "poi_counts": dict(sorted(Counter(poi["poi_type"] for poi in pois).items())),
        "average_location_score": round(sum(scores) / len(scores), 2) if scores else 0,
        "location_score_distribution": score_distribution(scores),
    }


def write_csv_debug(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def run_synthesis() -> dict[str, Any]:
    GENERATED_DIR.mkdir(parents=True, exist_ok=True)
    STATISTICS_DIR.mkdir(parents=True, exist_ok=True)
    properties = load_master_properties()
    points = as_points(properties)
    LOGGER.info("Loaded %s master properties", len(points))

    classes = assign_property_classes(points)
    pois = generate_synthetic_pois(points, classes)
    location_records = calculate_location_scores(points, pois)
    profiles = generate_property_profiles(points, classes, location_records)
    stats = synthesis_stats(profiles, pois, location_records)

    write_json(GENERATED_DIR / "property_profiles.json", profiles)
    write_json(GENERATED_DIR / "synthetic_pois.json", pois)
    write_json(GENERATED_DIR / "location_scores.json", location_records)
    write_json(STATISTICS_DIR / "synthesis_stats.json", stats)
    return stats


def main() -> None:
    configure_logging()
    stats = run_synthesis()
    LOGGER.info("Synthesis complete: %s", stats)


if __name__ == "__main__":
    main()
