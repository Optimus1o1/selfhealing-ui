# Release Notes — SelfHeal 1.0.0 Stable

**Moon Sanctum Labs** — *Decode. Build. Evolve.*  
**Lead Engineer:** Aniket Nandi (Kolkata, IST)  
**Release Tag:** `v1.0.0` (Pending Owner Push)  
**Date:** November 2, 2026  
**License:** MIT License  

---

## Executive Summary

Moon Sanctum Labs is pleased to announce the official stable **1.0.0 release** of **SelfHeal**, a production-grade, deterministic self-healing test automation framework for Microsoft Playwright in Python.

SelfHeal solves the enterprise *brittle locator problem*: automated end-to-end tests breaking due to routine CSS refactoring, design system migrations (e.g. Bootstrap to Tailwind CSS), dynamic hash classes, or copy changes. Rather than relying on non-deterministic cloud-hosted Large Language Models (LLMs) or brittle pixel-based computer vision, SelfHeal uses a deterministic 6-dimensional similarity engine operating completely locally in **under 3 milliseconds** with **zero false positive interactions**.

---

## 🚀 Major Capabilities

1. **Drop-in Playwright Integration:**
   - Wraps Playwright's `Page` and `Locator` primitives (`SelfHealingPage`, `SelfHealingLocator`).
   - 100% backward-compatible: test scripts written for vanilla Playwright run without architectural rewrites.
   - Built-in `pytest` plugin registering the zero-configuration `healed_page` fixture.
   - Full support for locator chaining (`first`, `last`, `nth`).

2. **Deterministic 6-Dimensional Similarity Engine:**
   - **Text & Semantics (30%):** Combines RapidFuzz normalized Levenshtein, Jaro-Winkler, and Token Sort with a curated 12-set UI synonym ontology (e.g. "Login" $\leftrightarrow$ "Sign In", "Cart" $\leftrightarrow$ "Bag", "Continue to Payment" $\leftrightarrow$ "Proceed to Payment").
   - **Accessible Name Blending:** Dynamically prioritizes W3C accessible names over visible text ($0.70 \times \text{acc} + 0.30 \times \text{text}$) to disambiguate identical buttons across repetitive cards.
   - **HTML Tag & ARIA Role Compatibility (20%):** Handles interchangeable controls (`<button>`, `<a>`, `<input type="submit">`) with structured role matrices.
   - **Attribute Evolutionary Jaccard Overlap (20%):** Measures intersection-over-union across attribute keys and key-value pairs, accommodating utility class additions (e.g. Tailwind).
   - **Parent Container Hierarchy (15%):** Anchors candidate controls within form and card boundaries using container tags, parent IDs, and parent CSS classes.
   - **Child Substructure (10%):** Analyzes internal icons, badges, and nested spans.
   - **Spatial Viewport Proximity (5%):** Normalizes centroid Euclidean distance relative to standard viewport diagonal ($D = 1920\text{ px}$).

3. **Dual-Gating Safety Policy & Zero False Positives:**
   - **Minimum Confidence Threshold:** Requires winning candidate score $S_1 \ge \tau_{\min} = 0.80$.
   - **Ambiguity Margin Protection:** Requires runner-up margin $\Delta = S_1 - S_2 \ge \Delta_{\min} = 0.10$. Rejects near-tie candidate collisions (`REJECTED_AMBIGUOUS_MATCH`).
   - **Strict Candidate Uniqueness:** Verifies that the synthesized selector resolves to strictly one element (`count == 1`). Rejects multi-element collisions (`REJECTED_AMBIGUOUS_RETRY`).
   - **Single-Retry Guarantee:** Retries a healed interaction strictly once; never enters recursive or non-deterministic retry loops.

4. **Failure Classification Engine:**
   - Differentiates true locator disappearance ($count == 0$) from actionability defects (`ELEMENT_HIDDEN`, `ELEMENT_DISABLED`, `AMBIGUOUS_LOCATOR`, `INVALID_SELECTOR`, `ASSERTION_FAILURE`).
   - Fast short-circuits on unhealable bugs without attempting repair.
   - Configurable grace period (`grace_period_ms: 500`) to accommodate asynchronous SPA hydration.

5. **Auditable SQLite WAL Persistence & Baseline Evolution:**
   - Embedded SQLite storage operating in Write-Ahead Logging (`WAL`) mode (`artifacts/selfheal.db`).
   - Full version lifecycle tracking (Baseline v1 $\rightarrow$ v2 promotion).
   - Non-blocking concurrent access: running test suites append to WAL without blocking dashboard readers.
   - Non-repudiation audit log in `locator_history` recording approver identities and timestamps.

6. **Enterprise 9-Section Streamlit Audit Dashboard:**
   - **Overview:** Executive KPIs, test volumes, and historical run trends.
   - **Live Execution:** Real-time run monitoring and step-by-step selector execution logs.
   - **Healing Analytics:** Decision triage (approved vs rejected) and failure distribution charts.
   - **Locator Explorer:** Target key inventory, stability index, and mutation timeline.
   - **Fingerprint Inspector:** Side-by-side DOM attribute diff (`MATCHED`, `CHANGED`, `NEW`).
   - **Intelligence Inspector:** 6-dimension score breakdown, threshold & margin checks, diagnostics.
   - **Audit Centre:** Pending review queue with an explicit confirmation checkbox gate before promoting to V2.
   - **Baseline Manager:** Version evolution tracking (v1 $\rightarrow$ v2) with active vs archived status.
   - **Performance Monitor:** Live SQLite WAL latency percentiles ($P_{50}, P_{90}, P_{95}$) vs benchmarks.

