from __future__ import annotations

import hashlib
import json
import logging
import math
import random
from collections import Counter, defaultdict
from datetime import date, timedelta
from pathlib import Path
from typing import Any

ROOT_DIR = Path(__file__).resolve().parents[2]
MASTER_PROPERTIES_PATH = ROOT_DIR / "data" / "master" / "master_properties.json"
PROPERTY_PROFILES_PATH = ROOT_DIR / "data" / "generated" / "property_profiles.json"
SYNTHETIC_POIS_PATH = ROOT_DIR / "data" / "generated" / "synthetic_pois.json"
GENERATED_DIR = ROOT_DIR / "data" / "generated"
DOCUMENTS_DIR = GENERATED_DIR / "documents"
REPORTS_DIR = GENERATED_DIR / "reports"
DOCUMENT_SAMPLES_DIR = REPORTS_DIR / "document_samples"

LOGGER = logging.getLogger(__name__)
BUSINESS_DATASET_SEED = 20260623

DOCUMENT_TYPES: list[dict[str, Any]] = [
    {
        "key": "sale_deed",
        "file": "sale_deeds.json",
        "document_type": "sale_deed",
        "fields": [
            "seller_name",
            "buyer_name",
            "registration_number",
            "registration_date",
            "market_value",
        ],
    },
    {
        "key": "mother_deed",
        "file": "mother_deeds.json",
        "document_type": "mother_deed",
        "fields": [
            "parent_document_number",
            "ownership_chain_length",
            "origin_year",
        ],
    },
    {
        "key": "encumbrance_certificate",
        "file": "encumbrance_certificates.json",
        "document_type": "encumbrance_certificate",
        "fields": [
            "ec_period_from",
            "ec_period_to",
            "encumbrance_count",
            "active_encumbrance",
        ],
    },
    {
        "key": "property_tax_receipt",
        "file": "property_tax_receipts.json",
        "document_type": "property_tax_receipt",
        "fields": [
            "financial_year",
            "tax_amount",
            "paid_amount",
            "pending_amount",
        ],
    },
    {
        "key": "mutation_record",
        "file": "mutation_records.json",
        "document_type": "mutation_record",
        "fields": [
            "mutation_number",
            "mutation_date",
            "reason",
        ],
    },
    {
        "key": "survey_map",
        "file": "survey_maps.json",
        "document_type": "survey_map",
        "fields": [
            "survey_number",
            "plot_area_sqyd",
            "survey_date",
        ],
    },
    {
        "key": "rtc_record",
        "file": "rtc_records.json",
        "document_type": "rtc_record",
        "fields": [
            "survey_number",
            "land_type",
            "cultivation_status",
        ],
    },
    {
        "key": "khata_certificate",
        "file": "khata_certificates.json",
        "document_type": "khata_certificate",
        "fields": [
            "khata_number",
            "owner_name",
        ],
    },
    {
        "key": "khata_extract",
        "file": "khata_extracts.json",
        "document_type": "khata_extract",
        "fields": [
            "khata_number",
            "assessment_value",
        ],
    },
    {
        "key": "building_approval_plan",
        "file": "building_approval_plans.json",
        "document_type": "building_approval_plan",
        "fields": [
            "approval_number",
            "approved_floors",
            "approval_date",
        ],
    },
    {
        "key": "layout_approval",
        "file": "layout_approvals.json",
        "document_type": "layout_approval",
        "fields": [
            "layout_number",
            "approved_by",
            "approval_date",
        ],
    },
    {
        "key": "land_conversion_certificate",
        "file": "land_conversion_certificates.json",
        "document_type": "land_conversion_certificate",
        "fields": [
            "conversion_type",
            "conversion_date",
        ],
    },
    {
        "key": "occupancy_certificate",
        "file": "occupancy_certificates.json",
        "document_type": "occupancy_certificate",
        "fields": [
            "building_type",
            "occupancy_date",
        ],
    },
    {
        "key": "completion_certificate",
        "file": "completion_certificates.json",
        "document_type": "completion_certificate",
        "fields": [
            "completion_date",
            "approved_structure",
        ],
    },
    {
        "key": "noc",
        "file": "nocs.json",
        "document_type": "noc",
        "fields": [
            "issuing_department",
            "valid_until",
        ],
    },
    {
        "key": "identity_proof",
        "file": "identity_proofs.json",
        "document_type": "identity_proof",
        "fields": [
            "owner_id",
            "proof_type",
            "proof_last4",
        ],
    },
    {
        "key": "power_of_attorney",
        "file": "power_of_attorneys.json",
        "document_type": "power_of_attorney",
        "fields": [
            "principal_name",
            "agent_name",
            "valid_until",
        ],
    },
    {
        "key": "court_dispute_record",
        "file": "court_dispute_records.json",
        "document_type": "court_dispute_record",
        "fields": [
            "case_number",
            "court_name",
            "case_type",
            "case_status",
        ],
    },
]

COMMON_DOCUMENT_FIELDS = [
    "document_id",
    "property_id",
    "document_type",
    "status",
    "issue_date",
    "last_updated",
    "issuing_authority",
    "document_number",
    "remarks",
]

INDIVIDUAL_FIRST_NAMES = [
    "Aarav",
    "Aditi",
    "Ananya",
    "Arjun",
    "Deepak",
    "Divya",
    "Harsha",
    "Kavya",
    "Kiran",
    "Meera",
    "Nikhil",
    "Priya",
    "Rahul",
    "Sanjana",
    "Suresh",
    "Vikram",
]

LAST_NAMES = [
    "Reddy",
    "Rao",
    "Sharma",
    "Varma",
    "Goud",
    "Naidu",
    "Patel",
    "Kumar",
    "Iyer",
    "Menon",
    "Chowdary",
    "Singh",
]

ORG_PREFIXES = [
    "Sri",
    "Urban",
    "Green",
    "Sree",
    "Apex",
    "Srinidhi",
    "Vertex",
    "Nava",
]

ORG_SUFFIXES = [
    "Developers LLP",
    "Constructions Pvt Ltd",
    "Estates",
    "Infra Holdings",
    "Educational Trust",
    "Healthcare Foundation",
    "Civic Services Society",
]


def configure_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s - %(message)s",
    )


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=True), encoding="utf-8")


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def stable_unit(value: str) -> float:
    digest = hashlib.sha256(value.encode("utf-8")).hexdigest()
    return int(digest[:12], 16) / float(0xFFFFFFFFFFFF)


def stable_choice(options: list[str], key: str) -> str:
    index = int(stable_unit(key) * len(options)) % len(options)
    return options[index]


def clean_slug(value: str) -> str:
    return value.lower().replace("_", "-").replace(" ", "-")


def parse_sequence(property_id: str) -> int:
    return int(property_id.rsplit("-", 1)[1])


def property_token(property_id: str) -> str:
    return property_id.removeprefix("PROP-")


def iso_date(year: int, month: int, day: int) -> str:
    return date(year, month, day).isoformat()


def add_days(value: str, days: int) -> str:
    base = date.fromisoformat(value)
    return (base + timedelta(days=days)).isoformat()


def quota_counts(total: int, shares: dict[str, float]) -> dict[str, int]:
    raw = {key: total * share for key, share in shares.items()}
    counts = {key: int(math.floor(value)) for key, value in raw.items()}
    remainder = total - sum(counts.values())
    ranked = sorted(raw, key=lambda key: (raw[key] - counts[key], key), reverse=True)
    for key in ranked[:remainder]:
        counts[key] += 1
    return counts


