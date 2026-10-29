# Opioid Overdose Risk Prediction

> Build a reproducible overdose-risk pipeline so model results can be tested, traced and evaluated reliably

**Status:** Educational business-case draft reconstructed from the notebook and prior discussion. It has not been independently approved, clinically validated or confirmed as merged into `dev`. Open decisions are explicitly marked.

## 1. Business case

### Context

- **Provisional setting:** A healthcare team explores whether a model can identify people at elevated opioid-overdose risk for additional clinical review
- **Client, unit, system owner and organizational maturity:** To be confirmed
- **Human responsibility:** A qualified professional makes clinical decisions, not the model

### Problem and baseline

- **Problem:** Reduce missed overdose-positive cases without overwhelming reviewers with false alerts
- **Current workflow and business baseline:** To be measured (specify process, indicator, value, period and source)
- **Distinction:** The notebook's majority-class classifier is an ML baseline, **not** a measured baseline for clinical operations

### Goal and success metrics

| Type | Metric | Baseline | Target or threshold |
| --- | --- | --- | --- |
| Business key performance indicator | To be defined, linked to missed-risk cases or review outcomes | To be measured | To be agreed |
| Primary ML metric | `recall` for `OD = 1` | Re-evaluate on validation data | **To be set before final evaluation** |
| ML guardrail | `precision` | To be measured | To be agreed |
| Supporting metrics | `f1`, `roc_auc`, `specificity` | To be measured | Reported, not release gates yet |
| Operational limits | Latency and cost per prediction | To be measured | To be agreed |

**Confirmed decision:** Prioritize recall to reduce false negatives, while tracking precision to limit false alerts. No numerical release threshold has been approved.

### Solution

- **Proposed output:** Overdose-risk prediction or probability, linked to the original `ID`
- **Target:** `OD`, a binary indicator of opioid overdose (meaning confirmed in the coaching conversation)
- **Inputs:** `Low_inc`, `SURG`, letter-coded binary indicators and prescription quantity `rx_ds`; `rx_ds` was confirmed available at prediction time
- **Prototype model:** Class-weighted logistic regression, following the notebook
- **Serving mode:** Batch or on-demand, to be decided
- **Fallback:** Human-led review if the model is unavailable or not approved; no autonomous clinical decisions

### Data

- **Notebook:** `opiod_analysis_v01(2).ipynb`
- **Referenced workbook:** `CaseStudy_training_data.xlsx`, worksheet `Model_data` (provenance not supplied)
- **Notebook summary:** 1,000 records, 22 columns, 23.5% positive `OD` outcomes; no missing values reported in the initial profile
- **Preparation:** Rename `rx ds` to `rx_ds`; exclude `ID` from model features but retain it with outputs
- **Unverified:** Data owner, row meaning, label provenance, refresh frequency, permissions, privacy status and representativeness
- **Teaching safeguard:** Use only public, synthetic or suitably anonymised data in the repository

### Value, cost and risks

**Potential value:** Replace a one-off notebook with a reproducible, tested pipeline for investigating overdose-risk prediction. Real-world benefit, cost, staffing and clinical suitability have not been established.

| Risk | Mitigation |
| --- | --- |
| Missed positives or excess alerts | Measure recall and precision; keep professional review |
| Data leakage and inflated performance | Fit transformations on training data; keep final test data sealed; never tune on test results |
| Invalid data or unavailable inputs | Validate required fields, ranges, identifiers and prediction-time availability |
| Privacy, bias and poor generalization | Verify data rights, assess subgroups and evaluate on representative unseen data |
| Failure or model deterioration | Define ownership, monitoring, fallback and rollback before deployment |

### Open gaps

1. Confirm client, workflow, ownership and organizational maturity
2. Measure or clearly estimate the **business** baseline and define the business KPI and target
3. Set the numerical `recall` quality gate **before** final evaluation, plus a precision guardrail
4. Agree on batch versus on-demand serving, latency limits and cost expectations
5. Verify data provenance, outcome definition, time horizon, access rights and privacy safeguards
6. Estimate value and costs against a non-ML alternative; assign risk and fallback owners
7. Obtain project-owner approval before treating this README as finalized and merged into `dev`

## 2. Starting a new coaching session

Attach **this README**, `opiod_analysis_v01(2).ipynb`, and the amended `ai-prompt-kickoff-scaffold.md`. The README is the intended source for **business decisions**; the notebook supports **technical facts**. The separate `TEAM_BRIEF.md` records module agreements once reconciled with this README. Resolve business-case gaps before treating project setup as complete. Students should create repository files themselves in VS Code, with guided explanation, copy-paste snippets, tests and confirmation gates.
