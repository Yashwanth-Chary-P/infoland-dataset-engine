# Pipeline Documentation

## Phase 1: Geographic Preprocessing

Inputs: `data/raw/*.geojson`, fallback `data/geojson/*.geojson`, `config/region_config.json`, `config/classification_rules.json`.

Scripts: `scripts/run_preprocessing.py` and `scripts/preprocessing/*`.

Outputs: `data/cleaned/*_clean.geojson`, `data/master/master_properties.json`, `data/master/property_candidates.json`, `data/master/master_properties.csv`, `data/poi/*.json`, and preprocessing reports.

Purpose: inspect, validate, repair, deduplicate, classify, enrich, extract POIs, and create the canonical master dataset.

## Phase 2: Property Synthesis

Inputs: `data/master/master_properties.json`.

Scripts: `scripts/run_synthesis.py`, `scripts/synthesis/generate_synthesis.py`.

Outputs: `property_profiles.json`, `synthetic_pois.json`, `location_scores.json`, `synthesis_stats.json`.

Purpose: generate profile attributes, building-anchored POI markers, sale status, verification workflow assignment, location scores, and score distributions.

POI generation policy (v1 freeze): each map marker is placed at the centroid of an existing classified building polygon. POIs reference `property_id` and never use random coordinates, road offsets, or vacant-land placement.

Property classification policy: `feature_category` from preprocessing is mapped directly where possible (apartments, commercial, school, hospital, government, park, religious, community). Remaining `property_candidate` parcels receive quota-based `property_class` assignment including institutional types.

## Phase 3: Ownership and Legal Dataset Generation

Inputs: master properties, property profiles, synthetic POIs.

Scripts: `scripts/run_business_dataset_generation.py`, `scripts/synthesis/generate_business_datasets.py`.

Outputs: owners, events, registry, metadata, timeline, health, loans, taxes, disputes, 18 document datasets, `documents_all.json`, and reports.

Purpose: build the business/legal/financial dataset ecosystem.

Verification workflow policy:
- `complete_property_verification` for residential_plot, villa, apartment, commercial
- `institutional_property` for school, hospital, clinic, government, community_center, religious, park, industrial, vacant_land

Institutional properties receive organization or government owners, simplified ownership chains, type-specific legal document packets, and no residential home loans or court disputes.

## Phase 4: Validation and Statistics

Inputs: generated datasets.

Outputs: consistency, coverage, dataset summary, document stats, property stats, owner stats, loan stats, tax stats, dispute stats, MongoDB import summary, schema catalog, document samples.

Validation status: `passed`.

## Future Improvements (Not Implemented)

Add checksum validation and a formal release process.