def assign_by_quota(property_ids: list[str], shares: dict[str, float], namespace: str) -> dict[str, str]:
    counts = quota_counts(len(property_ids), shares)
    ranked = sorted(property_ids, key=lambda property_id: stable_unit(f"{namespace}:{property_id}"))
    assignments = {}
    cursor = 0
    for label, count in counts.items():
        for property_id in ranked[cursor : cursor + count]:
            assignments[property_id] = label
        cursor += count
    return assignments


def load_sources() -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    properties = read_json(MASTER_PROPERTIES_PATH)
    profiles = read_json(PROPERTY_PROFILES_PATH)
    pois = read_json(SYNTHETIC_POIS_PATH)

    property_ids = {item["property_id"] for item in properties}
    profile_ids = {item["property_id"] for item in profiles}
    if property_ids != profile_ids:
        missing_profiles = sorted(property_ids - profile_ids)[:10]
        missing_properties = sorted(profile_ids - property_ids)[:10]
        raise ValueError(
            "Source mismatch between master properties and property profiles: "
            f"missing_profiles={missing_profiles}, missing_properties={missing_properties}"
        )
    return properties, profiles, pois


def owner_name(owner_type: str, property_id: str, region: str) -> str:
    if owner_type == "organization":
        prefix = stable_choice(ORG_PREFIXES, f"org-prefix:{property_id}")
        suffix = stable_choice(ORG_SUFFIXES, f"org-suffix:{property_id}:{region}")
        return f"{prefix} {region.title()} {suffix}"
    first = stable_choice(INDIVIDUAL_FIRST_NAMES, f"first:{property_id}")
    last = stable_choice(LAST_NAMES, f"last:{property_id}")
    return f"{first} {last}"


def generated_person_name(key: str) -> str:
    first = stable_choice(INDIVIDUAL_FIRST_NAMES, f"hist-first:{key}")
    last = stable_choice(LAST_NAMES, f"hist-last:{key}")
    return f"{first} {last}"


def generate_owners(
    properties: list[dict[str, Any]], profiles_by_id: dict[str, dict[str, Any]]
) -> tuple[list[dict[str, Any]], list[dict[str, str]]]:
    property_ids = [item["property_id"] for item in properties]
    owner_type_by_property = assign_by_quota(
        property_ids,
        {"individual": 0.90, "organization": 0.10},
        "owner-type",
    )
    owners = []
    registry = []
    for item in sorted(properties, key=lambda row: row["property_id"]):
        property_id = item["property_id"]
        sequence = parse_sequence(property_id)
        token = property_token(property_id)
        owner_id = f"OWN-{token}"
        owner_type = owner_type_by_property[property_id]
        region = item["source_region"]
        full_name = owner_name(owner_type, property_id, region)
        email_name = full_name.lower().replace(" ", ".").replace(",", "")
        owners.append(
            {
                "owner_id": owner_id,
                "property_id": property_id,
                "owner_type": owner_type,
                "full_name": full_name,
                "phone": f"+91-9{sequence % 10}{(sequence * 7919) % 100000000:08d}",
                "email": f"{email_name}.{sequence}@infoland.example",
                "source_region": region,
            }
        )
        registry.append({"property_id": property_id, "owner_id": owner_id})
    return owners, registry


def quality_condition_inputs(
    properties: list[dict[str, Any]], profiles_by_id: dict[str, dict[str, Any]]
) -> dict[str, str]:
    property_ids = [item["property_id"] for item in properties]
    return assign_by_quota(
        property_ids,
        {
            "clean": 0.40,
            "minor_issues": 0.35,
            "moderate_issues": 0.15,
            "high_risk_candidate": 0.10,
        },
        "condition-profile",
    )


def transfer_count(condition: str, property_id: str) -> int:
    unit = stable_unit(f"transfer-count:{property_id}")
    if condition == "clean":
        return 1 if unit < 0.70 else 2
    if condition == "minor_issues":
        return 2 if unit < 0.75 else 3
    if condition == "moderate_issues":
        return 2 if unit < 0.25 else 3 if unit < 0.75 else 4
    return 3 if unit < 0.35 else 4 if unit < 0.80 else 5


def transfer_type(condition: str, property_id: str, index: int) -> str:
    if condition == "clean":
        options = ["sale", "sale", "inheritance"]
    elif condition == "minor_issues":
        options = ["sale", "inheritance", "gift"]
    elif condition == "moderate_issues":
        options = ["sale", "inheritance", "gift", "settlement"]
    else:
        options = ["sale", "settlement", "inheritance", "gift", "settlement"]
    return stable_choice(options, f"transfer-type:{property_id}:{index}")


def registration_date_for(property_id: str, condition: str) -> str:
    sequence = parse_sequence(property_id)
    year_floor = {
        "clean": 2008,
        "minor_issues": 2005,
        "moderate_issues": 2001,
        "high_risk_candidate": 1996,
    }[condition]
    span = 2021 - year_floor
    year = year_floor + (sequence * 7) % span
    month = 1 + (sequence * 5) % 12
    day = 1 + (sequence * 11) % 24
    return iso_date(year, month, day)


def generate_ownership_events(
    properties: list[dict[str, Any]],
    owners_by_property: dict[str, dict[str, Any]],
    condition_by_property: dict[str, str],
) -> list[dict[str, Any]]:
    events = []
    for item in sorted(properties, key=lambda row: row["property_id"]):
        property_id = item["property_id"]
        condition = condition_by_property[property_id]
        count = transfer_count(condition, property_id)
        current_owner_id = owners_by_property[property_id]["owner_id"]
        token = property_token(property_id)
        prior_owner_id = f"HOWN-{token}-00"
        event_start = registration_date_for(property_id, condition)
        for index in range(1, count + 1):
            if index == count:
                next_owner_id = current_owner_id
            else:
                next_owner_id = f"HOWN-{token}-{index:02d}"
            event_date = add_days(event_start, 365 * (index - 1) * 3 + 29 * index)
            events.append(
                {
                    "event_id": f"OE-{token}-{index:02d}",
                    "property_id": property_id,
                    "from_owner_id": prior_owner_id,
                    "to_owner_id": next_owner_id,
                    "transfer_type": transfer_type(condition, property_id, index),
                    "transfer_date": event_date,
                }
            )
            prior_owner_id = next_owner_id
    return events


def generate_metadata(
    properties: list[dict[str, Any]], profiles_by_id: dict[str, dict[str, Any]]
) -> list[dict[str, Any]]:
    records = []
    for item in sorted(properties, key=lambda row: row["property_id"]):
        property_id = item["property_id"]
        profile = profiles_by_id[property_id]
        property_class = profile["property_class"]
        sequence = parse_sequence(property_id)
        if property_class == "residential_plot":
            construction_status = "vacant_land"
            property_age = 0
            land_use = "residential"
        elif property_class in {"villa", "apartment"}:
            construction_status = "under_construction" if stable_unit(f"construction:{property_id}") < 0.18 else "completed"
            property_age = 0 if construction_status == "under_construction" else 1 + sequence % 18
            land_use = "residential"
        elif property_class == "commercial":
            construction_status = "under_construction" if stable_unit(f"construction:{property_id}") < 0.12 else "completed"
            property_age = 0 if construction_status == "under_construction" else 2 + sequence % 22
            land_use = "commercial"
        elif property_class in {"school", "hospital", "government"}:
            construction_status = "completed"
            property_age = 4 + sequence % 30
            land_use = "institutional"
        else:
            construction_status = "vacant_land"
            property_age = 0
            land_use = "recreational"

        region = item["source_region"]
        zone_type = "urban" if region == "kokapet" else "semi_urban"
        if region == "kokapet":
            development_stage = "developed" if profile["area_segment"] != "large" else "developing"
        elif region == "mokila":
            development_stage = "developing"
        else:
            development_stage = "undeveloped" if property_class == "residential_plot" else "developing"

        records.append(
            {
                "property_id": property_id,
                "property_age_years": property_age,
                "construction_status": construction_status,
                "land_use": land_use,
                "zone_type": zone_type,
                "development_stage": development_stage,
            }
        )
    return records


