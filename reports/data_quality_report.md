# Data Quality Audit Report

**Total Records:** 1000 | **Total Columns:** 18

## 1. Field Completeness & Cardinality
| Feature | Completeness (%) | Unique Values (Cardinality) |
| :--- | :--- | :--- |
| `id_datalake` | 100.0% | 1000 |
| `nct_id` | 100.0% | 1000 |
| `brief_title` | 100.0% | 1000 |
| `official_title` | 99.4% | 994 |
| `phase` | 96.0% | 7 |
| `recruitment_status` | 100.0% | 9 |
| `start_date` | 99.5% | 693 |
| `completion_date` | 94.8% | 600 |
| `primary_completion_date` | 94.9% | 610 |
| `enrollment` | 97.4% | 253 |
| `enrollment_type` | 95.6% | 2 |
| `indications` | 100.0% | 463 |
| `interventions_drugs` | 100.0% | 948 |
| `drugs_datalake` | 100.0% | 846 |
| `main_technologies` | 100.0% | 194 |
| `specific_technologies` | 100.0% | 227 |
| `target_names` | 100.0% | 663 |
| `target_abbreviations` | 100.0% | 687 |

## 2. Structural Anomalies Detected
- **Duplicate `nct_id` records:** 0
- **Newline/Truncation errors in `recruitment_status`:** 0

> *Note: These anomalies mandate a strict string-normalization and deduplication layer before analytical metrics can be reliably computed.*
