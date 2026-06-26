# Field Reference

This file documents every field discovered in the current primary generated datasets.

## master_properties

Path: `data/master/master_properties.json`  
Purpose: Canonical property source of truth with geometry and measurements.  
Records: 1633

| Field Name | Type | Description | Required / Optional | Example Value | Notes |
| --- | --- | --- | --- | --- | --- |
| area_sq_ft | number (1633) | Generated field: area sq ft. | Required | 1547.87 | Present in 1633 of 1633 records. |
| area_sq_m | number (1633) | Generated field: area sq m. | Required | 143.8 | Present in 1633 of 1633 records. |
| area_sq_yd | number (1633) | Generated field: area sq yd. | Required | 171.99 | Present in 1633 of 1633 records. |
| bbox | object (1633) | Bounding box object. | Required | {"max_lat": 17.3879113, "max_lon": 78.3343128, "min_lat": 17.3878061, "min_lo... | Present in 1633 of 1633 records. |
| building | string (1633) | Generated field: building. | Required | yes | Present in 1633 of 1633 records. |
| centroid_lat | number (1633) | Generated field: centroid lat. | Required | 17.3878587 | Present in 1633 of 1633 records. |
| centroid_lon | number (1633) | Generated field: centroid lon. | Required | 78.3342363 | Present in 1633 of 1633 records. |
| feature_category | string (1633) | Generated field: feature category. | Required | property_candidate | Present in 1633 of 1633 records. |
| geometry | object (1633) | GeoJSON geometry stored only in master_properties. | Required | {"coordinates": [[[78.334173, 17.3879113], [78.3341598, 17.3878258], [78.3342... | Present in 1633 of 1633 records. |
| perimeter_m | number (1633) | Generated field: perimeter m. | Required | 49.19 | Present in 1633 of 1633 records. |
| property_id | string (1633) | Stable cross-dataset property key. | Required | PROP-KOK-000001 | Present in 1633 of 1633 records. |
| source_id | string (1633) | Generated field: source id. | Required | way/356011387 | Present in 1633 of 1633 records. |
| source_region | string (1633) | Normalized source region. | Required | kokapet | Present in 1633 of 1633 records. |

## property_candidates

Path: `data/master/property_candidates.json`  
Purpose: Property-only candidate mirror from preprocessing.  
Records: 1633

| Field Name | Type | Description | Required / Optional | Example Value | Notes |
| --- | --- | --- | --- | --- | --- |
| area_sq_ft | number (1633) | Generated field: area sq ft. | Required | 1547.87 | Present in 1633 of 1633 records. |
| area_sq_m | number (1633) | Generated field: area sq m. | Required | 143.8 | Present in 1633 of 1633 records. |
| area_sq_yd | number (1633) | Generated field: area sq yd. | Required | 171.99 | Present in 1633 of 1633 records. |
| bbox | object (1633) | Bounding box object. | Required | {"max_lat": 17.3879113, "max_lon": 78.3343128, "min_lat": 17.3878061, "min_lo... | Present in 1633 of 1633 records. |
| building | string (1633) | Generated field: building. | Required | yes | Present in 1633 of 1633 records. |
| centroid_lat | number (1633) | Generated field: centroid lat. | Required | 17.3878587 | Present in 1633 of 1633 records. |
| centroid_lon | number (1633) | Generated field: centroid lon. | Required | 78.3342363 | Present in 1633 of 1633 records. |
| feature_category | string (1633) | Generated field: feature category. | Required | property_candidate | Present in 1633 of 1633 records. |
| geometry | object (1633) | GeoJSON geometry stored only in master_properties. | Required | {"coordinates": [[[78.334173, 17.3879113], [78.3341598, 17.3878258], [78.3342... | Present in 1633 of 1633 records. |
| perimeter_m | number (1633) | Generated field: perimeter m. | Required | 49.19 | Present in 1633 of 1633 records. |
| property_id | string (1633) | Stable cross-dataset property key. | Required | PROP-KOK-000001 | Present in 1633 of 1633 records. |
| source_id | string (1633) | Generated field: source id. | Required | way/356011387 | Present in 1633 of 1633 records. |
| source_region | string (1633) | Normalized source region. | Required | kokapet | Present in 1633 of 1633 records. |

## property_profiles

Path: `data/generated/property_profiles.json`  
Purpose: Synthetic profile per property.  
Records: 1633

| Field Name | Type | Description | Required / Optional | Example Value | Notes |
| --- | --- | --- | --- | --- | --- |
| area_segment | string (1633) | Generated field: area segment. | Required | medium | Present in 1633 of 1633 records. |
| future_risk_tier | string (1633) | Synthetic placeholder tier, not risk-engine output. | Required | low | Present in 1633 of 1633 records. |
| location_score | integer (1633) | Synthetic proximity score. | Required | 94 | Present in 1633 of 1633 records. |
| property_class | string (1633) | Business property type used across synthesis and legal generation. | Required | residential_plot | Extended values include clinic, community_center, religious, industrial, vacant_land. |
| property_id | string (1633) | Stable cross-dataset property key. | Required | PROP-KOK-000001 | Present in 1633 of 1633 records. |
| sale_status | string (1633) | Generated field: sale status. | Required | not_for_sale | Present in 1633 of 1633 records. |
| verification_workflow | string (1633) | Dataset workflow scope for frontend/backend verification. | Required | complete_property_verification | Values: complete_property_verification, institutional_property. |

## synthetic_pois

Path: `data/generated/synthetic_pois.json`  
Purpose: Building-anchored POI markers used for proximity scoring. Each POI is placed on an existing property centroid.
Records: 95

| Field Name | Type | Description | Required / Optional | Example Value | Notes |
| --- | --- | --- | --- | --- | --- |
| lat | number (95) | Latitude copied from source property centroid. | Required | 17.38997783 | Present in 95 of 95 records. |
| lon | number (95) | Longitude copied from source property centroid. | Required | 78.34046474 | Present in 95 of 95 records. |
| name | string (95) | Generated field: name. | Required | Green Valley School | Present in 95 of 95 records. |
| poi_id | string (95) | Generated field: poi id. | Required | POI-00001 | Present in 95 of 95 records. |
| poi_type | string (95) | Generated field: poi type. | Required | school | Present in 95 of 95 records. |
| property_id | string (95) | Source building property for this marker. | Required | PROP-KOK-000697 | Present in 95 of 95 records. |
| source_region | string (95) | Normalized source region. | Required | kokapet | Present in 95 of 95 records. |

## location_scores

Path: `data/generated/location_scores.json`  
Purpose: Generated proximity artifact, not a full location-intelligence engine.  
Records: 1633

| Field Name | Type | Description | Required / Optional | Example Value | Notes |
| --- | --- | --- | --- | --- | --- |
| distance_to_nearest_commercial_km | number (1398), null (235) | Generated field: distance to nearest commercial km. | Required, nullable | 0.056 | Present in 1633 of 1633 records. |
| distance_to_nearest_hospital_km | number (1633) | Generated field: distance to nearest hospital km. | Required | 0.417 | Present in 1633 of 1633 records. |
| distance_to_nearest_park_km | number (1633) | Generated field: distance to nearest park km. | Required | 0.023 | Present in 1633 of 1633 records. |
| distance_to_nearest_school_km | number (1633) | Generated field: distance to nearest school km. | Required | 0.113 | Present in 1633 of 1633 records. |
| location_score | integer (1633) | Synthetic proximity score. | Required | 94 | Present in 1633 of 1633 records. |
| nearby_commercial_count | integer (1633) | Generated field: nearby commercial count. | Required | 10 | Present in 1633 of 1633 records. |
| nearby_hospital_count | integer (1633) | Generated field: nearby hospital count. | Required | 6 | Present in 1633 of 1633 records. |
| nearby_park_count | integer (1633) | Generated field: nearby park count. | Required | 12 | Present in 1633 of 1633 records. |
| nearby_school_count | integer (1633) | Generated field: nearby school count. | Required | 10 | Present in 1633 of 1633 records. |
| property_id | string (1633) | Stable cross-dataset property key. | Required | PROP-KOK-000001 | Present in 1633 of 1633 records. |

## owners

Path: `data/generated/owners.json`  
Purpose: Current owner per property.  
Records: 1633

| Field Name | Type | Description | Required / Optional | Example Value | Notes |
| --- | --- | --- | --- | --- | --- |
| email | string (1633) | Generated field: email. | Required | vikram.menon.1@infoland.example | Present in 1633 of 1633 records. |
| full_name | string (1633) | Generated field: full name. | Required | Vikram Menon | Present in 1633 of 1633 records. |
| owner_id | string (1633) | Current owner identifier. | Required | OWN-KOK-000001 | Present in 1633 of 1633 records. |
| owner_type | string (1633) | Generated field: owner type. | Required | individual | Present in 1633 of 1633 records. |
| phone | string (1633) | Generated field: phone. | Required | +91-9100007919 | Present in 1633 of 1633 records. |
| property_id | string (1633) | Stable cross-dataset property key. | Required | PROP-KOK-000001 | Present in 1633 of 1633 records. |
| source_region | string (1633) | Normalized source region. | Required | kokapet | Present in 1633 of 1633 records. |

## ownership_events

Path: `data/generated/ownership_events.json`  
Purpose: Ownership transfer history.  
Records: 3517

| Field Name | Type | Description | Required / Optional | Example Value | Notes |
| --- | --- | --- | --- | --- | --- |
| event_id | string (3517) | Generated field: event id. | Required | OE-KOK-000001-01 | Present in 3517 of 3517 records. |
| from_owner_id | string (3517) | Generated field: from owner id. | Required | HOWN-KOK-000001-00 | Present in 3517 of 3517 records. |
| property_id | string (3517) | Stable cross-dataset property key. | Required | PROP-KOK-000001 | Present in 3517 of 3517 records. |
| to_owner_id | string (3517) | Generated field: to owner id. | Required | HOWN-KOK-000001-01 | Present in 3517 of 3517 records. |
| transfer_date | string (3517) | Generated field: transfer date. | Required | 2012-07-11 | Present in 3517 of 3517 records. |
| transfer_type | string (3517) | Generated field: transfer type. | Required | sale | Present in 3517 of 3517 records. |

## property_registry

Path: `data/generated/property_registry.json`  
Purpose: Property to current owner bridge.  
Records: 1633

| Field Name | Type | Description | Required / Optional | Example Value | Notes |
| --- | --- | --- | --- | --- | --- |
| owner_id | string (1633) | Current owner identifier. | Required | OWN-KOK-000001 | Present in 1633 of 1633 records. |
| property_id | string (1633) | Stable cross-dataset property key. | Required | PROP-KOK-000001 | Present in 1633 of 1633 records. |

## property_metadata

Path: `data/generated/property_metadata.json`  
Purpose: Construction, land-use, zone, and development metadata.  
Records: 1633

| Field Name | Type | Description | Required / Optional | Example Value | Notes |
| --- | --- | --- | --- | --- | --- |
| construction_status | string (1633) | Generated field: construction status. | Required | vacant_land | Present in 1633 of 1633 records. |
| development_stage | string (1633) | Generated field: development stage. | Required | developed | Present in 1633 of 1633 records. |
| land_use | string (1633) | Generated field: land use. | Required | residential | Present in 1633 of 1633 records. |
| property_age_years | integer (1633) | Generated field: property age years. | Required | 0 | Present in 1633 of 1633 records. |
| property_id | string (1633) | Stable cross-dataset property key. | Required | PROP-KOK-000001 | Present in 1633 of 1633 records. |
| zone_type | string (1633) | Generated field: zone type. | Required | urban | Present in 1633 of 1633 records. |

## property_timeline

Path: `data/generated/property_timeline.json`  
Purpose: Per-property event timeline.  
Records: 1633

| Field Name | Type | Description | Required / Optional | Example Value | Notes |
| --- | --- | --- | --- | --- | --- |
| events | array (1633) | Timeline event array. | Required | [{"event_type": "ownership_transfer", "event_date": "2012-07-11"}, {"event_ty... | Present in 1633 of 1633 records. |
| property_id | string (1633) | Stable cross-dataset property key. | Required | PROP-KOK-000001 | Present in 1633 of 1633 records. |

## property_health_summary

Path: `data/generated/property_health_summary.json`  
Purpose: Per-property summary of documents, loans, disputes, and taxes.  
Records: 1633

| Field Name | Type | Description | Required / Optional | Example Value | Notes |
| --- | --- | --- | --- | --- | --- |
| active_loan_count | integer (1633) | Generated field: active loan count. | Required | 0 | Present in 1633 of 1633 records. |
| court_dispute_count | integer (1633) | Generated field: court dispute count. | Required | 0 | Present in 1633 of 1633 records. |
| document_count | integer (1633) | Generated field: document count. | Required | 13 | Present in 1633 of 1633 records. |
| missing_document_count | integer (1633) | Generated field: missing document count. | Required | 5 | Present in 1633 of 1633 records. |
| pending_tax_count | integer (1633) | Generated field: pending tax count. | Required | 0 | Present in 1633 of 1633 records. |
| property_id | string (1633) | Stable cross-dataset property key. | Required | PROP-KOK-000001 | Present in 1633 of 1633 records. |

## loans

Path: `data/generated/loans.json`  
Purpose: Loan records for selected properties.  
Records: 294

| Field Name | Type | Description | Required / Optional | Example Value | Notes |
| --- | --- | --- | --- | --- | --- |
| loan_id | string (294) | Generated field: loan id. | Required | LOAN-KOK-000005 | Present in 294 of 294 records. |
| loan_type | string (294) | Generated field: loan type. | Required | home_loan | Present in 294 of 294 records. |
| outstanding_amount | integer (294) | Generated field: outstanding amount. | Required | 2425000 | Present in 294 of 294 records. |
| property_id | string (294) | Stable cross-dataset property key. | Required | PROP-KOK-000005 | Present in 294 of 294 records. |
| status | string (294) | Record status; documents use available, missing, or expired. | Required | active | Present in 294 of 294 records. |

## tax_records

Path: `data/generated/tax_records.json`  
Purpose: One current tax record per property.  
Records: 1633

| Field Name | Type | Description | Required / Optional | Example Value | Notes |
| --- | --- | --- | --- | --- | --- |
| pending_amount | integer (1633) | Generated field: pending amount. | Required | 0 | Present in 1633 of 1633 records. |
| property_id | string (1633) | Stable cross-dataset property key. | Required | PROP-KOK-000001 | Present in 1633 of 1633 records. |
| status | string (1633) | Record status; documents use available, missing, or expired. | Required | paid | Present in 1633 of 1633 records. |
| tax_id | string (1633) | Generated field: tax id. | Required | TAX-KOK-000001 | Present in 1633 of 1633 records. |

## court_disputes

Path: `data/generated/court_disputes.json`  
Purpose: Dispute records for selected properties.  
Records: 65

| Field Name | Type | Description | Required / Optional | Example Value | Notes |
| --- | --- | --- | --- | --- | --- |
| case_type | string (65) | Generated field: case type. | Required | sale_agreement_dispute | Present in 65 of 65 records. |
| dispute_id | string (65) | Generated field: dispute id. | Required | DISP-KOK-000005 | Present in 65 of 65 records. |
| property_id | string (65) | Stable cross-dataset property key. | Required | PROP-KOK-000005 | Present in 65 of 65 records. |
| status | string (65) | Record status; documents use available, missing, or expired. | Required | closed | Present in 65 of 65 records. |

## sale_deed

Path: `data/generated/documents/sale_deeds.json`  
Purpose: sale_deed legal document records.  
Records: 1633

| Field Name | Type | Description | Required / Optional | Example Value | Notes |
| --- | --- | --- | --- | --- | --- |
| buyer_name | string (1490), null (143) | Generated field: buyer name. | Required, nullable | Vikram Menon | Present in 1633 of 1633 records. |
| document_id | string (1633) | Legal document identifier. | Required | DOC-SALE-DEED-KOK-000001 | Present in 1633 of 1633 records. |
| document_number | string (1490), null (143) | Generated field: document number. | Required, nullable | SAL-KOK-000001 | Present in 1633 of 1633 records. |
| document_type | string (1633) | Generated field: document type. | Required | sale_deed | Present in 1633 of 1633 records. |
| issue_date | string (1490), null (143) | Generated field: issue date. | Required, nullable | 2012-07-26 | Present in 1633 of 1633 records. |
| issuing_authority | string (1633) | Generated field: issuing authority. | Required | Kokapet Sub-Registrar Office | Present in 1633 of 1633 records. |
| last_updated | string (1490), null (143) | Generated field: last updated. | Required, nullable | 2014-07-26 | Present in 1633 of 1633 records. |
| market_value | integer (1490), null (143) | Generated field: market value. | Required, nullable | 8943480 | Present in 1633 of 1633 records. |
| property_id | string (1633) | Stable cross-dataset property key. | Required | PROP-KOK-000001 | Present in 1633 of 1633 records. |
| registration_date | string (1490), null (143) | Generated field: registration date. | Required, nullable | 2012-07-11 | Present in 1633 of 1633 records. |
| registration_number | string (1490), null (143) | Generated field: registration number. | Required, nullable | REG-0000001 | Present in 1633 of 1633 records. |
| remarks | string (1633) | Generated field: remarks. | Required | Available in generated source packet | Present in 1633 of 1633 records. |
| seller_name | string (1490), null (143) | Generated field: seller name. | Required, nullable | Ananya Iyer | Present in 1633 of 1633 records. |
| status | string (1633) | Record status; documents use available, missing, or expired. | Required | available | Present in 1633 of 1633 records. |

## mother_deed

Path: `data/generated/documents/mother_deeds.json`  
Purpose: mother_deed legal document records.  
Records: 1633

| Field Name | Type | Description | Required / Optional | Example Value | Notes |
| --- | --- | --- | --- | --- | --- |
| document_id | string (1633) | Legal document identifier. | Required | DOC-MOTHER-DEED-KOK-000001 | Present in 1633 of 1633 records. |
| document_number | string (1509), null (124) | Generated field: document number. | Required, nullable | MOT-KOK-000001 | Present in 1633 of 1633 records. |
| document_type | string (1633) | Generated field: document type. | Required | mother_deed | Present in 1633 of 1633 records. |
| issue_date | string (1509), null (124) | Generated field: issue date. | Required, nullable | 2012-07-26 | Present in 1633 of 1633 records. |
| issuing_authority | string (1633) | Generated field: issuing authority. | Required | Kokapet Sub-Registrar Office | Present in 1633 of 1633 records. |
| last_updated | string (1509), null (124) | Generated field: last updated. | Required, nullable | 2014-07-26 | Present in 1633 of 1633 records. |
| origin_year | integer (1509), null (124) | Generated field: origin year. | Required, nullable | 2002 | Present in 1633 of 1633 records. |
| ownership_chain_length | integer (1509), null (124) | Generated field: ownership chain length. | Required, nullable | 2 | Present in 1633 of 1633 records. |
| parent_document_number | string (1509), null (124) | Generated field: parent document number. | Required, nullable | MD-PARENT-000001 | Present in 1633 of 1633 records. |
| property_id | string (1633) | Stable cross-dataset property key. | Required | PROP-KOK-000001 | Present in 1633 of 1633 records. |
| remarks | string (1633) | Generated field: remarks. | Required | Available in generated source packet | Present in 1633 of 1633 records. |
| status | string (1633) | Record status; documents use available, missing, or expired. | Required | available | Present in 1633 of 1633 records. |

## encumbrance_certificate

Path: `data/generated/documents/encumbrance_certificates.json`  
Purpose: encumbrance_certificate legal document records.  
Records: 1633

| Field Name | Type | Description | Required / Optional | Example Value | Notes |
| --- | --- | --- | --- | --- | --- |
| active_encumbrance | boolean (1561), null (72) | Generated field: active encumbrance. | Required, nullable | false | Present in 1633 of 1633 records. |
| document_id | string (1633) | Legal document identifier. | Required | DOC-ENCUMBRANCE-CERTIFICATE-KOK-000001 | Present in 1633 of 1633 records. |
| document_number | string (1561), null (72) | Generated field: document number. | Required, nullable | ENC-KOK-000001 | Present in 1633 of 1633 records. |
| document_type | string (1633) | Generated field: document type. | Required | encumbrance_certificate | Present in 1633 of 1633 records. |
| ec_period_from | string (1561), null (72) | Generated field: ec period from. | Required, nullable | 2007-07-13 | Present in 1633 of 1633 records. |
| ec_period_to | string (1561), null (72) | Generated field: ec period to. | Required, nullable | 2026-03-31 | Present in 1633 of 1633 records. |
| encumbrance_count | integer (1561), null (72) | Generated field: encumbrance count. | Required, nullable | 0 | Present in 1633 of 1633 records. |
| issue_date | string (1561), null (72) | Generated field: issue date. | Required, nullable | 2012-07-26 | Present in 1633 of 1633 records. |
| issuing_authority | string (1633) | Generated field: issuing authority. | Required | Kokapet Registration Department | Present in 1633 of 1633 records. |
| last_updated | string (1561), null (72) | Generated field: last updated. | Required, nullable | 2014-07-26 | Present in 1633 of 1633 records. |
| property_id | string (1633) | Stable cross-dataset property key. | Required | PROP-KOK-000001 | Present in 1633 of 1633 records. |
| remarks | string (1633) | Generated field: remarks. | Required | Available in generated source packet | Present in 1633 of 1633 records. |
| status | string (1633) | Record status; documents use available, missing, or expired. | Required | available | Present in 1633 of 1633 records. |

## property_tax_receipt

Path: `data/generated/documents/property_tax_receipts.json`  
Purpose: property_tax_receipt legal document records.  
Records: 1633

| Field Name | Type | Description | Required / Optional | Example Value | Notes |
| --- | --- | --- | --- | --- | --- |
| document_id | string (1633) | Legal document identifier. | Required | DOC-PROPERTY-TAX-RECEIPT-KOK-000001 | Present in 1633 of 1633 records. |
| document_number | string (1633) | Generated field: document number. | Required | PRO-KOK-000001 | Present in 1633 of 1633 records. |
| document_type | string (1633) | Generated field: document type. | Required | property_tax_receipt | Present in 1633 of 1633 records. |
| financial_year | string (1633) | Generated field: financial year. | Required | 2025-2026 | Present in 1633 of 1633 records. |
| issue_date | string (1633) | Generated field: issue date. | Required | 2012-07-26 | Present in 1633 of 1633 records. |
| issuing_authority | string (1633) | Generated field: issuing authority. | Required | Kokapet Municipal Revenue Office | Present in 1633 of 1633 records. |
| last_updated | string (1633) | Generated field: last updated. | Required | 2014-07-26 | Present in 1633 of 1633 records. |
| paid_amount | integer (1633) | Generated field: paid amount. | Required | 4953 | Present in 1633 of 1633 records. |
| pending_amount | integer (1633) | Generated field: pending amount. | Required | 0 | Present in 1633 of 1633 records. |
| property_id | string (1633) | Stable cross-dataset property key. | Required | PROP-KOK-000001 | Present in 1633 of 1633 records. |
| remarks | string (1633) | Generated field: remarks. | Required | Available in generated source packet | Present in 1633 of 1633 records. |
| status | string (1633) | Record status; documents use available, missing, or expired. | Required | available | Present in 1633 of 1633 records. |
| tax_amount | integer (1633) | Generated field: tax amount. | Required | 4953 | Present in 1633 of 1633 records. |

## mutation_record

Path: `data/generated/documents/mutation_records.json`  
Purpose: mutation_record legal document records.  
Records: 1633

| Field Name | Type | Description | Required / Optional | Example Value | Notes |
| --- | --- | --- | --- | --- | --- |
| document_id | string (1633) | Legal document identifier. | Required | DOC-MUTATION-RECORD-KOK-000001 | Present in 1633 of 1633 records. |
| document_number | string (1498), null (135) | Generated field: document number. | Required, nullable | MUT-KOK-000001 | Present in 1633 of 1633 records. |
| document_type | string (1633) | Generated field: document type. | Required | mutation_record | Present in 1633 of 1633 records. |
| issue_date | string (1498), null (135) | Generated field: issue date. | Required, nullable | 2012-07-26 | Present in 1633 of 1633 records. |
| issuing_authority | string (1633) | Generated field: issuing authority. | Required | Kokapet Revenue Department | Present in 1633 of 1633 records. |
| last_updated | string (1498), null (135) | Generated field: last updated. | Required, nullable | 2014-07-26 | Present in 1633 of 1633 records. |
| mutation_date | string (1498), null (135) | Generated field: mutation date. | Required, nullable | 2012-08-25 | Present in 1633 of 1633 records. |
| mutation_number | string (1498), null (135) | Generated field: mutation number. | Required, nullable | MUT-000001 | Present in 1633 of 1633 records. |
| property_id | string (1633) | Stable cross-dataset property key. | Required | PROP-KOK-000001 | Present in 1633 of 1633 records. |
| reason | string (1498), null (135) | Generated field: reason. | Required, nullable | sale | Present in 1633 of 1633 records. |
| remarks | string (1633) | Generated field: remarks. | Required | Document requires renewal or updated extract | Present in 1633 of 1633 records. |
| status | string (1633) | Record status; documents use available, missing, or expired. | Required | expired | Present in 1633 of 1633 records. |

## survey_map

Path: `data/generated/documents/survey_maps.json`  
Purpose: survey_map legal document records.  
Records: 1633

| Field Name | Type | Description | Required / Optional | Example Value | Notes |
| --- | --- | --- | --- | --- | --- |
| document_id | string (1633) | Legal document identifier. | Required | DOC-SURVEY-MAP-KOK-000001 | Present in 1633 of 1633 records. |
| document_number | string (1494), null (139) | Generated field: document number. | Required, nullable | SUR-KOK-000001 | Present in 1633 of 1633 records. |
| document_type | string (1633) | Generated field: document type. | Required | survey_map | Present in 1633 of 1633 records. |
| issue_date | string (1494), null (139) | Generated field: issue date. | Required, nullable | 2012-07-26 | Present in 1633 of 1633 records. |
| issuing_authority | string (1633) | Generated field: issuing authority. | Required | Kokapet Survey and Land Records Office | Present in 1633 of 1633 records. |
| last_updated | string (1494), null (139) | Generated field: last updated. | Required, nullable | 2014-07-26 | Present in 1633 of 1633 records. |
| plot_area_sqyd | number (1494), null (139) | Generated field: plot area sqyd. | Required, nullable | 171.99 | Present in 1633 of 1633 records. |
| property_id | string (1633) | Stable cross-dataset property key. | Required | PROP-KOK-000001 | Present in 1633 of 1633 records. |
| remarks | string (1633) | Generated field: remarks. | Required | Available in generated source packet | Present in 1633 of 1633 records. |
| status | string (1633) | Record status; documents use available, missing, or expired. | Required | available | Present in 1633 of 1633 records. |
| survey_date | string (1494), null (139) | Generated field: survey date. | Required, nullable | 2012-05-12 | Present in 1633 of 1633 records. |
| survey_number | string (1494), null (139) | Generated field: survey number. | Required, nullable | SY-KOK-0001 | Present in 1633 of 1633 records. |

## rtc_record

Path: `data/generated/documents/rtc_records.json`  
Purpose: rtc_record legal document records.  
Records: 1633

| Field Name | Type | Description | Required / Optional | Example Value | Notes |
| --- | --- | --- | --- | --- | --- |
| cultivation_status | string (1277), null (356) | Generated field: cultivation status. | Required, nullable | not_cultivated | Present in 1633 of 1633 records. |
| document_id | string (1633) | Legal document identifier. | Required | DOC-RTC-RECORD-KOK-000001 | Present in 1633 of 1633 records. |
| document_number | string (1277), null (356) | Generated field: document number. | Required, nullable | RTC-KOK-000001 | Present in 1633 of 1633 records. |
| document_type | string (1633) | Generated field: document type. | Required | rtc_record | Present in 1633 of 1633 records. |
| issue_date | string (1277), null (356) | Generated field: issue date. | Required, nullable | 2012-07-26 | Present in 1633 of 1633 records. |
| issuing_authority | string (1633) | Generated field: issuing authority. | Required | Kokapet Mandal Revenue Office | Present in 1633 of 1633 records. |
| land_type | string (1277), null (356) | Generated field: land type. | Required, nullable | dry | Present in 1633 of 1633 records. |
| last_updated | string (1277), null (356) | Generated field: last updated. | Required, nullable | 2014-07-26 | Present in 1633 of 1633 records. |
| property_id | string (1633) | Stable cross-dataset property key. | Required | PROP-KOK-000001 | Present in 1633 of 1633 records. |
| remarks | string (1633) | Generated field: remarks. | Required | Available in generated source packet | Present in 1633 of 1633 records. |
| status | string (1633) | Record status; documents use available, missing, or expired. | Required | available | Present in 1633 of 1633 records. |
| survey_number | string (1277), null (356) | Generated field: survey number. | Required, nullable | SY-KOK-0001 | Present in 1633 of 1633 records. |

## khata_certificate

Path: `data/generated/documents/khata_certificates.json`  
Purpose: khata_certificate legal document records.  
Records: 1633

| Field Name | Type | Description | Required / Optional | Example Value | Notes |
| --- | --- | --- | --- | --- | --- |
| document_id | string (1633) | Legal document identifier. | Required | DOC-KHATA-CERTIFICATE-KOK-000001 | Present in 1633 of 1633 records. |
| document_number | string (1488), null (145) | Generated field: document number. | Required, nullable | KHA-KOK-000001 | Present in 1633 of 1633 records. |
| document_type | string (1633) | Generated field: document type. | Required | khata_certificate | Present in 1633 of 1633 records. |
| issue_date | string (1488), null (145) | Generated field: issue date. | Required, nullable | 2012-07-26 | Present in 1633 of 1633 records. |
| issuing_authority | string (1633) | Generated field: issuing authority. | Required | Kokapet Panchayat Office | Present in 1633 of 1633 records. |
| khata_number | string (1488), null (145) | Generated field: khata number. | Required, nullable | KH-000001 | Present in 1633 of 1633 records. |
| last_updated | string (1488), null (145) | Generated field: last updated. | Required, nullable | 2014-07-26 | Present in 1633 of 1633 records. |
| owner_name | string (1488), null (145) | Generated field: owner name. | Required, nullable | Vikram Menon | Present in 1633 of 1633 records. |
| property_id | string (1633) | Stable cross-dataset property key. | Required | PROP-KOK-000001 | Present in 1633 of 1633 records. |
| remarks | string (1633) | Generated field: remarks. | Required | Available in generated source packet | Present in 1633 of 1633 records. |
| status | string (1633) | Record status; documents use available, missing, or expired. | Required | available | Present in 1633 of 1633 records. |

## khata_extract

Path: `data/generated/documents/khata_extracts.json`  
Purpose: khata_extract legal document records.  
Records: 1633

| Field Name | Type | Description | Required / Optional | Example Value | Notes |
| --- | --- | --- | --- | --- | --- |
| assessment_value | integer (1510), null (123) | Generated field: assessment value. | Required, nullable | 7223580 | Present in 1633 of 1633 records. |
| document_id | string (1633) | Legal document identifier. | Required | DOC-KHATA-EXTRACT-KOK-000001 | Present in 1633 of 1633 records. |
| document_number | string (1510), null (123) | Generated field: document number. | Required, nullable | KHA-KOK-000001 | Present in 1633 of 1633 records. |
| document_type | string (1633) | Generated field: document type. | Required | khata_extract | Present in 1633 of 1633 records. |
| issue_date | string (1510), null (123) | Generated field: issue date. | Required, nullable | 2012-07-26 | Present in 1633 of 1633 records. |
| issuing_authority | string (1633) | Generated field: issuing authority. | Required | Kokapet Panchayat Office | Present in 1633 of 1633 records. |
| khata_number | string (1510), null (123) | Generated field: khata number. | Required, nullable | KH-000001 | Present in 1633 of 1633 records. |
| last_updated | string (1510), null (123) | Generated field: last updated. | Required, nullable | 2014-07-26 | Present in 1633 of 1633 records. |
| property_id | string (1633) | Stable cross-dataset property key. | Required | PROP-KOK-000001 | Present in 1633 of 1633 records. |
| remarks | string (1633) | Generated field: remarks. | Required | Available in generated source packet | Present in 1633 of 1633 records. |
| status | string (1633) | Record status; documents use available, missing, or expired. | Required | available | Present in 1633 of 1633 records. |

## building_approval_plan

Path: `data/generated/documents/building_approval_plans.json`  
Purpose: building_approval_plan legal document records.  
Records: 1633

| Field Name | Type | Description | Required / Optional | Example Value | Notes |
| --- | --- | --- | --- | --- | --- |
| approval_date | null (725), string (908) | Generated field: approval date. | Required, nullable | 2010-03-22 | Present in 1633 of 1633 records. |
| approval_number | null (725), string (908) | Generated field: approval number. | Required, nullable | BAP-000002 | Present in 1633 of 1633 records. |
| approved_floors | null (725), integer (908) | Generated field: approved floors. | Required, nullable | 1 | Present in 1633 of 1633 records. |
| document_id | string (1633) | Legal document identifier. | Required | DOC-BUILDING-APPROVAL-PLAN-KOK-000001 | Present in 1633 of 1633 records. |
| document_number | null (725), string (908) | Generated field: document number. | Required, nullable | BUI-KOK-000002 | Present in 1633 of 1633 records. |
| document_type | string (1633) | Generated field: document type. | Required | building_approval_plan | Present in 1633 of 1633 records. |
| issue_date | null (725), string (908) | Generated field: issue date. | Required, nullable | 2010-01-07 | Present in 1633 of 1633 records. |
| issuing_authority | string (1633) | Generated field: issuing authority. | Required | Kokapet Planning Authority | Present in 1633 of 1633 records. |
| last_updated | null (725), string (908) | Generated field: last updated. | Required, nullable | 2013-01-06 | Present in 1633 of 1633 records. |
| property_id | string (1633) | Stable cross-dataset property key. | Required | PROP-KOK-000001 | Present in 1633 of 1633 records. |
| remarks | string (1633) | Generated field: remarks. | Required | Document not available in source packet | Present in 1633 of 1633 records. |
| status | string (1633) | Record status; documents use available, missing, or expired. | Required | missing | Present in 1633 of 1633 records. |

## layout_approval

Path: `data/generated/documents/layout_approvals.json`  
Purpose: layout_approval legal document records.  
Records: 1633

| Field Name | Type | Description | Required / Optional | Example Value | Notes |
| --- | --- | --- | --- | --- | --- |
| approval_date | string (1295), null (338) | Generated field: approval date. | Required, nullable | 2012-09-24 | Present in 1633 of 1633 records. |
| approved_by | string (1295), null (338) | Generated field: approved by. | Required, nullable | Kokapet Planning Authority | Present in 1633 of 1633 records. |
| document_id | string (1633) | Legal document identifier. | Required | DOC-LAYOUT-APPROVAL-KOK-000001 | Present in 1633 of 1633 records. |
| document_number | string (1295), null (338) | Generated field: document number. | Required, nullable | LAY-KOK-000001 | Present in 1633 of 1633 records. |
| document_type | string (1633) | Generated field: document type. | Required | layout_approval | Present in 1633 of 1633 records. |
| issue_date | string (1295), null (338) | Generated field: issue date. | Required, nullable | 2012-07-26 | Present in 1633 of 1633 records. |
| issuing_authority | string (1633) | Generated field: issuing authority. | Required | Kokapet Urban Development Authority | Present in 1633 of 1633 records. |
| last_updated | string (1295), null (338) | Generated field: last updated. | Required, nullable | 2014-07-26 | Present in 1633 of 1633 records. |
| layout_number | string (1295), null (338) | Generated field: layout number. | Required, nullable | LAY-000001 | Present in 1633 of 1633 records. |
| property_id | string (1633) | Stable cross-dataset property key. | Required | PROP-KOK-000001 | Present in 1633 of 1633 records. |
| remarks | string (1633) | Generated field: remarks. | Required | Available in generated source packet | Present in 1633 of 1633 records. |
| status | string (1633) | Record status; documents use available, missing, or expired. | Required | available | Present in 1633 of 1633 records. |

## land_conversion_certificate

Path: `data/generated/documents/land_conversion_certificates.json`  
Purpose: land_conversion_certificate legal document records.  
Records: 1633

| Field Name | Type | Description | Required / Optional | Example Value | Notes |
| --- | --- | --- | --- | --- | --- |
| conversion_date | string (1294), null (339) | Generated field: conversion date. | Required, nullable | 2012-03-13 | Present in 1633 of 1633 records. |
| conversion_type | string (1294), null (339) | Generated field: conversion type. | Required, nullable | agricultural_to_residential | Present in 1633 of 1633 records. |
| document_id | string (1633) | Legal document identifier. | Required | DOC-LAND-CONVERSION-CERTIFICATE-KOK-000001 | Present in 1633 of 1633 records. |
| document_number | string (1294), null (339) | Generated field: document number. | Required, nullable | LAN-KOK-000001 | Present in 1633 of 1633 records. |
| document_type | string (1633) | Generated field: document type. | Required | land_conversion_certificate | Present in 1633 of 1633 records. |
| issue_date | string (1294), null (339) | Generated field: issue date. | Required, nullable | 2012-07-26 | Present in 1633 of 1633 records. |
| issuing_authority | string (1633) | Generated field: issuing authority. | Required | Telangana Revenue Department | Present in 1633 of 1633 records. |
| last_updated | string (1294), null (339) | Generated field: last updated. | Required, nullable | 2014-07-26 | Present in 1633 of 1633 records. |
| property_id | string (1633) | Stable cross-dataset property key. | Required | PROP-KOK-000001 | Present in 1633 of 1633 records. |
| remarks | string (1633) | Generated field: remarks. | Required | Available in generated source packet | Present in 1633 of 1633 records. |
| status | string (1633) | Record status; documents use available, missing, or expired. | Required | available | Present in 1633 of 1633 records. |

## occupancy_certificate

Path: `data/generated/documents/occupancy_certificates.json`  
Purpose: occupancy_certificate legal document records.  
Records: 1633

| Field Name | Type | Description | Required / Optional | Example Value | Notes |
| --- | --- | --- | --- | --- | --- |
| building_type | null (727), string (906) | Generated field: building type. | Required, nullable | residential_plot | Present in 1633 of 1633 records. |
| document_id | string (1633) | Legal document identifier. | Required | DOC-OCCUPANCY-CERTIFICATE-KOK-000001 | Present in 1633 of 1633 records. |
| document_number | null (727), string (906) | Generated field: document number. | Required, nullable | OCC-KOK-000002 | Present in 1633 of 1633 records. |
| document_type | string (1633) | Generated field: document type. | Required | occupancy_certificate | Present in 1633 of 1633 records. |
| issue_date | null (727), string (906) | Generated field: issue date. | Required, nullable | 2010-01-07 | Present in 1633 of 1633 records. |
| issuing_authority | string (1633) | Generated field: issuing authority. | Required | Kokapet Building Permissions Office | Present in 1633 of 1633 records. |
| last_updated | null (727), string (906) | Generated field: last updated. | Required, nullable | 2013-01-06 | Present in 1633 of 1633 records. |
| occupancy_date | null (727), string (906) | Generated field: occupancy date. | Required, nullable | 2010-12-22 | Present in 1633 of 1633 records. |
| property_id | string (1633) | Stable cross-dataset property key. | Required | PROP-KOK-000001 | Present in 1633 of 1633 records. |
| remarks | string (1633) | Generated field: remarks. | Required | Document not available in source packet | Present in 1633 of 1633 records. |
| status | string (1633) | Record status; documents use available, missing, or expired. | Required | missing | Present in 1633 of 1633 records. |

## completion_certificate

Path: `data/generated/documents/completion_certificates.json`  
Purpose: completion_certificate legal document records.  
Records: 1633

| Field Name | Type | Description | Required / Optional | Example Value | Notes |
| --- | --- | --- | --- | --- | --- |
| approved_structure | null (725), string (908) | Generated field: approved structure. | Required, nullable | residential_plot | Present in 1633 of 1633 records. |
| completion_date | null (725), string (908) | Generated field: completion date. | Required, nullable | 2010-11-17 | Present in 1633 of 1633 records. |
| document_id | string (1633) | Legal document identifier. | Required | DOC-COMPLETION-CERTIFICATE-KOK-000001 | Present in 1633 of 1633 records. |
| document_number | null (725), string (908) | Generated field: document number. | Required, nullable | COM-KOK-000002 | Present in 1633 of 1633 records. |
| document_type | string (1633) | Generated field: document type. | Required | completion_certificate | Present in 1633 of 1633 records. |
| issue_date | null (725), string (908) | Generated field: issue date. | Required, nullable | 2010-01-07 | Present in 1633 of 1633 records. |
| issuing_authority | string (1633) | Generated field: issuing authority. | Required | Kokapet Building Permissions Office | Present in 1633 of 1633 records. |
| last_updated | null (725), string (908) | Generated field: last updated. | Required, nullable | 2013-01-06 | Present in 1633 of 1633 records. |
| property_id | string (1633) | Stable cross-dataset property key. | Required | PROP-KOK-000001 | Present in 1633 of 1633 records. |
| remarks | string (1633) | Generated field: remarks. | Required | Document not available in source packet | Present in 1633 of 1633 records. |
| status | string (1633) | Record status; documents use available, missing, or expired. | Required | missing | Present in 1633 of 1633 records. |

## noc

Path: `data/generated/documents/nocs.json`  
Purpose: noc legal document records.  
Records: 1633

| Field Name | Type | Description | Required / Optional | Example Value | Notes |
| --- | --- | --- | --- | --- | --- |
| document_id | string (1633) | Legal document identifier. | Required | DOC-NOC-KOK-000001 | Present in 1633 of 1633 records. |
| document_number | null (741), string (892) | Generated field: document number. | Required, nullable | NOC-KOK-000002 | Present in 1633 of 1633 records. |
| document_type | string (1633) | Generated field: document type. | Required | noc | Present in 1633 of 1633 records. |
| issue_date | null (741), string (892) | Generated field: issue date. | Required, nullable | 2010-01-07 | Present in 1633 of 1633 records. |
| issuing_authority | string (1633) | Generated field: issuing authority. | Required | Kokapet Fire and Civic NOC Cell | Present in 1633 of 1633 records. |
| issuing_department | null (741), string (892) | Generated field: issuing department. | Required, nullable | Fire and Civic Services | Present in 1633 of 1633 records. |
| last_updated | null (741), string (892) | Generated field: last updated. | Required, nullable | 2013-01-06 | Present in 1633 of 1633 records. |
| property_id | string (1633) | Stable cross-dataset property key. | Required | PROP-KOK-000001 | Present in 1633 of 1633 records. |
| remarks | string (1633) | Generated field: remarks. | Required | Document not available in source packet | Present in 1633 of 1633 records. |
| status | string (1633) | Record status; documents use available, missing, or expired. | Required | missing | Present in 1633 of 1633 records. |
| valid_until | null (741), string (892) | Generated field: valid until. | Required, nullable | 2028-03-31 | Present in 1633 of 1633 records. |

## identity_proof

Path: `data/generated/documents/identity_proofs.json`  
Purpose: identity_proof legal document records.  
Records: 1633

| Field Name | Type | Description | Required / Optional | Example Value | Notes |
| --- | --- | --- | --- | --- | --- |
| document_id | string (1633) | Legal document identifier. | Required | DOC-IDENTITY-PROOF-KOK-000001 | Present in 1633 of 1633 records. |
| document_number | string (1633) | Generated field: document number. | Required | IDE-KOK-000001 | Present in 1633 of 1633 records. |
| document_type | string (1633) | Generated field: document type. | Required | identity_proof | Present in 1633 of 1633 records. |
| issue_date | string (1633) | Generated field: issue date. | Required | 2012-07-26 | Present in 1633 of 1633 records. |
| issuing_authority | string (1633) | Generated field: issuing authority. | Required | Government Identity Authority | Present in 1633 of 1633 records. |
| last_updated | string (1633) | Generated field: last updated. | Required | 2014-07-26 | Present in 1633 of 1633 records. |
| owner_id | string (1633) | Current owner identifier. | Required | OWN-KOK-000001 | Present in 1633 of 1633 records. |
| proof_last4 | string (1633) | Generated field: proof last4. | Required | 3571 | Present in 1633 of 1633 records. |
| proof_type | string (1633) | Generated field: proof type. | Required | aadhaar | Present in 1633 of 1633 records. |
| property_id | string (1633) | Stable cross-dataset property key. | Required | PROP-KOK-000001 | Present in 1633 of 1633 records. |
| remarks | string (1633) | Generated field: remarks. | Required | Available in generated source packet | Present in 1633 of 1633 records. |
| status | string (1633) | Record status; documents use available, missing, or expired. | Required | available | Present in 1633 of 1633 records. |

## power_of_attorney

Path: `data/generated/documents/power_of_attorneys.json`  
Purpose: power_of_attorney legal document records.  
Records: 1633

| Field Name | Type | Description | Required / Optional | Example Value | Notes |
| --- | --- | --- | --- | --- | --- |
| agent_name | string (871), null (762) | Generated field: agent name. | Required, nullable | Kiran Kumar | Present in 1633 of 1633 records. |
| document_id | string (1633) | Legal document identifier. | Required | DOC-POWER-OF-ATTORNEY-KOK-000001 | Present in 1633 of 1633 records. |
| document_number | string (871), null (762) | Generated field: document number. | Required, nullable | POW-KOK-000001 | Present in 1633 of 1633 records. |
| document_type | string (1633) | Generated field: document type. | Required | power_of_attorney | Present in 1633 of 1633 records. |
| issue_date | string (871), null (762) | Generated field: issue date. | Required, nullable | 2012-07-26 | Present in 1633 of 1633 records. |
| issuing_authority | string (1633) | Generated field: issuing authority. | Required | Kokapet Notary and Registration Office | Present in 1633 of 1633 records. |
| last_updated | string (871), null (762) | Generated field: last updated. | Required, nullable | 2014-07-26 | Present in 1633 of 1633 records. |
| principal_name | string (871), null (762) | Generated field: principal name. | Required, nullable | Vikram Menon | Present in 1633 of 1633 records. |
| property_id | string (1633) | Stable cross-dataset property key. | Required | PROP-KOK-000001 | Present in 1633 of 1633 records. |
| remarks | string (1633) | Generated field: remarks. | Required | Available in generated source packet | Present in 1633 of 1633 records. |
| status | string (1633) | Record status; documents use available, missing, or expired. | Required | available | Present in 1633 of 1633 records. |
| valid_until | string (871), null (762) | Generated field: valid until. | Required, nullable | 2027-12-31 | Present in 1633 of 1633 records. |

## court_dispute_record

Path: `data/generated/documents/court_dispute_records.json`  
Purpose: court_dispute_record legal document records.  
Records: 1633

| Field Name | Type | Description | Required / Optional | Example Value | Notes |
| --- | --- | --- | --- | --- | --- |
| case_number | null (883), string (750) | Generated field: case number. | Required, nullable | NIL-000002 | Present in 1633 of 1633 records. |
| case_status | null (883), string (750) | Generated field: case status. | Required, nullable | no_case | Present in 1633 of 1633 records. |
| case_type | null (883), string (750) | Generated field: case type. | Required, nullable | none | Present in 1633 of 1633 records. |
| court_name | null (883), string (750) | Generated field: court name. | Required, nullable | Kokapet Civil Court | Present in 1633 of 1633 records. |
| document_id | string (1633) | Legal document identifier. | Required | DOC-COURT-DISPUTE-RECORD-KOK-000001 | Present in 1633 of 1633 records. |
| document_number | null (883), string (750) | Generated field: document number. | Required, nullable | COU-KOK-000002 | Present in 1633 of 1633 records. |
| document_type | string (1633) | Generated field: document type. | Required | court_dispute_record | Present in 1633 of 1633 records. |
| issue_date | null (883), string (750) | Generated field: issue date. | Required, nullable | 2010-01-07 | Present in 1633 of 1633 records. |
| issuing_authority | string (1633) | Generated field: issuing authority. | Required | Kokapet Civil Court | Present in 1633 of 1633 records. |
| last_updated | null (883), string (750) | Generated field: last updated. | Required, nullable | 2013-01-06 | Present in 1633 of 1633 records. |
| property_id | string (1633) | Stable cross-dataset property key. | Required | PROP-KOK-000001 | Present in 1633 of 1633 records. |
| remarks | string (1633) | Generated field: remarks. | Required | Document not available in source packet | Present in 1633 of 1633 records. |
| status | string (1633) | Record status; documents use available, missing, or expired. | Required | missing | Present in 1633 of 1633 records. |

## documents_all

Path: `data/generated/documents/documents_all.json`  
Purpose: Merged legal document collection.  
Records: 29394

| Field Name | Type | Description | Required / Optional | Example Value | Notes |
| --- | --- | --- | --- | --- | --- |
| active_encumbrance | boolean (1561), null (72) | Generated field: active encumbrance. | Optional | false | Present in 1633 of 29394 records. |
| agent_name | string (871), null (762) | Generated field: agent name. | Optional | Kiran Kumar | Present in 1633 of 29394 records. |
| approval_date | null (1063), string (2203) | Generated field: approval date. | Optional | 2012-09-24 | Present in 3266 of 29394 records. |
| approval_number | null (725), string (908) | Generated field: approval number. | Optional | BAP-000002 | Present in 1633 of 29394 records. |
| approved_by | string (1295), null (338) | Generated field: approved by. | Optional | Kokapet Planning Authority | Present in 1633 of 29394 records. |
| approved_floors | null (725), integer (908) | Generated field: approved floors. | Optional | 1 | Present in 1633 of 29394 records. |
| approved_structure | null (725), string (908) | Generated field: approved structure. | Optional | residential_plot | Present in 1633 of 29394 records. |
| assessment_value | integer (1510), null (123) | Generated field: assessment value. | Optional | 7223580 | Present in 1633 of 29394 records. |
| building_type | null (727), string (906) | Generated field: building type. | Optional | residential_plot | Present in 1633 of 29394 records. |
| buyer_name | string (1490), null (143) | Generated field: buyer name. | Optional | Vikram Menon | Present in 1633 of 29394 records. |
| case_number | null (883), string (750) | Generated field: case number. | Optional | NIL-000002 | Present in 1633 of 29394 records. |
| case_status | null (883), string (750) | Generated field: case status. | Optional | no_case | Present in 1633 of 29394 records. |
| case_type | null (883), string (750) | Generated field: case type. | Optional | none | Present in 1633 of 29394 records. |
| completion_date | null (725), string (908) | Generated field: completion date. | Optional | 2010-11-17 | Present in 1633 of 29394 records. |
| conversion_date | string (1294), null (339) | Generated field: conversion date. | Optional | 2012-03-13 | Present in 1633 of 29394 records. |
| conversion_type | string (1294), null (339) | Generated field: conversion type. | Optional | agricultural_to_residential | Present in 1633 of 29394 records. |
| court_name | null (883), string (750) | Generated field: court name. | Optional | Kokapet Civil Court | Present in 1633 of 29394 records. |
| cultivation_status | string (1277), null (356) | Generated field: cultivation status. | Optional | not_cultivated | Present in 1633 of 29394 records. |
| document_id | string (29394) | Legal document identifier. | Required | DOC-SALE-DEED-KOK-000001 | Present in 29394 of 29394 records. |
| document_number | string (22917), null (6477) | Generated field: document number. | Required, nullable | SAL-KOK-000001 | Present in 29394 of 29394 records. |
| document_type | string (29394) | Generated field: document type. | Required | sale_deed | Present in 29394 of 29394 records. |
| ec_period_from | string (1561), null (72) | Generated field: ec period from. | Optional | 2007-07-13 | Present in 1633 of 29394 records. |
| ec_period_to | string (1561), null (72) | Generated field: ec period to. | Optional | 2026-03-31 | Present in 1633 of 29394 records. |
| encumbrance_count | integer (1561), null (72) | Generated field: encumbrance count. | Optional | 0 | Present in 1633 of 29394 records. |
| financial_year | string (1633) | Generated field: financial year. | Optional | 2025-2026 | Present in 1633 of 29394 records. |
| issue_date | string (22917), null (6477) | Generated field: issue date. | Required, nullable | 2012-07-26 | Present in 29394 of 29394 records. |
| issuing_authority | string (29394) | Generated field: issuing authority. | Required | Kokapet Sub-Registrar Office | Present in 29394 of 29394 records. |
| issuing_department | null (741), string (892) | Generated field: issuing department. | Optional | Fire and Civic Services | Present in 1633 of 29394 records. |
| khata_number | string (2998), null (268) | Generated field: khata number. | Optional | KH-000001 | Present in 3266 of 29394 records. |
| land_type | string (1277), null (356) | Generated field: land type. | Optional | dry | Present in 1633 of 29394 records. |
| last_updated | string (22917), null (6477) | Generated field: last updated. | Required, nullable | 2014-07-26 | Present in 29394 of 29394 records. |
| layout_number | string (1295), null (338) | Generated field: layout number. | Optional | LAY-000001 | Present in 1633 of 29394 records. |
| market_value | integer (1490), null (143) | Generated field: market value. | Optional | 8943480 | Present in 1633 of 29394 records. |
| mutation_date | string (1498), null (135) | Generated field: mutation date. | Optional | 2012-08-25 | Present in 1633 of 29394 records. |
| mutation_number | string (1498), null (135) | Generated field: mutation number. | Optional | MUT-000001 | Present in 1633 of 29394 records. |
| occupancy_date | null (727), string (906) | Generated field: occupancy date. | Optional | 2010-12-22 | Present in 1633 of 29394 records. |
| origin_year | integer (1509), null (124) | Generated field: origin year. | Optional | 2002 | Present in 1633 of 29394 records. |
| owner_id | string (1633) | Current owner identifier. | Optional | OWN-KOK-000001 | Present in 1633 of 29394 records. |
| owner_name | string (1488), null (145) | Generated field: owner name. | Optional | Vikram Menon | Present in 1633 of 29394 records. |
| ownership_chain_length | integer (1509), null (124) | Generated field: ownership chain length. | Optional | 2 | Present in 1633 of 29394 records. |
| paid_amount | integer (1633) | Generated field: paid amount. | Optional | 4953 | Present in 1633 of 29394 records. |
| parent_document_number | string (1509), null (124) | Generated field: parent document number. | Optional | MD-PARENT-000001 | Present in 1633 of 29394 records. |
| pending_amount | integer (1633) | Generated field: pending amount. | Optional | 0 | Present in 1633 of 29394 records. |
| plot_area_sqyd | number (1494), null (139) | Generated field: plot area sqyd. | Optional | 171.99 | Present in 1633 of 29394 records. |
| principal_name | string (871), null (762) | Generated field: principal name. | Optional | Vikram Menon | Present in 1633 of 29394 records. |
| proof_last4 | string (1633) | Generated field: proof last4. | Optional | 3571 | Present in 1633 of 29394 records. |
| proof_type | string (1633) | Generated field: proof type. | Optional | aadhaar | Present in 1633 of 29394 records. |
| property_id | string (29394) | Stable cross-dataset property key. | Required | PROP-KOK-000001 | Present in 29394 of 29394 records. |
| reason | string (1498), null (135) | Generated field: reason. | Optional | sale | Present in 1633 of 29394 records. |
| registration_date | string (1490), null (143) | Generated field: registration date. | Optional | 2012-07-11 | Present in 1633 of 29394 records. |
| registration_number | string (1490), null (143) | Generated field: registration number. | Optional | REG-0000001 | Present in 1633 of 29394 records. |
| remarks | string (29394) | Generated field: remarks. | Required | Available in generated source packet | Present in 29394 of 29394 records. |
| seller_name | string (1490), null (143) | Generated field: seller name. | Optional | Ananya Iyer | Present in 1633 of 29394 records. |
| status | string (29394) | Record status; documents use available, missing, or expired. | Required | available | Present in 29394 of 29394 records. |
| survey_date | string (1494), null (139) | Generated field: survey date. | Optional | 2012-05-12 | Present in 1633 of 29394 records. |
| survey_number | string (2771), null (495) | Generated field: survey number. | Optional | SY-KOK-0001 | Present in 3266 of 29394 records. |
| tax_amount | integer (1633) | Generated field: tax amount. | Optional | 4953 | Present in 1633 of 29394 records. |
| valid_until | null (1503), string (1763) | Generated field: valid until. | Optional | 2027-12-31 | Present in 3266 of 29394 records. |

## Future Improvements (Not Implemented)

Convert this Markdown reference into formal JSON Schema contracts when downstream repositories need enforcement.
