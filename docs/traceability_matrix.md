# Requirements Traceability Matrix (RTM)

**Moon Sanctum Labs** — *Decode. Build. Evolve.*  
**Lead Engineer:** Aniket Nandi (Kolkata, IST)  
**System Version:** `1.0.0rc1`  

---

## Traceability Architecture

The Requirements Traceability Matrix demonstrates that every functional and non-functional objective defined for the SelfHeal framework has been implemented in source code, covered by automated test suites, validated against empirical benchmarks, and preserved as verifiable artifacts.

```
Project Objective 
    ──> Requirement (FR/NFR) 
        ──> Implemented Module 
            ──> Automated Test Case 
                ──> Evaluation Metric 
                    ──> Evidence Artifact
```

---

## Master Traceability Matrix

| Objective ID | Requirement Description | Implemented Module | Automated Test Case | Measured Metric | Evidence Artifact |
|---|---|---|---|---|---|
| **OBJ-01** | Deterministic Playwright Wrapper without global monkey-patching | `src/selfheal/engine/page.py`<br/>`src/selfheal/engine/locator.py` | `tests/unit/test_locator_hardening.py::<br/>test_locator_chaining_first_last_nth` | 100% API Compatibility with Playwright | `tests/unit/test_locator_hardening.py` |
| **OBJ-02** | Automated DOM Baseline Snapshot & Privacy-Preserving Redaction | `src/selfheal/baseline/fingerprint.py`<br/>`src/selfheal/baseline/repository.py` | `tests/unit/test_fingerprint.py::<br/>test_fingerprint_sanitizes_passwords`<br/>`tests/unit/test_fingerprint.py::<br/>test_fingerprint_db_roundtrip` | 0 leaked passwords / full SQLite WAL roundtrip | `artifacts/selfheal.db` |
| **OBJ-03** | Failure Triage distinguishing absence from actionability defects | `src/selfheal/detection/failure_detector.py` | `tests/unit/test_failure_detector.py::<br/>test_classify_assertion_error`<br/>`tests/unit/test_failure_detector.py::<br/>test_classify_hidden_element`<br/>`tests/unit/test_failure_detector.py::<br/>test_classify_disabled_element` | 100% Failure Classification Accuracy (6/6) | `tests/unit/test_failure_detector.py` |
| **OBJ-04** | Fast In-Browser DOM Candidate Extraction | `src/selfheal/scanner/dom_scanner.py`<br/>`src/selfheal/scanner/dom_extractor.js` | `tests/healing/test_lifecycle_validation.py` | Mean 2.30 ms extraction latency | `artifacts/reports/performance_profile.json` |
| **OBJ-05** | Multi-Dimensional Similarity Scoring Engine | `src/selfheal/intelligence/similarity.py`<br/>`src/selfheal/intelligence/scoring.py` | `tests/unit/test_similarity.py::<br/>test_text_similarity_exact_and_variants`<br/>`tests/unit/test_similarity.py::<br/>test_type_and_role_similarity`<br/>`tests/unit/test_similarity.py::<br/>test_attributes_similarity`<br/>`tests/unit/test_similarity.py::<br/>test_position_similarity`<br/>`tests/unit/test_similarity.py::<br/>test_weighted_scoring_aggregation` | Mean 0.69 ms scoring latency across 50 candidates | `tests/unit/test_similarity.py`<br/>`artifacts/reports/performance_profile.json` |
| **OBJ-06** | Conservative Decision Gating (Threshold $\ge 0.80$, Margin $\ge 0.10$) | `src/selfheal/intelligence/decision_engine.py` | `tests/unit/test_decision_engine.py::<br/>test_decision_rejects_low_score`<br/>`tests/unit/test_decision_engine.py::<br/>test_decision_rejects_ambiguous_margin`<br/>`tests/unit/test_decision_engine.py::<br/>test_decision_approves_strong_match` | 0.00% False Positive Rate across 109 scenarios | `artifacts/reports/benchmark_results.json`<br/>`artifacts/reports/holdout_benchmark_results.json` |
| **OBJ-07** | Strict Uniqueness & Single-Retry Execution Safety | `src/selfheal/engine/executor.py` | `tests/unit/test_locator_hardening.py::<br/>test_execute_action_rejects_ambiguous_healed_retry` | Retry limit strictly enforced to 1; ambiguous counts rejected | `src/selfheal/engine/executor.py` |
| **OBJ-08** | Relational SQLite WAL Storage & Baseline Version Evolution | `src/selfheal/baseline/repository.py`<br/>`src/selfheal/database/schema.sql` | `tests/unit/test_dashboard_integration.py::<br/>test_baseline_promotion_and_rejection_workflow` | Version v1 $\rightarrow$ v2 evolution with audit trail | `artifacts/selfheal.db` |
| **OBJ-09** | Enterprise 9-Section Streamlit Audit Dashboard | `src/selfheal/dashboard/app.py` | `tests/unit/test_dashboard_integration.py::<br/>test_empty_database_handling`<br/>`tests/unit/test_dashboard_integration.py::<br/>test_invalid_or_missing_record_lookups`<br/>`tests/unit/test_dashboard_integration.py::<br/>test_metric_calculations_and_filtering` | 9 active dashboard sections verified | `artifacts/screenshots/dashboard/01_overview.png`<br/>through `09_performance_monitor.png` |
| **OBJ-10** | End-to-End E-Commerce Multi-Page Demonstration Application | `demo_app/ecommerce.py`<br/>`demo/run_demo.py` | `tests/demo/test_ecommerce_demonstration.py::<br/>test_ecommerce_complete_e2e_healing_journey`<br/>`tests/demo/test_ecommerce_demonstration.py::<br/>test_ecommerce_ambiguous_rejection_negative_case`<br/>`tests/demo/test_ecommerce_demonstration.py::<br/>test_ecommerce_actionability_rejection_negative_case` | 100% healing success on V2 with unchanged V1 test code | `artifacts/screenshots/demo/` (10 evidence images) |
| **OBJ-11** | Independent Large-Scale Evaluation Benchmark | `tests/evaluation/benchmark.py`<br/>`tests/evaluation/holdout_benchmark.py` | Automated Execution of 109 Test Scenarios | 100.0% Precision<br/>87.30% Recall<br/>92.66% Accuracy | `artifacts/reports/benchmark_results.json`<br/>`artifacts/reports/holdout_benchmark_results.json` |
| **OBJ-12** | Continuous Integration & Distribution Packaging | `.github/workflows/ci.yml`<br/>`pyproject.toml` | GitHub Actions Workflow Execution | Python Wheel & Source Distribution build clean | `dist/selfheal-1.0.0rc1-py3-none-any.whl`<br/>`dist/selfheal-1.0.0rc1.tar.gz` |

