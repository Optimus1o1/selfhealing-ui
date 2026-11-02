# SelfHeal — Project Showcase & Presentation Guide

**Version:** 1.0.0 (Stable)  
**Moon Sanctum Labs** — *Decode. Build. Evolve.*  
**Lead Engineer:** Aniket Nandi (Kolkata, IST)  
**Repository:** [SelfHeal — Intelligent Self-Healing UI Automation](https://github.com/)

---

## 🧭 Executive Overview

**SelfHeal** is a production-ready, deterministic self-healing test automation framework for Microsoft Playwright in Python. It resolves the single largest maintenance bottleneck in modern software delivery: **brittle DOM locators that break during routine UI refactoring**.

Unlike heuristic or probabilistic approaches that rely on remote Large Language Models (LLMs) — which introduce non-deterministic execution, high latency, data leakage, and false positive clicks — SelfHeal uses a **multi-dimensional deterministic similarity engine** backed by versioned SQLite WAL storage.

### Core Value Proposition:
1. **Zero Flakiness / Zero False Positives**: Evaluated across 109 independent UI mutation scenarios with **100.00% precision** and **0.00% false positive rate**.
2. **Deterministic & Local**: Pure Python and in-browser DOM extraction with RapidFuzz scoring. Runs completely offline in under 3.5 milliseconds per evaluation.
3. **Non-Invasive Architecture**: Wraps Playwright via clean proxy composition (`SelfHealingPage`, `SelfHealingLocator`). Zero monkey-patching of Playwright internals.
4. **Complete Engineering Transparency**: 9-section Streamlit governance dashboard providing dimensional score radars, baseline evolution tracking, and human-in-the-loop review queues.

---

## ⏱️ 3-Minute Technical Pitch (Engineering Leads & Architects)

### Target Audience:
Principal QA Architects, Senior Staff Engineers, DevOps Leads, Engineering Directors.

### Key Talking Points:
* **The Problem**: End-to-end UI tests break constantly not because user flows are broken, but because frontend teams rename CSS classes, change kebab-case IDs, or wrap buttons in new `<div>` containers. Teams waste 30–40% of their automation sprints updating selectors.
* **Why Not LLMs?**: Sending whole DOM trees to cloud LLMs costs tokens, takes 2–8 seconds per failure, poses security/PII leakage risks, and risks hallucinating interactions on completely wrong elements.
* **The SelfHeal Solution**:
  * Captures element fingerprints during baseline test runs (tag, text, accessible name, attributes, parent context, children structure, bounding box).
  * On locator timeout, triage with the **Failure Classifier** immediately rules out genuine actionability bugs (hidden, disabled, syntax error) so real bugs are never masked.
  * If the locator is genuinely absent, it scans the live DOM and calculates a 6-dimension weighted similarity score ($S$).
  * Enforces **two strict mathematical guardrails**:
    1. **Confidence Threshold**: $S \ge 0.80$.
    2. **Ambiguity Margin**: $\Delta = S_1 - S_2 \ge 0.10$. If two buttons are too similar, it safely abstains rather than guessing.
  * Verifies candidate uniqueness ($count == 1$) and executes a single safe retry.

### 3-Minute Live Terminal Walkthrough:
```bash
# 1. Run the headless academic demonstration
python scripts/run_academic_demo.py
```
* **Step 1 (Baseline V1)**: Show terminal output demonstrating that normal tests establish element baselines in SQLite.
* **Step 2 (Mutation V2)**: Show V2 tests running the *exact same test script* against a mutated frontend with changed IDs, altered text, and restructured DOM.
* **Step 3 (Healing Execution)**: Point to the live terminal logs showing similarity computation:
  `[HEALED] Target 'auth.login_submit': #btnLogin -> button:has-text('Sign In') (Score: 0.8640 >= 0.80, Margin: 0.2840 >= 0.10)`.
* **Step 4 (Ambiguity Rejection)**: Point to Scenario F output where two conflicting payment buttons score within 0.05 of each other, triggering `REJECTED_AMBIGUOUS_MATCH` to prevent false positive checkout.

---

## ⏱️ 5-Minute Full Product Demonstration (Product & QA Leads)

### Target Audience:
QA Managers, Product Managers, Software Engineers in Test (SDETs), Engineering Teams.

### Presentation Flow & Script:

#### Minute 1: The Context & Live Mutation Application
* Open the e-commerce demo application in browser (`http://localhost:5000/v1` vs `http://localhost:5000/v2`).
* Highlight the intentional changes between V1 and V2:
  * Login Button: `#btnLogin` ("Log In") $\rightarrow$ `#sign-in-btn` ("Sign In") wrapped in an extra flex container.
  * Add to Cart: Standard `#btnAddToCart1` $\rightarrow$ 3 identical "Add to Bag" buttons inside responsive product cards.
  * Checkout: `#btnProceedCheckout` $\rightarrow$ `.checkout-btn-cta` with restructured parent DOM.
* State clearly: *"In conventional Playwright test suites, every single one of these tests fails immediately, halting the release pipeline."*

#### Minute 2: Running the Healed Test Suite
* Execute the test suite with headed browser:
  ```bash
  python scripts/run_academic_demo.py --headed
  ```
* Show the browser autonomously navigating the store, encountering broken locators, calculating candidate scores, repairing selectors in real time, and completing the order successfully without modifying a single line of test code.

#### Minute 3: The Safety Guardrails in Action
* Demonstrate **Scenario F (Ambiguous Candidate Protection)**:
  * Explain: *"What happens if there are two similar buttons? Traditional auto-healers click whichever happens to be first. SelfHeal calculates the score margin. If $\Delta < 0.10$, it immediately flags an ambiguity error and halts."*
* Demonstrate **Scenario G (Actionability Failure)**:
  * Explain: *"If a button is disabled, SelfHeal does not attempt to heal it. It correctly classifies it as `ELEMENT_DISABLED` and asserts test failure, preserving genuine bug reporting."*

#### Minute 4: The 9-Section Engineering Streamlit Dashboard
* Launch and show the dashboard:
  ```bash
  selfheal dashboard --port 8501
  ```
* Navigate through key views:
  1. **Overview**: Executive telemetry showing 100% precision, zero false positives, and mean latency.
  2. **Intelligence Inspector**: Select a healed event (e.g., `auth.login_submit`). Show the 6-dimension radar/bar chart breakdown (Text 30%, Tag/Role 20%, Attributes 20%, Parent 15%, Children 10%, Geometry 5%).
  3. **Fingerprint Inspector**: Show the side-by-side diff comparing the V1 baseline DOM attributes with the V2 live candidate attributes, color-coded as `MATCHED`, `CHANGED`, or `NEW`.

#### Minute 5: Governance & Human-in-the-Loop Sign-off
* Navigate to **Audit Centre**:
  * Show the pending review queue.
  * Demonstrate the human QA sign-off gate: select the pending repaired locator, review before/after selectors, click the safety confirmation checkbox, and click **Approve & Promote to V2**.
  * Show that the new selector is committed as the new active baseline in SQLite WAL, making future test runs instant with zero healing overhead.

---

## 🖼️ Visual Screenshot Gallery

All visual assets are stored in the repository under `docs/assets/`:

### 1. System Architecture & Workflows
* **System Architecture**: `docs/assets/diagrams/architecture_overview.svg`  
  *Depicts the 4-tier separation: Test Execution Layer, Detection & Triage Layer, Deterministic Engine Layer, and Audit & Governance Layer.*
* **Healing Decision Lifecycle**: `docs/assets/diagrams/healing_workflow.svg`  
  *Details the complete gatekeeper flowchart including Failure Classifier, Score Threshold ($S \ge 0.80$), Ambiguity Margin ($\Delta \ge 0.10$), and Uniqueness Check ($count == 1$).*
* **Similarity Dimension Weights**: `docs/assets/diagrams/feature_weights.svg`  
  *Visualizes the 6 deterministic dimensions: Text (30%), Type & Role (20%), Attributes (20%), Parent (15%), Children (10%), Geometry (5%).*

### 2. Engineering Dashboard Gallery (`docs/assets/dashboard/`)
| Section | Screenshot File | Description |
|:---|:---|:---|
| **01 Overview** | `01_overview.png` | Executive KPI cards, execution counts, success rates, latency, and historical trend lines. |
| **02 Live Execution** | `02_live_execution.png` | Real-time session monitoring with status badges and chronological execution steps. |
| **03 Healing Analytics** | `03_healing_analytics.png` | Triage analysis, failure classification breakdown, retry rates, and score distributions. |
| **04 Locator Explorer** | `04_locator_explorer.png` | Target key inventory, locator stability index, mutation timelines, and version counts. |
| **05 Fingerprint Inspector** | `05_fingerprint_inspector.png` | Side-by-side baseline vs candidate DOM attribute diff (MATCHED / CHANGED / NEW). |
| **06 Intelligence Inspector** | `06_intelligence_inspector.png` | Multi-dimensional score breakdown, threshold gating, and natural language explanations. |
| **07 Audit Centre** | `07_audit_centre.png` | Human sign-off workflow, pending review queue, safety checkbox, and V2 promotion. |
| **08 Baseline Manager** | `08_baseline_manager.png` | Version lifecycle tracking (v1 $\rightarrow$ v2) and active vs archived baseline inventory. |
| **09 Performance Monitor** | `09_performance_monitor.png` | Real-time database latency percentiles (P50, P90, P95) vs laboratory benchmarks. |

### 3. Demonstration & Verification Gallery (`docs/assets/demo/`)
| Scenario | Screenshot File | Captured Evidence |
|:---|:---|:---|
| **Scenario A** | `01_scenario_a_v1_login_baseline.png` | V1 Baseline login page with semantic IDs captured into SQLite baseline. |
| **Scenario A** | `02_scenario_a_v1_checkout_baseline.png` | V1 Baseline checkout page establishing shipping and payment fingerprints. |
| **Scenario B** | `03_scenario_b_v2_login_mutated.png` | V2 Mutated login form with renamed IDs and modernized CSS classes. |
| **Scenario B** | `04_scenario_b_v2_login_healed_success.png` | Autonomous healing of `#btnLogin` to `button:has-text('Sign In')` ($S = 0.8640$). |
| **Scenario E** | `05_scenario_e_catalog_grid_candidates.png` | Multi-card catalog grid with 3 identical "Add to Bag" buttons. |
| **Scenario E** | `06_scenario_e_catalog_item_added_to_cart.png` | Disambiguation using card context; target item correctly added to cart. |
| **Scenario D** | `07_scenario_d_v2_checkout_restructured.png` | V2 Restructured multi-tier checkout DOM with modified hierarchy. |
| **Scenario D** | `08_scenario_d_v2_order_success.png` | Successful end-to-end checkout completion and order confirmation. |
| **Scenario F** | `09_scenario_f_ambiguous_candidates.png` | Ambiguous payment buttons rejected via margin guardrail ($\Delta < 0.10$). |
| **Scenario G** | `10_scenario_g_disabled_target.png` | Disabled checkout button intercepted by failure classifier (`REJECTED_ACTIONABILITY`). |

---

## 🏆 Portfolio & GitHub Presentation Guide

### Headline Pitch (for GitHub profile, CV, or LinkedIn):
> *"Architected and built **SelfHeal**, a production-grade, deterministic self-healing test automation framework for Microsoft Playwright in Python. Evaluated across 109 UI mutation scenarios with 100% precision, 0% false positives, and 93.58% accuracy. Features versioned SQLite persistence, safe proxy composition, and an enterprise 9-section Streamlit governance dashboard."*

### Key Technical Achievements to Emphasize:
1. **Mathematical Rigor Over Generative AI**:
   - Replaced unreliable cloud LLMs with RapidFuzz token sorting, Levenshtein distance, Jaccard attribute overlap, and UI synonym ontologies.
   - Algorithmic latency: **$\approx 3.2$ ms** per element evaluation vs. $2,000 - 5,000$ ms for LLMs.
2. **The "Zero False Positive" Safety Architecture**:
   - In automated test execution, a false positive click (clicking the wrong button or submitting the wrong form) is worse than a test failure.
   - Implemented a two-tiered gating mechanism ($S \ge 0.80$, $\Delta \ge 0.10$) and actionability pre-filtering that completely eliminated false positive interactions ($0 / 109$ occurrences).
3. **Clean Software Engineering & Architecture**:
   - Avoided brittle global monkey-patching of Playwright internals by implementing proxy composition (`SelfHealingPage` and `SelfHealingLocator`).
   - Built a complete `pytest11` plugin enabling seamless zero-config test suite adoption (`def test_flow(healed_page): ...`).
4. **Enterprise Governance & Auditability**:
   - Local-first SQLite database running in Write-Ahead Logging (WAL) mode with ACID transaction guarantees.
   - Automatic redaction of sensitive credentials, passwords, and tokens before persistence.
   - Interactive human-in-the-loop audit interface for QA engineers to review, approve, or reject repaired locators.

---

## 📊 Summary of Canonical Benchmark Results

```
========================================================================================
EVALUATION BENCHMARK SUITE SUMMARY (109 COMBINED SCENARIOS)
========================================================================================
Total Scenarios Evaluated:         109
True Positives (Repaired):         56
True Negatives (Correct Abort):    46
False Positives (Misdirected):     0  (0.00% False Positive Rate)
False Negatives (Missed Repairs):  7
----------------------------------------------------------------------------------------
PRECISION:                         100.00%
FALSE POSITIVE RATE (FPR):         0.00%
RECALL:                            88.89%
OVERALL ACCURACY:                  93.58%
F1 SCORE:                          94.12%
MEAN HEALING LATENCY:              1,842 ms (dominated by Playwright action timeout)
PURE ALGORITHMIC LATENCY:          3.2 ms per candidate evaluation
========================================================================================
```

---

## 🏷️ Credits & Agency Attribution

- **Developed By:** Moon Sanctum Labs — *Decode. Build. Evolve.*
- **Lead Full-Stack Engineer & Architect:** Aniket Nandi (Kolkata, IST)
- **License:** MIT License

