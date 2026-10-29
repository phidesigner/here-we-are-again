# Team brief

## Business context

Business case: README.md, section 1 (merged into dev; date not recorded)
Use case: Healthcare professionals decide which cases warrant additional clinical review using predicted opioid overdose risk (educational prototype)
Notebook: opiod_analysis_v01(4).ipynb
Target: OD | Problem type: classification | ID column: ID

## Features, model and evaluation

Feature groups:
- Binary: [Low_inc, SURG, A, B, C, D, E, F, H, I, J, K, L, M, N, R, S, T, V] -> passthrough (19 binary indicators)
- Numerical: [rx_ds] -> passthrough (preserve original prescription quantity)
- Quartiles: [rx_ds] -> 4 quantile-based bins, one-hot encoded (boundaries fitted on training data only)
- Engineered: [binary_sum, rx_ds_to_binary_sum] -> sum of binary indicators; rx_ds / max(binary_sum, 1) to prevent division by zero

Excluded columns: ID (identifier, retained for predictions); OD (target, never a predictor)
Model: LogisticRegression(class_weight="balanced", max_iter=1000, random_state=42)
Metric: recall for OD=1, key in evaluate_model output: ["recall"], quality gate: >= 0.80 on validation data; precision reported without numerical gate
Split: test 0.15 and validation 0.15, both of full dataset; training 0.70; stratified; random_state 42

## Implementation agreements

Validation rules: Required columns present; OD and binary indicators in {0,1}; rx_ds numeric and nonnegative; no missing required values; ID present and unique (fail fast on invalid data)
README follow-ups: Business baseline and KPI, clinical thresholds, data provenance and privacy, serving mode, operational requirements -> solo owner; reconcile notebook filename reference in README
features.py signature: get_feature_preprocessor(binary_columns, prescription_column, n_bins=4) -> ColumnTransformer; fitted only inside train.py; expected 26 features when all four bins are available
Agreed extra parameters: None beyond the approved features.py signature; other contract defaults unchanged
utils.py helpers: load_csv, save_csv, save_model, load_model
Environment: No additional pipeline packages identified beyond pandas, numpy, scikit-learn, joblib, pytest and flake8; notebook-only dependencies to be decided
Decisions: Preserve notebook's weighted logistic regression; fit preprocessing on training data only; evaluate on validation; seal final test data; retain IDs; batch demonstration pending serving decision; recall >= 0.80 is educational, not clinical approval; report precision without a numerical gate
Owners (solo): all modules -> solo student