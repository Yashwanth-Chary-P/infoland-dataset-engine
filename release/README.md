# InfoLand AI Dataset Engine — Release v1

Frozen dataset package generated on 2026-06-26.

This `release/` folder is the canonical handoff artifact for:

1. Frontend dataset validation
2. MongoDB Atlas import
3. FastAPI / backend development
4. Future AI context

## Contents

| Path | Description |
| --- | --- |
| `generated/` | Final JSON datasets (properties, profiles, POIs, owners, legal, financial) |
| `generated/documents/` | 18 document type datasets + `documents_all.json` |
| `reports/` | Validation, statistics, coverage, and schema reports |
| `reports/document_samples/` | Sample records per document type |
| `*.md` | Documentation knowledge base |

## Key Refinements in v1

- Property classification extended to 13 `property_class` values
- POI markers anchored to building centroids via `property_id`
- Institutional properties use simplified legal and ownership workflows
- Residential/commercial properties retain full verification workflow
- All consistency validations passed

## Regeneration

To regenerate from source (outside this frozen package):

```bash
pip install -r requirements.txt
python scripts/run_preprocessing.py
python scripts/run_synthesis.py
python scripts/run_business_dataset_generation.py
```

See `DEVELOPER_HANDOFF.md` for full instructions.