def select_loans(
    properties: list[dict[str, Any]],
    condition_by_property: dict[str, str],
    profiles_by_id: dict[str, dict[str, Any]],
) -> set[str]:
    target_count = round(len(properties) * 0.18)
    weights = {
        "clean": 0.25,
        "minor_issues": 1.0,
        "moderate_issues": 1.8,
        "high_risk_candidate": 2.4,
    }
    eligible = [
        item["property_id"]
        for item in properties
        if profiles_by_id[item["property_id"]]["property_class"] not in {"government", "school", "hospital", "park"}
    ]
    ranked = sorted(
        eligible,
        key=lambda property_id: (
            stable_unit(f"loan:{property_id}") * weights[condition_by_property[property_id]],
            property_id,
        ),
        reverse=True,
    )
    return set(ranked[:target_count])


def generate_loans(
    loan_property_ids: set[str],
    profiles_by_id: dict[str, dict[str, Any]],
    condition_by_property: dict[str, str],
) -> list[dict[str, Any]]:
    records = []
    for property_id in sorted(loan_property_ids):
        condition = condition_by_property[property_id]
        active_threshold = {
            "clean": 0.15,
            "minor_issues": 0.35,
            "moderate_issues": 0.55,
            "high_risk_candidate": 0.75,
        }[condition]
        status = "active" if stable_unit(f"loan-status:{property_id}") < active_threshold else "closed"
        property_class = profiles_by_id[property_id]["property_class"]
        loan_type = "commercial_mortgage" if property_class == "commercial" else "home_loan"
        base_amount = {
            "residential_plot": 1800000,
            "villa": 8500000,
            "apartment": 5200000,
            "commercial": 12000000,
        }.get(property_class, 2500000)
        amount = 0 if status == "closed" else base_amount + (parse_sequence(property_id) % 19) * 125000
        records.append(
            {
                "loan_id": f"LOAN-{property_token(property_id)}",
                "property_id": property_id,
                "status": status,
                "loan_type": loan_type,
                "outstanding_amount": amount,
            }
        )
    return records


def select_pending_tax(
    properties: list[dict[str, Any]],
    condition_by_property: dict[str, str],
) -> set[str]:
    target_count = round(len(properties) * 0.14)
    weights = {
        "clean": 0.08,
        "minor_issues": 0.75,
        "moderate_issues": 1.8,
        "high_risk_candidate": 2.6,
    }
    ranked = sorted(
        [item["property_id"] for item in properties],
        key=lambda property_id: (
            stable_unit(f"pending-tax:{property_id}") * weights[condition_by_property[property_id]],
            property_id,
        ),
        reverse=True,
    )
    return set(ranked[:target_count])


def generate_tax_records(
    properties: list[dict[str, Any]], pending_property_ids: set[str]
) -> list[dict[str, Any]]:
    records = []
    for item in sorted(properties, key=lambda row: row["property_id"]):
        property_id = item["property_id"]
        pending = property_id in pending_property_ids
        annual_tax = int(max(1800, round(float(item["area_sq_ft"]) * 3.2)))
        pending_amount = 0 if not pending else annual_tax * (1 + parse_sequence(property_id) % 3)
        records.append(
            {
                "tax_id": f"TAX-{property_token(property_id)}",
                "property_id": property_id,
                "status": "pending" if pending else "paid",
                "pending_amount": pending_amount,
            }
        )
    return records


def select_disputes(
    properties: list[dict[str, Any]],
    condition_by_property: dict[str, str],
    profiles_by_id: dict[str, dict[str, Any]],
) -> set[str]:
    target_count = round(len(properties) * 0.04)
    weights = {
        "clean": 0.02,
        "minor_issues": 0.35,
        "moderate_issues": 1.7,
        "high_risk_candidate": 3.0,
    }
    eligible = [
        item["property_id"]
        for item in properties
        if profiles_by_id[item["property_id"]]["property_class"] not in {"government", "school", "hospital", "park"}
    ]
    ranked = sorted(
        eligible,
        key=lambda property_id: (
            stable_unit(f"dispute:{property_id}") * weights[condition_by_property[property_id]],
            property_id,
        ),
        reverse=True,
    )
    return set(ranked[:target_count])


def generate_court_disputes(
    dispute_property_ids: set[str], condition_by_property: dict[str, str]
) -> list[dict[str, Any]]:
    records = []
    case_types = ["title_dispute", "boundary_dispute", "inheritance_dispute", "sale_agreement_dispute"]
    for property_id in sorted(dispute_property_ids):
        condition = condition_by_property[property_id]
        active_threshold = 0.72 if condition == "high_risk_candidate" else 0.52
        status = "active" if stable_unit(f"dispute-status:{property_id}") < active_threshold else "closed"
        records.append(
            {
                "dispute_id": f"DISP-{property_token(property_id)}",
                "property_id": property_id,
                "case_type": stable_choice(case_types, f"case-type:{property_id}"),
                "status": status,
            }
        )
    return records


def document_target(condition: str, property_id: str) -> int:
    unit = stable_unit(f"doc-target:{property_id}")
    if condition == "clean":
        return 16 + int(unit * 3)
    if condition == "minor_issues":
        return 13 + int(unit * 3)
    if condition == "moderate_issues":
        return 10 + int(unit * 3)
    return 6 + int(unit * 4)


def required_document_keys(
    property_id: str,
    profile: dict[str, Any],
    has_loan: bool,
    has_active_loan: bool,
    has_pending_tax: bool,
    has_dispute: bool,
) -> set[str]:
    property_class = profile["property_class"]
    keys = {
        "sale_deed",
        "mother_deed",
        "encumbrance_certificate",
        "property_tax_receipt",
        "mutation_record",
        "survey_map",
        "khata_certificate",
        "khata_extract",
        "identity_proof",
    }
    if property_class in {"villa", "apartment", "commercial", "school", "hospital", "government"}:
        keys.update(
            {
                "building_approval_plan",
                "occupancy_certificate",
                "completion_certificate",
                "noc",
            }
        )
    else:
        keys.update({"layout_approval", "land_conversion_certificate"})
    if profile["sale_status"] == "for_sale" or has_pending_tax:
        keys.add("property_tax_receipt")
    if has_loan or has_active_loan:
        keys.add("encumbrance_certificate")
    if has_dispute:
        keys.add("court_dispute_record")
    if stable_unit(f"poa:{property_id}") < 0.17:
        keys.add("power_of_attorney")
    if profile["property_class"] == "residential_plot":
        keys.add("rtc_record")
    return keys


