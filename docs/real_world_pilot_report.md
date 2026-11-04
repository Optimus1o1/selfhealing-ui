# SelfHeal — Real-World Pilot Report

**Moon Sanctum Labs** — *Decode. Build. Evolve.*  
**Framework Version:** 1.0.0  
**Report Status:** TEMPLATE — pilot has NOT been conducted yet  
**Last Updated:** November 2026

---

> **Notice:** This document is a structured template for recording real-world pilot results. All result sections are intentionally blank and marked as PENDING. They will be populated only after actual external developers complete the pilot evaluation protocol.

---

## 1. Executive Summary

**Status: SELF-VALIDATION COMPLETE · EXTERNAL COHORTS PENDING**

This report documents the real-world validation program for SelfHeal 1.0.0. Phase 18B internal self-validation (Participant Code `P000`) has been successfully verified using the bundled multi-page e-commerce demonstration suite across Windows 11 and Python 3.12, achieving 100% healing precision and 0 false positives across all 7 real mutation scenarios.

External participant testing across third-party proprietary codebases (React SPAs, SaaS dashboards, and complex enterprise forms) is currently open for participant onboarding via [Pilot Onboarding Package](pilot_onboarding_package.md). Formal results for Cohorts P001–P005 will be integrated upon receipt and verification.

---

## 2. Methodology

### 2.1 Pilot Design

The pilot follows the framework defined in:
- [Pilot Testing Framework](pilot_testing_framework.md) — participant onboarding and testing protocol
- [Pilot Evaluation Methodology](pilot_evaluation_methodology.md) — metrics and data collection
- [Developer Experience Evaluation](developer_experience_evaluation.md) — DX scoring methodology
- [Compatibility Test Scenarios](compatibility_test_scenarios.md) — scenario categories

### 2.2 Participant Selection Criteria

- Must have existing experience with Playwright for Python.
- Must have an existing Playwright test suite or willingness to use the bundled demo application.
- Must test only applications they own or have explicit permission to test.
- Target: 3–5 participants across different application types.

### 2.3 Data Collection

Each participant provides:
1. Structured mutation log (what was changed, what was expected).
2. Healing event export from the CLI or dashboard.
3. Completed feedback questionnaire.
4. Optional: screen recording of the integration process.

---

## 3. Target Application Categories

| # | Category | Participant | Application Description | Status |
|---|---|---|---|---|
| 1 | React application | P001 | Community submission candidate | PENDING |
| 2 | E-commerce website | P000 | Multi-page dynamic checkout flow (Demo suite) | COMPLETED (Self-val) |
| 3 | SaaS dashboard | P002 | Community submission candidate | PENDING |
| 4 | Form-heavy application | P003 | Community submission candidate | PENDING |
| 5 | SPA application | P004 | Community submission candidate | PENDING |

---

## 4. Testing Procedures

Each participant follows the standardised 9-step protocol:

1. Install SelfHeal in a clean virtual environment.
2. Integrate `SelfHealingPage` into their test suite.
3. Run tests to create a baseline.
4. Mutate the application's UI (controlled attribute changes).
5. Run the unchanged tests.
6. Verify healing via CLI (`selfheal report`).
7. Verify healing via dashboard (Streamlit).
8. Modify a configuration threshold and re-test.
9. Complete the structured feedback questionnaire.

Detailed instructions are in the [Pilot Testing Framework](pilot_testing_framework.md).

---

## 5. Compatibility Matrix

**Status: PARTIAL (P000 Self-Validation recorded; external cohorts pending)**

| Application Type | Framework | OS | Python | Healing Precision | Healing Recall | FPR | Abstention Rate | Overall |
|---|---|---|---|---|---|---|---|---|
| E-commerce Store | Native HTML5/JS | Windows 11 | 3.12.10 | 100.00% | 85.71% (6/7) | 0.00% | 14.29% (1/7) | PASS (P000) |
| React SPA | React 18+ | TBD | TBD | Pending | Pending | Pending | Pending | PENDING |
| SaaS Portal | Vue/Next.js | TBD | TBD | Pending | Pending | Pending | Pending | PENDING |

---

## 6. Aggregate Results

**Status: PRELIMINARY (Self-Validation P000 only; external metrics pending)**

### 6.1 Accuracy Metrics

