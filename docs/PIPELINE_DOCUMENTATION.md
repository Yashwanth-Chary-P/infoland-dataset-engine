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

Purpose: generate profile attributes, synthetic POIs, sale status, location scores, and score distributions.

## Phase 3: Ownership and Legal Dataset Generation

Inputs: master properties, property profiles, synthetic POIs.

Scripts: `scripts/run_business_dataset_generation.py`, `scripts/synthesis/generate_business_datasets.py`.

Outputs: owners, events, registry, metadata, timeline, health, loans, taxes, disputes, 18 document datasets, `documents_all.json`, and reports.

Purpose: build the business/legal/financial dataset ecosystem.

## Phase 4: Validation and Statistics

Inputs: generated datasets.

Outputs: consistency, coverage, dataset summary, document stats, property stats, owner stats, loan stats, tax stats, dispute stats, MongoDB import summary, schema catalog, document samples.

Validation status: `passed`.

## Future Improvements (Not Implemented)

Add checksum validation and a formal release process.