def choose_available_document_keys(
    property_id: str,
    profile: dict[str, Any],
    condition: str,
    transfer_count_value: int,
    has_loan: bool,
    has_active_loan: bool,
    has_pending_tax: bool,
    has_dispute: bool,
) -> set[str]:
    target = document_target(condition, property_id)
    if transfer_count_value >= 4:
        target = max(6, target - 1)
    keys = required_document_keys(property_id, profile, has_loan, has_active_loan, has_pending_tax, has_dispute)
    all_keys = [item["key"] for item in DOCUMENT_TYPES]
    ranked_optional = sorted(
        [key for key in all_keys if key not in keys],
        key=lambda key: stable_unit(f"doc-optional:{property_id}:{key}"),
        reverse=True,
    )
    for key in ranked_optional:
        if len(keys) >= target:
            break
        keys.add(key)
    if len(keys) > target:
        removable = sorted(
            [key for key in keys if key not in {"court_dispute_record", "property_tax_receipt", "identity_proof"}],
            key=lambda key: stable_unit(f"doc-remove:{property_id}:{key}"),
        )
        while len(keys) > target and removable:
            candidate = removable.pop(0)
            if candidate == "encumbrance_certificate" and has_active_loan:
                continue
            keys.remove(candidate)
    return keys


def issuing_authority(document_key: str, region: str) -> str:
    mapping = {
        "sale_deed": f"{region.title()} Sub-Registrar Office",
        "mother_deed": f"{region.title()} Sub-Registrar Office",
        "encumbrance_certificate": f"{region.title()} Registration Department",
        "property_tax_receipt": f"{region.title()} Municipal Revenue Office",
        "mutation_record": f"{region.title()} Revenue Department",
        "survey_map": f"{region.title()} Survey and Land Records Office",
        "rtc_record": f"{region.title()} Mandal Revenue Office",
        "khata_certificate": f"{region.title()} Panchayat Office",
        "khata_extract": f"{region.title()} Panchayat Office",
        "building_approval_plan": f"{region.title()} Planning Authority",
        "layout_approval": f"{region.title()} Urban Development Authority",
        "land_conversion_certificate": "Telangana Revenue Department",
        "occupancy_certificate": f"{region.title()} Building Permissions Office",
        "completion_certificate": f"{region.title()} Building Permissions Office",
        "noc": f"{region.title()} Fire and Civic NOC Cell",
        "identity_proof": "Government Identity Authority",
        "power_of_attorney": f"{region.title()} Notary and Registration Office",
        "court_dispute_record": f"{region.title()} Civil Court",
    }
    return mapping[document_key]


def missing_document_record(
    property_id: str,
    document_key: str,
    document_type: str,
    region: str,
) -> dict[str, Any]:
    return {
        "document_id": f"DOC-{clean_slug(document_key).upper()}-{property_token(property_id)}",
        "property_id": property_id,
        "document_type": document_type,
        "status": "missing",
        "issue_date": None,
        "last_updated": None,
        "issuing_authority": issuing_authority(document_key, region),
        "document_number": None,
        "remarks": "Document not available in source packet",
    }


def base_document_record(
    property_id: str,
    document_key: str,
    document_type: str,
    region: str,
    registration_date: str,
    status: str,
) -> dict[str, Any]:
    sequence = parse_sequence(property_id)
    issue_date = add_days(registration_date, 14 + sequence % 120)
    last_updated = add_days(issue_date, 365 * (1 + sequence % 5))
    return {
        "document_id": f"DOC-{clean_slug(document_key).upper()}-{property_token(property_id)}",
        "property_id": property_id,
        "document_type": document_type,
        "status": status,
        "issue_date": issue_date,
        "last_updated": last_updated,
        "issuing_authority": issuing_authority(document_key, region),
        "document_number": f"{document_key[:3].upper()}-{region[:3].upper()}-{sequence:06d}",
        "remarks": "Available in generated source packet" if status == "available" else "Document requires renewal or updated extract",
    }


def document_status(
    property_id: str,
    document_key: str,
    condition: str,
    has_active_loan: bool,
    has_pending_tax: bool,
) -> str:
    if document_key == "encumbrance_certificate" and has_active_loan:
        return "expired" if stable_unit(f"ec-outdated:{property_id}") < 0.45 else "available"
    if document_key == "property_tax_receipt" and has_pending_tax:
        return "available"
    expired_threshold = {
        "clean": 0.02,
        "minor_issues": 0.07,
        "moderate_issues": 0.15,
        "high_risk_candidate": 0.24,
    }[condition]
    return "expired" if stable_unit(f"doc-expired:{property_id}:{document_key}") < expired_threshold else "available"


def add_document_specific_fields(
    record: dict[str, Any],
    document_key: str,
    property_item: dict[str, Any],
    profile: dict[str, Any],
    owner: dict[str, Any],
    ownership_events: list[dict[str, Any]],
    tax_record: dict[str, Any],
    loan: dict[str, Any] | None,
    dispute: dict[str, Any] | None,
    registration_date: str,
) -> None:
    property_id = property_item["property_id"]
    sequence = parse_sequence(property_id)
    area_sqyd = float(property_item["area_sq_yd"])
    owner_full_name = owner["full_name"]
    first_seller = generated_person_name(f"seller:{property_id}")
    chain_length = len(ownership_events)

    if record["status"] == "missing":
        for field in next(item for item in DOCUMENT_TYPES if item["key"] == document_key)["fields"]:
            record[field] = None
        return

    if document_key == "sale_deed":
        record.update(
            {
                "seller_name": first_seller,
                "buyer_name": owner_full_name,
                "registration_number": f"REG-{sequence:07d}",
                "registration_date": registration_date,
                "market_value": int(area_sqyd * 52000),
            }
        )
    elif document_key == "mother_deed":
        origin_year = max(1965, date.fromisoformat(registration_date).year - 8 - chain_length)
        record.update(
            {
                "parent_document_number": f"MD-PARENT-{sequence:06d}",
                "ownership_chain_length": chain_length,
                "origin_year": origin_year,
            }
        )
    elif document_key == "encumbrance_certificate":
        has_active_loan = bool(loan and loan["status"] == "active")
        record.update(
            {
                "ec_period_from": add_days(registration_date, -365 * 5),
                "ec_period_to": "2026-03-31" if record["status"] == "available" else "2024-03-31",
                "encumbrance_count": 1 if has_active_loan else 0,
                "active_encumbrance": has_active_loan,
            }
        )
    elif document_key == "property_tax_receipt":
        annual_tax = int(max(1800, round(float(property_item["area_sq_ft"]) * 3.2)))
        pending_amount = int(tax_record["pending_amount"])
        record.update(
            {
                "financial_year": "2025-2026",
                "tax_amount": annual_tax,
                "paid_amount": max(0, annual_tax - pending_amount),
                "pending_amount": pending_amount,
            }
        )
        if pending_amount:
            record["remarks"] = "Tax receipt shows outstanding municipal dues"
    elif document_key == "mutation_record":
        record.update(
            {
                "mutation_number": f"MUT-{sequence:06d}",
                "mutation_date": add_days(registration_date, 45),
                "reason": ownership_events[-1]["transfer_type"],
            }
        )
    elif document_key == "survey_map":
        record.update(
            {
                "survey_number": f"SY-{property_item['source_region'][:3].upper()}-{sequence % 9000:04d}",
                "plot_area_sqyd": round(area_sqyd, 2),
                "survey_date": add_days(registration_date, -60),
            }
        )
    elif document_key == "rtc_record":
        record.update(
            {
                "survey_number": f"SY-{property_item['source_region'][:3].upper()}-{sequence % 9000:04d}",
                "land_type": "dry" if profile["property_class"] == "residential_plot" else "converted",
                "cultivation_status": "not_cultivated",
            }
        )
    elif document_key == "khata_certificate":
        record.update(
            {
                "khata_number": f"KH-{sequence:06d}",
                "owner_name": owner_full_name,
            }
        )
    elif document_key == "khata_extract":
        record.update(
            {
                "khata_number": f"KH-{sequence:06d}",
                "assessment_value": int(area_sqyd * 42000),
            }
        )
    elif document_key == "building_approval_plan":
        floors = 1
        if profile["property_class"] == "villa":
            floors = 2
        elif profile["property_class"] == "apartment":
            floors = 8 + sequence % 12
        elif profile["property_class"] == "commercial":
            floors = 3 + sequence % 8
        record.update(
            {
                "approval_number": f"BAP-{sequence:06d}",
                "approved_floors": floors,
                "approval_date": add_days(registration_date, 90),
            }
        )
    elif document_key == "layout_approval":
        record.update(
            {
                "layout_number": f"LAY-{sequence:06d}",
                "approved_by": f"{property_item['source_region'].title()} Planning Authority",
                "approval_date": add_days(registration_date, 75),
            }
        )
    elif document_key == "land_conversion_certificate":
        record.update(
            {
                "conversion_type": "agricultural_to_residential"
                if profile["property_class"] == "residential_plot"
                else "agricultural_to_non_agricultural",
                "conversion_date": add_days(registration_date, -120),
            }
        )
    elif document_key == "occupancy_certificate":
        record.update(
            {
                "building_type": profile["property_class"],
                "occupancy_date": add_days(registration_date, 365),
            }
        )
    elif document_key == "completion_certificate":
        record.update(
            {
                "completion_date": add_days(registration_date, 330),
                "approved_structure": profile["property_class"],
            }
        )
    elif document_key == "noc":
        record.update(
            {
                "issuing_department": "Fire and Civic Services",
                "valid_until": "2028-03-31" if record["status"] == "available" else "2024-03-31",
            }
        )
    elif document_key == "identity_proof":
        record.update(
            {
                "owner_id": owner["owner_id"],
                "proof_type": "aadhaar" if owner["owner_type"] == "individual" else "company_pan",
                "proof_last4": f"{(sequence * 3571) % 10000:04d}",
            }
        )
    elif document_key == "power_of_attorney":
        record.update(
            {
                "principal_name": owner_full_name,
                "agent_name": generated_person_name(f"agent:{property_id}"),
                "valid_until": "2027-12-31" if record["status"] == "available" else "2023-12-31",
            }
        )
    elif document_key == "court_dispute_record":
        if dispute:
            record.update(
                {
                    "case_number": f"CS-{sequence:06d}-2025",
                    "court_name": f"{property_item['source_region'].title()} Civil Court",
                    "case_type": dispute["case_type"],
                    "case_status": dispute["status"],
                }
            )
            record["remarks"] = "Court dispute record linked to court_disputes collection"
        else:
            record.update(
                {
                    "case_number": f"NIL-{sequence:06d}",
                    "court_name": f"{property_item['source_region'].title()} Civil Court",
                    "case_type": "none",
                    "case_status": "no_case",
                }
            )


