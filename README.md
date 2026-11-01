# Self-Healing UI Automation Framework

**Moon Sanctum Labs** — *Decode. Build. Evolve.*  
**Lead Developer:** Aniket Nandi (Kolkata, IST)

A production-grade, deterministic self-healing test automation framework for Playwright with Python. Recovers broken locators caused by routine UI refactoring without brittle monkey-patching or non-deterministic LLM hallucination.

---

## 🚀 Key Architectural Highlights

1. **Deterministic Intelligence Engine**: Multi-dimensional weighted similarity scoring combining RapidFuzz string metrics (Jaro-Winkler, token sort), Jaccard attribute analysis, parent/child DOM hierarchy, and spatial proximity.
2. **Failure Classification Engine**: Distinguishes true locator absence (`count == 0`) from actionability defects (`hidden`, `disabled`, `ambiguous`, `invalid syntax`, or assertion errors).
3. **Safe Composition & Delegation**: `SelfHealingPage` and `SelfHealingLocator` wrap Playwright without modifying internal classes.
4. **Stable Element Identities**: Supports explicit and inferred `target_key` (e.g. `login.submit_button`) to prevent false-matching between semantically distinct buttons.
5. **Conservative Healing Policy**: Requires minimum similarity threshold ($\ge 0.85$), confidence margin ($\ge 0.10$) between top candidates, candidate uniqueness check, and retries an action **only once**.
6. **Auditable SQLite WAL Persistence**: Versioned baselines, pending review workflows, locator evolution tracking, and complete privacy safeguards (sensitive values and passwords redacted).
7. **Streamlit Audit Dashboard & Reports**: Interactive portal for QA engineers to inspect similarity breakdowns, approve/promote repaired locators, and view metrics.

---

## 📊 Evaluation & Benchmark Results

Evaluated against simulated front-end refactoring scenarios:

| Metric | Target | Measured Result |
|---|---|---|
| **Healing Precision** | $> 90\%$ | **100.0%** |
| **Healing Recall** | $> 85\%$ | **100.0%** |
| **False Positive Rate (FPR)** | $< 5\%$ | **0.0%** |
| **Overall Accuracy** | $> 90\%$ | **100.0%** |
| **Average Algorithm Latency** | $< 200 \text{ ms}$ | **~1.2 ms** |

---

## 🛠️ Quick Start & Usage

### 1. Installation

```bash
# Clone and install dependencies
pip install -r requirements.txt

# Install Playwright browser binary
playwright install chromium
```

### 2. Writing a Self-Healing Test

```python
from selfheal import SelfHealingPage

def test_login_flow(page):
    sh_page = SelfHealingPage(page)
    sh_page.goto("https://your-app.com/login")
    
    # Bind locator to a stable logical identity
    sh_page.healed_locator("#username", key="login.username").fill("jane_doe")
    sh_page.healed_locator("#password", key="login.password").fill("secure_pass")
    
    # If #loginBtn is renamed to #signinBtn, the framework heals it automatically!
    sh_page.healed_locator("#loginBtn", key="login.submit_button").click()
```

### 3. Running Tests

```bash
# Run via CLI
python -m selfheal.cli test --tests tests/healing

# Or run with pytest directly
pytest tests/ -v
```

### 4. Generating Audit Reports

```bash
# Generate both JSON and HTML audit reports
python -m selfheal.cli report --format all
```

Open `artifacts/reports/report.html` in any web browser to view the visual report.

### 5. Launching the Audit Dashboard

```bash
python -m selfheal.cli dashboard --port 8501
```

Access the Streamlit Dashboard at `http://localhost:8501` to:
- Audit and review pending repaired locators.
- One-click **Approve & Promote** healed locators into the active baseline.
- Inspect full similarity score breakdowns across all scoring dimensions.
- Monitor execution latency and healing success rates.

---

## ⚙️ Configuration (`configs/default.yaml`)

```yaml
framework:
  project_name: "SelfHealing UI"
  policy: "assisted" # options: observe, assisted, automatic
  database_path: "artifacts/selfheal.db"
  report_dir: "artifacts/reports"
  grace_period_ms: 500
  retry_limit: 1

thresholds:
  minimum_score: 0.85
  minimum_score_margin: 0.10
  max_candidates: 100

weights:
  text: 0.30
  type_and_role: 0.20
  attributes: 0.20
  parent_context: 0.15
  children_structure: 0.10
  position: 0.05
```

---

## 🏛️ Project Structure

```
├── configs/default.yaml               # Engine weights and threshold configuration
├── src/selfheal/
│   ├── baseline/                      # Fingerprint models and SQLite repository
│   ├── detection/                     # Failure classifier and actionability filters
│   ├── scanner/                       # Fast JavaScript DOM candidate extractor
│   ├── intelligence/                  # RapidFuzz similarity, scoring & decision engine
│   ├── engine/                        # SelfHealingPage, SelfHealingLocator & Executor
│   ├── reporting/                     # HTML and JSON report generators
│   └── dashboard/app.py               # Streamlit analytics & audit portal
├── demo_app/app.py                    # Local HTTP demo server (V1, V2 refactored, edge cases)
├── tests/
│   ├── unit/                          # Unit tests for similarity, decision engine, detector
│   ├── healing/                       # Full end-to-end self-healing tests against demo app
│   └── evaluation/benchmark.py        # Accuracy, precision, recall and overhead benchmark
└── artifacts/                         # SQLite database, reports, and traces
```