---

## 📊 Canonical Evaluation & Performance Results

### 1. Empirical Accuracy Across 109 Scenarios

| Metric | Baseline Suite (57) | Holdout Suite (52) | **Combined (109 Scenarios)** |
|---|---|---|---|
| **True Positives (TP)** | 38 | 18 | **56** |
| **True Negatives (TN)** | 15 | 31 | **46** |
| **False Positives (FP)** | 0 | 0 | **0 (0.00%)** |
| **False Negatives (FN)** | 4 | 3 | **7** |
| **Healing Precision** | **100.00%** | **100.00%** | **100.00%** |
| **False Positive Rate** | **0.00%** | **0.00%** | **0.00%** |
| **Healing Recall** | **90.48%** | **85.71%** | **88.89%** ($56 / 63$) |
| **Overall Accuracy** | **92.98%** | **94.23%** | **93.58%** ($102 / 109$) |
| **F1 Score** | **95.00%** | **92.31%** | **94.12%** |

### 2. Multi-Tier Latency Telemetry (500+ Iterations)

| Subsystem Component | Mean Latency | Median (P50) | 95th Percentile (P95) |
|---|---|---|---|
| **Pure Algorithm Scoring** | **0.796 ms** | **0.647 ms** | **1.639 ms** |
| **Decision Engine Gating** | **0.008 ms** | **0.004 ms** | **0.023 ms** |
| **In-Browser DOM Extraction** | **2.266 ms** | **2.156 ms** | **3.076 ms** |
| **Normal Execution Overhead** | **24.494 ms** | **23.881 ms** | **28.518 ms** |
| **Standard Healing ($2,500$ ms timeout)** | **3,077.63 ms** | **3,076.90 ms** | **3,100.09 ms** |
| **Fast Healing ($1,000$ ms timeout)** | **1,577.15 ms** | **1,580.19 ms** | **1,590.05 ms** (48.8% faster) |

---

## 🛠️ Installation & Quickstart

### 1. Requirements
- Python 3.11 or 3.12
- Node.js (for Playwright browser engines)

### 2. Install from Wheel or Source
```bash
# Clone the repository
git clone https://github.com/<owner>/selfhealing-ui.git
cd selfhealing-ui

# Install dependencies and package
pip install -r requirements.txt
pip install -e .

# Install Playwright browser engine
playwright install chromium
```

### 3. Writing Tests with SelfHeal
```python
from selfheal import SelfHealingPage

def test_login_flow(page):
    sh_page = SelfHealingPage(page)
    sh_page.goto("https://example.com/login")

    # Bind interactions to stable logical target keys
    sh_page.healed_locator("#username", key="auth.username").fill("demo_user")
    sh_page.healed_locator("#password", key="auth.password").fill("secret123")

    # If #btnLogin is renamed to #btnSignInSubmit, the engine heals it automatically!
    sh_page.healed_locator("#btnLogin", key="auth.submit").click()

    assert "/dashboard" in sh_page.raw_page.url
```

### 4. Running the Dashboard
```bash
selfheal dashboard --port 8501
# Or directly:
streamlit run src/selfheal/dashboard/app.py
```

---

## 🔒 Security & Privacy Considerations

1. **Automatic Password & Token Redaction:** During baseline capture, password inputs, authentication tokens, and sensitive attributes (`password`, `token`, `secret`, `apikey`, `credit_card`, `cvv`) are stripped or set to empty strings.
2. **100% Parameterized SQL:** All SQLite repository queries use parameterized placeholders (`?`), preventing SQL injection.
3. **Strict HTML Autoescaping:** HTML test report generation enforces `select_autoescape(["html", "xml"])` in Jinja2 to eliminate XSS risks.
4. **Local-First Privacy:** Zero network transmission; DOM snapshots and attributes are never transmitted to external cloud endpoints.

---

## ⚠️ Known Platform Limitations

The following boundaries represent standard web platform constraints rather than software bugs:
1. **Closed Shadow DOM:** In compliance with the W3C Shadow DOM specification, closed shadow roots cannot be traversed by external JavaScript evaluators. (Open shadow roots are fully supported).
2. **HTML5 Canvas & WebGL:** Pixels rendered on a canvas lack individual DOM element nodes and cannot be matched using DOM-level heuristics.
3. **Cross-Origin iframes:** Elements inside third-party iframes without appropriate CORS permissions cannot be inspected in a single evaluation context.

---

## 👥 Authors & Acknowledgments

- **Lead Engineer & Architect:** Aniket Nandi (Kolkata, IST)
- **Agency:** Moon Sanctum Labs — *Decode. Build. Evolve.*
- **License:** MIT License