def generate_documents(
    properties: list[dict[str, Any]],
    profiles_by_id: dict[str, dict[str, Any]],
    owners_by_property: dict[str, dict[str, Any]],
    ownership_events_by_property: dict[str, list[dict[str, Any]]],
    condition_by_property: dict[str, str],
    loans_by_property: dict[str, dict[str, Any]],
    tax_by_property: dict[str, dict[str, Any]],
    disputes_by_property: dict[str, dict[str, Any]],
) -> tuple[dict[str, list[dict[str, Any]]], list[dict[str, Any]]]:
    documents_by_type = {item["key"]: [] for item in DOCUMENT_TYPES}
    all_documents = []
    for property_item in sorted(properties, key=lambda row: row["property_id"]):
        property_id = property_item["property_id"]
        profile = profiles_by_id[property_id]
        condition = condition_by_property[property_id]
        loan = loans_by_property.get(property_id)
        tax_record = tax_by_property[property_id]
        dispute = disputes_by_property.get(property_id)
        events = ownership_events_by_property[property_id]
        registration_date = events[0]["transfer_date"]
        available_keys = choose_available_document_keys(
            property_id=property_id,
            profile=profile,
            condition=condition,
            transfer_count_value=len(events),
            has_loan=bool(loan),
            has_active_loan=bool(loan and loan["status"] == "active"),
            has_pending_tax=tax_record["status"] == "pending",
            has_dispute=bool(dispute),
        )
        for document_info in DOCUMENT_TYPES:
            document_key = document_info["key"]
            if document_key in available_keys:
                status = document_status(
                    property_id,
                    document_key,
                    condition,
                    bool(loan and loan["status"] == "active"),
                    tax_record["status"] == "pending",
                )
                record = base_document_record(
                    property_id,
                    document_key,
                    document_info["document_type"],
                    property_item["source_region"],
                    registration_date,
                    status,
                )
            else:
                record = missing_document_record(
                    property_id,
                    document_key,
                    document_info["document_type"],
                    property_item["source_region"],
                )
            add_document_specific_fields(
                record,
                document_key,
                property_item,
                profile,
                owners_by_property[property_id],
                events,
                tax_record,
                loan,
                dispute,
                registration_date,
            )
            documents_by_type[document_key].append(record)
            all_documents.append(record)
    return documents_by_type, all_documents


def generate_timeline(
    properties: list[dict[str, Any]],
    ownership_events_by_property: dict[str, list[dict[str, Any]]],
    loans_by_property: dict[str, dict[str, Any]],
    tax_by_property: dict[str, dict[str, Any]],
    disputes_by_property: dict[str, dict[str, Any]],
) -> list[dict[str, Any]]:
    records = []
    for item in sorted(properties, key=lambda row: row["property_id"]):
        property_id = item["property_id"]
        events = []
        ownership_events = ownership_events_by_property[property_id]
        registration_date = ownership_events[0]["transfer_date"]
        events.append({"event_type": "registration", "event_date": registration_date})
        for ownership_event in ownership_events:
            events.append(
                {
                    "event_type": "ownership_transfer",
                    "event_date": ownership_event["transfer_date"],
                }
            )
        if property_id in loans_by_property:
            loan_start = add_days(ownership_events[-1]["transfer_date"], 40)
            events.append({"event_type": "loan_created", "event_date": loan_start})
            if loans_by_property[property_id]["status"] == "closed":
                events.append({"event_type": "loan_closed", "event_date": add_days(loan_start, 700)})
        events.append({"event_type": "mutation_updated", "event_date": add_days(ownership_events[-1]["transfer_date"], 45)})
        events.append({"event_type": "tax_paid", "event_date": "2026-03-20"})
        if property_id in disputes_by_property:
            dispute_date = add_days(ownership_events[-1]["transfer_date"], 120)
            events.append({"event_type": "court_dispute_filed", "event_date": dispute_date})
            if disputes_by_property[property_id]["status"] == "closed":
                events.append({"event_type": "court_dispute_closed", "event_date": add_days(dispute_date, 450)})
        records.append(
            {
                "property_id": property_id,
                "events": sorted(events, key=lambda event: (event["event_date"], event["event_type"])),
            }
        )
    return records


def generate_health_summary(
    properties: list[dict[str, Any]],
    all_documents: list[dict[str, Any]],
    loans_by_property: dict[str, dict[str, Any]],
    tax_by_property: dict[str, dict[str, Any]],
    disputes_by_property: dict[str, dict[str, Any]],
) -> list[dict[str, Any]]:
    document_counts = Counter()
    missing_counts = Counter()
    for document in all_documents:
        property_id = document["property_id"]
        if document["status"] == "missing":
            missing_counts[property_id] += 1
        else:
            document_counts[property_id] += 1

    records = []
    for item in sorted(properties, key=lambda row: row["property_id"]):
        property_id = item["property_id"]
        active_loan_count = 1 if loans_by_property.get(property_id, {}).get("status") == "active" else 0
        records.append(
            {
                "property_id": property_id,
                "document_count": document_counts[property_id],
                "missing_document_count": missing_counts[property_id],
                "active_loan_count": active_loan_count,
                "court_dispute_count": 1 if property_id in disputes_by_property else 0,
                "pending_tax_count": 1 if tax_by_property[property_id]["status"] == "pending" else 0,
            }
        )
    return records


