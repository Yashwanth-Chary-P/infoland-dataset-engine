# Statistics Summary

Dataset Engine v1 freeze — regenerated after institutional refinement.

## Geographic

| Metric | Value |
| --- | --- |
| total_properties | 1633 |
| average_area_sq_m | 198.76 |
| median_area_sq_m | 148.87 |

### Region Distribution

| Region | Count | Density share |
| --- | --- | --- |
| kokapet | 806 | 0.4936 |
| mokila | 592 | 0.3625 |
| shankarpally | 235 | 0.1439 |

### Coordinate Bounds

| Bound | Value |
| --- | --- |
| min_lat | 17.3845736 |
| max_lat | 17.4547757 |
| min_lon | 78.1265175 |
| max_lon | 78.343193 |

## Property Classes

| Value | Count |
| --- | --- |
| residential_plot | 1234 |
| villa | 153 |
| apartment | 50 |
| commercial | 68 |
| school | 19 |
| hospital | 13 |
| clinic | 8 |
| government | 10 |
| community_center | 13 |
| religious | 8 |
| park | 28 |
| industrial | 7 |
| vacant_land | 22 |

## Sale Status

| Value | Count |
| --- | --- |
| for_sale | 313 |
| not_for_sale | 1320 |

## Verification Workflow

| Value | Count |
| --- | --- |
| complete_property_verification | 1505 |
| institutional_property | 128 |

## Ownership

| Metric | Value |
| --- | --- |
| individual owners | 1354 |
| organization owners | 269 |
| government owners | 10 |

### Ownership Chain Length

| Transfers | Properties |
| --- | --- |
| 1 | 543 |
| 2 | 620 |
| 3 | 327 |
| 4 | 114 |
| 5 | 29 |

## Documents

Total documents: 29394 (18 records per property).

| Status | Count |
| --- | --- |
| available | 20405 |
| expired | 1353 |
| missing | 7636 |

## Loans

| Metric | Value |
| --- | --- |
| total_loans | 294 |
| properties_with_loans | 294 |
| active | 160 |
| closed | 134 |
| home_loan | 282 |
| commercial_mortgage | 12 |
| active_outstanding_amount_total | 632600000 |

## Taxes

| Metric | Value |
| --- | --- |
| total_tax_records | 1633 |
| paid | 1404 |
| pending | 229 |
| pending_amount_total | 2919562 |

## Disputes

| Metric | Value |
| --- | --- |
| total_disputes | 65 |
| properties_with_disputes | 65 |
| active | 46 |
| closed | 19 |

## Institutional Summary

| Metric | Value |
| --- | --- |
| institutional_properties | 128 |
| institutional_available_documents | 614 |
| institutional_missing_documents | 1673 |

## POI Markers

| poi_type | Count |
| --- | --- |
| school | 18 |
| hospital | 12 |
| park | 25 |
| commercial_hub | 20 |
| government_office | 8 |
| community_center | 12 |

All 95 POIs are anchored to existing building centroids via `property_id`.

## Dataset Health

| Metric | Value |
| --- | --- |
| clean_properties | 730 |
| minor_issues | 527 |
| moderate_issues | 226 |
| high_risk_candidates | 150 |
| validation_success_rate | 1.0 |
| consistency_score | 1.0 |
| coverage_score | 0.7402 |

## Validation Results

All consistency metrics: 0 errors. Status: `passed`.
