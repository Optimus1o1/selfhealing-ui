# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.0.0rc1] - 2026-11-02

### Added
- **52-Scenario Independent Holdout Validation Dataset** (`tests/evaluation/holdout_benchmark.py`):
  - Evaluates complex nested forms, multi-step wizards, dynamic React-style components (styled-components hashes, Tailwind arbitrary classes), repeated accessible names, async hydration, mobile responsive drawers, near-tie candidate collisions, and actionability boundaries.
  - Achieves 100.00% precision, 0.00% false positive rate (FPR), 80.95% recall, 92.31% accuracy, and 89.47% F1 score across unseen mutation topologies.
- **Combined 109-Scenario Empirical Benchmark**:
  - Across 57 baseline scenarios + 52 holdout scenarios: 100.00% precision, 0.00% FPR, 87.30% recall, 92.66% overall accuracy.
- **Multi-Tier 500+ Iteration Performance Profiler** (`tests/evaluation/profile_performance.py`):
  - Evaluates micro-benchmarks (pure algorithm scoring, decision engine evaluation, live browser DOM extraction) with 50 warm-up runs and 500 iterations.
  - Demonstrates configurable action timeout strategies (`action_timeout_ms: 1000` vs `2500`).
- **Pytest Plugin Registration**:
  - Registered `selfheal = "selfheal.pytest_plugin"` entry point in `pyproject.toml` for zero-configuration fixture loading in user test suites.
- **Configurable Action Timeout**:
  - Added `action_timeout_ms` to `FrameworkSettings` and YAML configurations to enable fine-tuning of browser timeout latency.
- **Deterministic UI Synonym Phrase Matching**:
  - Token-level semantic phrase replacement (e.g. "Continue to Payment" -> "Proceed to Payment") in `compute_text_similarity`.
- **Attribute Evolution with Key & Pair Jaccard**:
  - Evaluates `element_id`, `class_list`, and standard attribute key distributions to recognize preserved structure across framework redesigns.
- **Automated Test Database Isolation**:
  - Added clean SQLite transaction fixture in `conftest.py` ensuring test idempotency across continuous runs.

### Changed
- Refined `compute_text_similarity` with balanced Levenshtein (40%), Jaro-Winkler (30%), and Token Sort (30%) weighting with keyword discrimination to eliminate prefix illusions.
- Handled `<button>` and `<a>` elements in `compute_type_and_role_similarity` without spurious `input_type` penalties.
- Enforced strict Jinja2 HTML autoescaping (`autoescape=select_autoescape(["html", "xml"])`) in test report generation to eliminate XSS vulnerabilities.

### Security
- Hardened sensitive attribute redaction covering `password`, `token`, `secret`, `apikey`, `credit_card`, and `cvv`.
- Enforced empty strings for password inner text and input values.
- Formally validated SQL parameterized statements across all repository queries.