def counter_dict(values: list[Any]) -> dict[str, int]:
    return dict(sorted(Counter(values).items()))


def status_counts(records: list[dict[str, Any]], field: str = "status") -> dict[str, int]:
    return counter_dict([record[field] for record in records])


def generate_reports(
    properties: list[dict[str, Any]],
    profiles: list[dict[str, Any]],
    pois: list[dict[str, Any]],
    condition_by_property: dict[str, str],
    owners: list[dict[str, Any]],
    ownership_events: list[dict[str, Any]],
    metadata: list[dict[str, Any]],
    health_summary: list[dict[str, Any]],
    registry: list[dict[str, Any]],
    loans: list[dict[str, Any]],
    tax_records: list[dict[str, Any]],
    disputes: list[dict[str, Any]],
    documents_by_type: dict[str, list[dict[str, Any]]],
    all_documents: list[dict[str, Any]],
    consistency_report: dict[str, Any],
) -> dict[Path, Any]:
    profile_by_id = {profile["property_id"]: profile for profile in profiles}
    reports: dict[Path, Any] = {}
    reports[REPORTS_DIR / "dataset_summary.json"] = {
        "generation_seed": BUSINESS_DATASET_SEED,
        "source_datasets": [
            str(MASTER_PROPERTIES_PATH.relative_to(ROOT_DIR)).replace("\\", "/"),
            str(PROPERTY_PROFILES_PATH.relative_to(ROOT_DIR)).replace("\\", "/"),
            str(SYNTHETIC_POIS_PATH.relative_to(ROOT_DIR)).replace("\\", "/"),
        ],
        "record_counts": {
            "properties": len(properties),
            "property_profiles": len(profiles),
            "pois": len(pois),
            "owners": len(owners),
            "ownership_events": len(ownership_events),
            "property_registry": len(registry),
            "property_metadata": len(metadata),
            "property_timeline": len(properties),
            "property_health_summary": len(health_summary),
            "documents_all": len(all_documents),
            "loans": len(loans),
            "tax_records": len(tax_records),
            "court_disputes": len(disputes),
        },
        "data_condition_distribution": counter_dict(list(condition_by_property.values())),
    }
    reports[REPORTS_DIR / "property_stats.json"] = {
        "region_distribution": counter_dict([item["source_region"] for item in properties]),
        "property_class_distribution": counter_dict([profile["property_class"] for profile in profiles]),
        "sale_status_distribution": counter_dict([profile["sale_status"] for profile in profiles]),
        "metadata": {
            "construction_status_distribution": counter_dict([item["construction_status"] for item in metadata]),
            "land_use_distribution": counter_dict([item["land_use"] for item in metadata]),
            "zone_type_distribution": counter_dict([item["zone_type"] for item in metadata]),
            "development_stage_distribution": counter_dict([item["development_stage"] for item in metadata]),
        },
    }
    reports[REPORTS_DIR / "owner_stats.json"] = {
        "owner_type_distribution": counter_dict([owner["owner_type"] for owner in owners]),
        "source_region_distribution": counter_dict([owner["source_region"] for owner in owners]),
        "owners_per_property_min": 1,
        "owners_per_property_max": 1,
    }
    reports[REPORTS_DIR / "document_stats.json"] = {
        "total_documents": len(all_documents),
        "document_type_counts": counter_dict([document["document_type"] for document in all_documents]),
        "status_distribution": status_counts(all_documents),
        "status_by_document_type": {
            info["document_type"]: status_counts(documents_by_type[info["key"]]) for info in DOCUMENT_TYPES
        },
        "document_completeness_distribution": counter_dict(
            [
                "excellent_16_18"
                if item["document_count"] >= 16
                else "good_13_15"
                if item["document_count"] >= 13
                else "average_10_12"
                if item["document_count"] >= 10
                else "poor_6_9"
                for item in health_summary
            ]
        ),
    }
    reports[REPORTS_DIR / "loan_stats.json"] = {
        "total_loans": len(loans),
        "properties_with_loans": len({loan["property_id"] for loan in loans}),
        "status_distribution": status_counts(loans),
        "loan_type_distribution": counter_dict([loan["loan_type"] for loan in loans]),
        "active_outstanding_amount_total": sum(loan["outstanding_amount"] for loan in loans if loan["status"] == "active"),
    }
    reports[REPORTS_DIR / "tax_stats.json"] = {
        "total_tax_records": len(tax_records),
        "status_distribution": status_counts(tax_records),
        "pending_amount_total": sum(record["pending_amount"] for record in tax_records),
    }
    reports[REPORTS_DIR / "court_dispute_stats.json"] = {
        "total_disputes": len(disputes),
        "properties_with_disputes": len({record["property_id"] for record in disputes}),
        "status_distribution": status_counts(disputes),
        "case_type_distribution": counter_dict([record["case_type"] for record in disputes]),
    }

    available_documents = [document for document in all_documents if document["status"] != "missing"]
    available_by_type = defaultdict(set)
    for document in available_documents:
        available_by_type[document["document_type"]].add(document["property_id"])
    reports[REPORTS_DIR / "dataset_coverage_report.json"] = {
        "properties_with_sale_deed": len(available_by_type["sale_deed"]),
        "properties_with_mother_deed": len(available_by_type["mother_deed"]),
        "properties_with_ec": len(available_by_type["encumbrance_certificate"]),
        "properties_with_loans": len({loan["property_id"] for loan in loans}),
        "properties_with_pending_tax": len([record for record in tax_records if record["status"] == "pending"]),
        "properties_with_disputes": len({record["property_id"] for record in disputes}),
        "coverage_by_document_type": {
            info["document_type"]: len(available_by_type[info["document_type"]]) for info in DOCUMENT_TYPES
        },
        "coverage_by_sale_status": {
            status: {
                "property_count": len([pid for pid, profile in profile_by_id.items() if profile["sale_status"] == status]),
                "document_records": len(
                    [
                        document
                        for document in available_documents
                        if profile_by_id[document["property_id"]]["sale_status"] == status
                    ]
                ),
            }
            for status in ["for_sale", "not_for_sale"]
        },
    }
    reports[REPORTS_DIR / "consistency_report.json"] = consistency_report
    reports[REPORTS_DIR / "mongodb_import_summary.json"] = {
        "target_database": "MongoDB Atlas",
        "collections": [
            {"collection": "property_registry", "path": "data/generated/property_registry.json", "record_count": len(registry)},
            {"collection": "owners", "path": "data/generated/owners.json", "record_count": len(owners)},
            {
                "collection": "ownership_events",
                "path": "data/generated/ownership_events.json",
                "record_count": len(ownership_events),
            },
            {
                "collection": "property_metadata",
                "path": "data/generated/property_metadata.json",
                "record_count": len(metadata),
            },
            {
                "collection": "property_timeline",
                "path": "data/generated/property_timeline.json",
                "record_count": len(properties),
            },
            {
                "collection": "property_health_summary",
                "path": "data/generated/property_health_summary.json",
                "record_count": len(health_summary),
            },
            {"collection": "loans", "path": "data/generated/loans.json", "record_count": len(loans)},
            {"collection": "tax_records", "path": "data/generated/tax_records.json", "record_count": len(tax_records)},
            {
                "collection": "court_disputes",
                "path": "data/generated/court_disputes.json",
                "record_count": len(disputes),
            },
            {
                "collection": "documents_all",
                "path": "data/generated/documents/documents_all.json",
                "record_count": len(all_documents),
            },
        ],
        "document_collections": [
            {
                "collection": info["document_type"],
                "path": f"data/generated/documents/{info['file']}",
                "record_count": len(documents_by_type[info["key"]]),
            }
            for info in DOCUMENT_TYPES
        ],
        "primary_reference_field": "property_id",
        "geometry_policy": "Geometry remains only in data/master/master_properties.json",
    }
    reports[REPORTS_DIR / "document_schema_catalog.json"] = {
        "common_fields": COMMON_DOCUMENT_FIELDS,
        "status_values": ["available", "missing", "expired"],
        "document_types": [
            {
                "document_type": info["document_type"],
                "file": f"data/generated/documents/{info['file']}",
                "additional_fields": info["fields"],
            }
            for info in DOCUMENT_TYPES
        ],
        "field_note": "court_dispute_record uses case_status for the case state so the common document status field remains available/missing/expired.",
    }
    return reports