| Metric | Target | P000 Self-Validation | Status |
|---|---|---|---|
| Pilot Precision | ≥ 95% | 100.00% | VERIFIED |
| Pilot Recall | ≥ 80% | 85.71% | VERIFIED |
| False Positive Rate | ≤ 2% | 0.00% | VERIFIED |
| Abstention Rate | 5–15% | 14.29% (1 safety reject) | VERIFIED |

### 6.2 Performance Metrics

| Metric | Target | Actual | Status |
|---|---|---|---|
| End-to-end healing latency | ≤ 5 seconds | — | PENDING |
| Mean integration time | ≤ 40 minutes | — | PENDING |

### 6.3 Developer Experience

| Dimension | Target | Actual | Status |
|---|---|---|---|
| Installation complexity | ≥ 4.0 | — | PENDING |
| Integration complexity | ≥ 3.5 | — | PENDING |
| Configuration clarity | ≥ 3.5 | — | PENDING |
| API usability | ≥ 4.0 | — | PENDING |
| Error message quality | ≥ 3.5 | — | PENDING |
| Dashboard usability | ≥ 3.5 | — | PENDING |
| Documentation quality | ≥ 3.5 | — | PENDING |
| **Weighted DX Score** | **≥ 3.5** | — | PENDING |

---

## 7. Failure Analysis

**Status: PENDING — populated after testing**

### 7.1 False Negatives (Missed Healings)

| # | Application | Scenario | Root Cause | Potential Fix |
|---|---|---|---|---|
| — | — | — | — | — |

### 7.2 False Positives (Incorrect Healings)

| # | Application | Scenario | Root Cause | Severity |
|---|---|---|---|---|
| — | — | — | — | — |

### 7.3 Ambiguity Rejections

| # | Application | Scenario | Top Score | Margin | Justified? |
|---|---|---|---|---|---|
| — | — | — | — | — | — |

---

## 8. Known Limitations (Pre-Pilot)

These are known limitations of SelfHeal 1.0.0 that may affect pilot results:

1. **Shadow DOM:** Elements inside shadow roots are not scanned by `DOMScanner`.
2. **iframe content:** Elements inside `<iframe>` documents are not fingerprinted.
3. **Session-generated IDs:** Highly randomised IDs reduce attribute similarity scores.
4. **Nth-index locators:** Position-based nth-match strategies are not fingerprinted.
5. **Tag changes:** Element tag changes (e.g., `<a>` → `<button>`) significantly reduce similarity scores.
6. **macOS:** Not tested on macOS in the canonical benchmark.
7. **Dynamic content timing:** Elements that do not exist in DOM at scan time cannot be healed.

---

## 9. Participant Feedback Summary

**Status: PENDING — populated after testing**

### 9.1 Quantitative Summary

| Question | Mean Score | Range |
|---|---|---|
| How easy was installation? | — | — |
| How clear was the integration process? | — | — |
| Was the healed element correct? | — | — |
| How useful is the documentation? | — | — |
| Would you use SelfHeal in production? | — | — |

### 9.2 Qualitative Themes

**Status: PENDING**

Common themes from open-ended responses will be categorised here:
- Positive feedback themes
- Improvement suggestions
- Confusion points
- Feature requests

---

## 10. Recommended Improvements

**Status: PENDING — populated after testing**

Improvements will be prioritised based on:
1. Frequency of participant feedback
2. Impact on precision and recall
3. Technical feasibility
4. Development effort

| Priority | Improvement | Source | Effort |
|---|---|---|---|
| — | — | — | — |

---

## 11. Comparison with Canonical Benchmark

| Metric | Canonical (109 scenarios) | Pilot (real-world) | Delta |
|---|---|---|---|
| Precision | 100.00% | PENDING | — |
| Recall | 88.89% | PENDING | — |
| FPR | 0.00% | PENDING | — |
| Accuracy | 93.58% | PENDING | — |

> **Note:** The canonical benchmark uses controlled, reproducible mutations in the bundled demo application. Pilot results reflect uncontrolled real-world conditions and are expected to show wider variance. A precision drop below 95% or any false positive occurrence would trigger an engineering investigation.

---

## Appendices

### A. Raw Participant Data

**Status: PENDING** — anonymised per-participant YAML records will be appended here.

### B. Healing Event Logs

**Status: PENDING** — relevant CLI report exports will be included here.

### C. Dashboard Screenshots

**Status: PENDING** — key dashboard views from pilot sessions will be captured here.

---

*Moon Sanctum Labs — Decode. Build. Evolve.*

