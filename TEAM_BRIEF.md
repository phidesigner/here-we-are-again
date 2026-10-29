# Team brief: Opioid overdose prediction

> **Status: Provisional teaching-run artifact.** Reconcile with `README.md` before merging into `dev` in a real student workflow

**Business case:** `README.md`, `## 1. Business case` (not supplied in this trial; source-of-truth check pending)
**Use case:** Identify people at risk of opioid overdose for additional review (provisional until checked against README)
**Notebook:** `opiod_analysis_v01(2).ipynb`; source: `CaseStudy_training_data.xlsx`, `Model_data` sheet
**Data:** 1,000 rows, 22 columns in notebook output; raw Excel must be exported to CSV for the pipeline
**Target:** `OD` (overdose, 0/1) | **Problem type:** classification | **ID:** `ID`, kept for output but excluded from model inputs
**Input cleanup:** Rename `rx ds` to `rx_ds`; use the same rule for training and inference

## Feature recipe
**Binary passthrough:** `Low_inc`, `SURG`, `A`, `B`, `C`, `D`, `E`, `F`, `H`, `I`, `J`, `K`, `L`, `M`, `N`, `R`, `S`, `T`, `V`
**Continuous:** `rx_ds` -> `StandardScaler`; confirmed available at prediction time
**Buckets:** `rx_ds` -> four quantile bins, one-hot encoded; learn boundaries on training split only
**Engineered:** `binary_sum` = sum of 19 binary fields; `rx_ds_to_binary_sum` = `rx_ds / binary_sum`
**Zero denominator:** Set ratio to 0 when `binary_sum == 0` (provisional rule for explicit confirmation)
**Excluded columns:** `OD` from predictors; `ID` from predictors; `rx_ds_bucket` is an intermediate, not a raw input
**features.py signature:** `get_feature_preprocessor(binary_columns: list[str], rx_ds_column: str = "rx_ds", n_bins: int = 4) -> ColumnTransformer`
**SETTINGS["features"]:** `binary_columns` = fields above; `rx_ds_column` = `rx_ds`; `n_bins` = 4

## Model, evaluation and validation
**Model:** `LogisticRegression(class_weight="balanced", max_iter=1000, random_state=42)` in a preprocessing `Pipeline`
**Primary ML metric:** recall | **evaluate_model key:** `"recall"` | **Quality gate:** To be confirmed from README, not invented
**Supporting metrics:** precision, f1, roc_auc, specificity | **Classification threshold:** 0.5 initially
**Split:** 70% train, 15% validation, 15% sealed test; stratified; `random_state=42`
**Evaluation rule:** Train only on training split; evaluate on validation; do not tune on final test data
**Validation rules:** Check required fields, unique non-null IDs, binary 0/1 values, nonnegative finite `rx_ds`, valid 0/1 target and both target classes
**Inference rule:** Keep every input row and its ID; never use the target as an input; reject invalid rows rather than silently dropping them

## Shared implementation decisions
**Function contract:** Use the unmodified function names and return types in the kick-off scaffold
**Shared utils.py:** `load_csv`, `save_csv`, `save_model`, `load_model` (generic helpers only)
**Settings:** Critical paths, columns, split, model parameters and validation rules in `src/main.py` `SETTINGS`; leave `config.yaml` unchanged
**Environment:** Python 3.12; pandas, numpy, scikit-learn, joblib, pytest, flake8; review existing `environment.yml` before editing
**Owners:** Solo practice: one student owns all modules; each module gets its own branch and pull request
**README follow-ups:** Confirm client, business baseline, serving mode, business indicator, recall release threshold, privacy controls and deployment risks; owner: student
**Notebook correction:** Retire test-set threshold tuning (cell 28), fit quantile bins after splitting (cell 11), preserve IDs (cell 8)