def validate_consistency(
    properties: list[dict[str, Any]],
    owners: list[dict[str, Any]],
    ownership_events: list[dict[str, Any]],
    registry: list[dict[str, Any]],
    metadata: list[dict[str, Any]],
    timeline: list[dict[str, Any]],
    health_summary: list[dict[str, Any]],
    loans: list[dict[str, Any]],
    tax_records: list[dict[str, Any]],
    disputes: list[dict[str, Any]],
    documents_by_type: dict[str, list[dict[str, Any]]],
    all_documents: list[dict[str, Any]],
) -> dict[str, Any]:
    property_ids = {item["property_id"] for item in properties}
    owner_ids = {owner["owner_id"] for owner in owners}
    owners_by_property = {owner["property_id"]: owner for owner in owners}
    registry_pairs = {(record["property_id"], record["owner_id"]) for record in registry}
    events_by_property: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for event in ownership_events:
        events_by_property[event["property_id"]].append(event)

    invalid_property_references = []
    for name, records in [
        ("owners", owners),
        ("ownership_events", ownership_events),
        ("property_registry", registry),
        ("property_metadata", metadata),
        ("property_timeline", timeline),
        ("property_health_summary", health_summary),
        ("loans", loans),
        ("tax_records", tax_records),
        ("court_disputes", disputes),
        ("documents_all", all_documents),
    ]:
        invalid_property_references.extend(
            {"collection": name, "property_id": record["property_id"]}
            for record in records
            if record["property_id"] not in property_ids
        )

    orphan_owners = [owner for owner in owners if owner["property_id"] not in property_ids]
    registry_errors = [
        record
        for record in registry
        if record["property_id"] not in owners_by_property
        or owners_by_property[record["property_id"]]["owner_id"] != record["owner_id"]
    ]
    owner_property_counts = Counter(owner["property_id"] for owner in owners)
    duplicate_current_owners = {
        property_id: count for property_id, count in owner_property_counts.items() if count != 1
    }
    missing_current_owners = sorted(property_ids - set(owner_property_counts))

    ownership_chain_errors = []
    for property_id in sorted(property_ids):
        chain = sorted(events_by_property[property_id], key=lambda row: row["transfer_date"])
        if not chain:
            ownership_chain_errors.append({"property_id": property_id, "error": "missing_chain"})
            continue
        for previous, current in zip(chain, chain[1:]):
            if previous["to_owner_id"] != current["from_owner_id"]:
                ownership_chain_errors.append({"property_id": property_id, "error": "broken_owner_chain"})
                break
        if chain[-1]["to_owner_id"] != owners_by_property[property_id]["owner_id"]:
            ownership_chain_errors.append({"property_id": property_id, "error": "current_owner_mismatch"})

    documents_merged_count = sum(len(records) for records in documents_by_type.values())
    document_id_counts = Counter(document["document_id"] for document in all_documents)
    duplicate_document_ids = {
        document_id: count for document_id, count in document_id_counts.items() if count != 1
    }
    duplicate_owner_ids = {
        owner_id: count for owner_id, count in Counter(owner["owner_id"] for owner in owners).items() if count != 1
    }
    duplicate_event_ids = {
        event_id: count
        for event_id, count in Counter(event["event_id"] for event in ownership_events).items()
        if count != 1
    }
    duplicate_loan_ids = {
        loan_id: count for loan_id, count in Counter(loan["loan_id"] for loan in loans).items() if count != 1
    }
    duplicate_tax_ids = {
        tax_id: count
        for tax_id, count in Counter(record["tax_id"] for record in tax_records).items()
        if count != 1
    }
    duplicate_dispute_ids = {
        dispute_id: count
        for dispute_id, count in Counter(record["dispute_id"] for record in disputes).items()
        if count != 1
    }

    loans_by_property = {loan["property_id"]: loan for loan in loans}
    tax_by_property = {record["property_id"]: record for record in tax_records}
    disputes_by_property = {record["property_id"]: record for record in disputes}
    documents_by_property_type = {
        (document["property_id"], document["document_type"]): document for document in all_documents
    }

    court_document_errors = []
    for dispute in disputes:
        document = documents_by_property_type.get((dispute["property_id"], "court_dispute_record"))
        if not document or document["status"] == "missing" or document.get("case_type") != dispute["case_type"]:
            court_document_errors.append(dispute["property_id"])

    active_loan_ec_errors = []
    for loan in loans:
        if loan["status"] != "active":
            continue
        document = documents_by_property_type.get((loan["property_id"], "encumbrance_certificate"))
        if not document or document["status"] == "missing" or not document.get("active_encumbrance"):
            active_loan_ec_errors.append(loan["property_id"])

    pending_tax_receipt_errors = []
    for tax_record in tax_records:
        if tax_record["status"] != "pending":
            continue
        document = documents_by_property_type.get((tax_record["property_id"], "property_tax_receipt"))
        if not document or document["status"] == "missing" or document.get("pending_amount") != tax_record["pending_amount"]:
            pending_tax_receipt_errors.append(tax_record["property_id"])

    health_by_property = {record["property_id"]: record for record in health_summary}
    health_summary_errors = []
    document_count_by_property = Counter()
    missing_count_by_property = Counter()
    for document in all_documents:
        if document["status"] == "missing":
            missing_count_by_property[document["property_id"]] += 1
        else:
            document_count_by_property[document["property_id"]] += 1
    for property_id in sorted(property_ids):
        expected = {
            "document_count": document_count_by_property[property_id],
            "missing_document_count": missing_count_by_property[property_id],
            "active_loan_count": 1 if loans_by_property.get(property_id, {}).get("status") == "active" else 0,
            "court_dispute_count": 1 if property_id in disputes_by_property else 0,
            "pending_tax_count": 1 if tax_by_property[property_id]["status"] == "pending" else 0,
        }
        actual = {key: health_by_property[property_id][key] for key in expected}
        if actual != expected:
            health_summary_errors.append({"property_id": property_id, "expected": expected, "actual": actual})

    timeline_by_property = {record["property_id"]: record for record in timeline}
    timeline_errors = []
    for property_id in sorted(property_ids):
        event_types = [event["event_type"] for event in timeline_by_property[property_id]["events"]]
        if "registration" not in event_types or "ownership_transfer" not in event_types:
            timeline_errors.append({"property_id": property_id, "error": "missing_registration_or_transfer"})
        if property_id in loans_by_property and "loan_created" not in event_types:
            timeline_errors.append({"property_id": property_id, "error": "missing_loan_event"})
        if property_id in disputes_by_property and "court_dispute_filed" not in event_types:
            timeline_errors.append({"property_id": property_id, "error": "missing_dispute_event"})

    metrics = {
        "orphan_owners": len(orphan_owners),
        "orphan_documents": len([doc for doc in all_documents if doc["property_id"] not in property_ids]),
        "orphan_loans": len([loan for loan in loans if loan["property_id"] not in property_ids]),
        "orphan_tax_records": len([record for record in tax_records if record["property_id"] not in property_ids]),
        "orphan_disputes": len([record for record in disputes if record["property_id"] not in property_ids]),
        "invalid_property_references": len(invalid_property_references),
        "ownership_chain_errors": len(ownership_chain_errors),
        "registry_errors": len(registry_errors),
        "duplicate_current_owners": len(duplicate_current_owners),
        "missing_current_owners": len(missing_current_owners),
        "document_merge_count_mismatch": 0 if documents_merged_count == len(all_documents) else 1,
        "duplicate_owner_ids": len(duplicate_owner_ids),
        "duplicate_event_ids": len(duplicate_event_ids),
        "duplicate_loan_ids": len(duplicate_loan_ids),
        "duplicate_tax_ids": len(duplicate_tax_ids),
        "duplicate_dispute_ids": len(duplicate_dispute_ids),
        "duplicate_document_ids": len(duplicate_document_ids),
        "court_dispute_document_errors": len(court_document_errors),
        "active_loan_ec_errors": len(active_loan_ec_errors),
        "pending_tax_receipt_errors": len(pending_tax_receipt_errors),
        "health_summary_errors": len(health_summary_errors),
        "timeline_errors": len(timeline_errors),
    }
    return {
        "status": "passed" if all(value == 0 for value in metrics.values()) else "failed",
        "metrics": metrics,
        "details": {
            "invalid_property_references": invalid_property_references[:20],
            "ownership_chain_errors": ownership_chain_errors[:20],
            "registry_errors": registry_errors[:20],
            "duplicate_current_owners": duplicate_current_owners,
            "missing_current_owners": missing_current_owners[:20],
            "duplicate_owner_ids": duplicate_owner_ids,
            "duplicate_event_ids": duplicate_event_ids,
            "duplicate_loan_ids": duplicate_loan_ids,
            "duplicate_tax_ids": duplicate_tax_ids,
            "duplicate_dispute_ids": duplicate_dispute_ids,
            "duplicate_document_ids": duplicate_document_ids,
            "court_dispute_document_errors": court_document_errors[:20],
            "active_loan_ec_errors": active_loan_ec_errors[:20],
            "pending_tax_receipt_errors": pending_tax_receipt_errors[:20],
            "health_summary_errors": health_summary_errors[:20],
            "timeline_errors": timeline_errors[:20],
        },
    }


def write_document_samples(documents_by_type: dict[str, list[dict[str, Any]]]) -> None:
    for info in DOCUMENT_TYPES:
        records = documents_by_type[info["key"]]
        available = [record for record in records if record["status"] != "missing"]
        sample = available[:3] if available else records[:3]
        write_json(DOCUMENT_SAMPLES_DIR / f"{info['document_type']}_sample.json", sample)


def run_business_dataset_generation() -> dict[str, Any]:
    random.seed(BUSINESS_DATASET_SEED)
    properties, profiles, pois = load_sources()
    profiles_by_id = {profile["property_id"]: profile for profile in profiles}

    LOGGER.info("Loaded %s properties, %s profiles, %s POIs", len(properties), len(profiles), len(pois))

    condition_by_property = quality_condition_inputs(properties, profiles_by_id)
    owners, registry = generate_owners(properties, profiles_by_id)
    owners_by_property = {owner["property_id"]: owner for owner in owners}
    ownership_events = generate_ownership_events(properties, owners_by_property, condition_by_property)
    ownership_events_by_property: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for event in ownership_events:
        ownership_events_by_property[event["property_id"]].append(event)
    for events in ownership_events_by_property.values():
        events.sort(key=lambda event: event["transfer_date"])

    metadata = generate_metadata(properties, profiles_by_id)
    loan_property_ids = select_loans(properties, condition_by_property, profiles_by_id)
    loans = generate_loans(loan_property_ids, profiles_by_id, condition_by_property)
    loans_by_property = {loan["property_id"]: loan for loan in loans}
    pending_tax_property_ids = select_pending_tax(properties, condition_by_property)
    tax_records = generate_tax_records(properties, pending_tax_property_ids)
    tax_by_property = {record["property_id"]: record for record in tax_records}
    dispute_property_ids = select_disputes(properties, condition_by_property, profiles_by_id)
    disputes = generate_court_disputes(dispute_property_ids, condition_by_property)
    disputes_by_property = {record["property_id"]: record for record in disputes}
    documents_by_type, all_documents = generate_documents(
        properties,
        profiles_by_id,
        owners_by_property,
        ownership_events_by_property,
        condition_by_property,
        loans_by_property,
        tax_by_property,
        disputes_by_property,
    )
    timeline = generate_timeline(
        properties,
        ownership_events_by_property,
        loans_by_property,
        tax_by_property,
        disputes_by_property,
    )
    health_summary = generate_health_summary(
        properties,
        all_documents,
        loans_by_property,
        tax_by_property,
        disputes_by_property,
    )
    consistency_report = validate_consistency(
        properties,
        owners,
        ownership_events,
        registry,
        metadata,
        timeline,
        health_summary,
        loans,
        tax_records,
        disputes,
        documents_by_type,
        all_documents,
    )
    if consistency_report["status"] != "passed":
        raise ValueError(f"Consistency checks failed: {json.dumps(consistency_report, indent=2)}")

    write_json(GENERATED_DIR / "property_registry.json", registry)
    write_json(GENERATED_DIR / "owners.json", owners)
    write_json(GENERATED_DIR / "ownership_events.json", ownership_events)
    write_json(GENERATED_DIR / "property_metadata.json", metadata)
    write_json(GENERATED_DIR / "property_timeline.json", timeline)
    write_json(GENERATED_DIR / "property_health_summary.json", health_summary)
    write_json(GENERATED_DIR / "loans.json", loans)
    write_json(GENERATED_DIR / "tax_records.json", tax_records)
    write_json(GENERATED_DIR / "court_disputes.json", disputes)
    for info in DOCUMENT_TYPES:
        write_json(DOCUMENTS_DIR / info["file"], documents_by_type[info["key"]])
    write_json(DOCUMENTS_DIR / "documents_all.json", all_documents)

    reports = generate_reports(
        properties,
        profiles,
        pois,
        condition_by_property,
        owners,
        ownership_events,
        metadata,
        health_summary,
        registry,
        loans,
        tax_records,
        disputes,
        documents_by_type,
        all_documents,
        consistency_report,
    )
    for path, payload in reports.items():
        write_json(path, payload)
    write_document_samples(documents_by_type)

    summary = reports[REPORTS_DIR / "dataset_summary.json"]
    LOGGER.info("Business dataset generation complete: %s", summary["record_counts"])
    return summary


def main() -> None:
    configure_logging()
    summary = run_business_dataset_generation()
    LOGGER.info("Dataset summary written with seed %s", summary["generation_seed"])


if __name__ == "__main__":
    main()
