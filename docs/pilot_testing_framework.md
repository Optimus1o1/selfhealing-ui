# SelfHeal — Real-World Pilot Testing Framework

**Moon Sanctum Labs** — *Decode. Build. Evolve.*  
**Framework Version:** 1.0.0  
**Document Status:** Template — awaiting pilot execution

---

## 1. Purpose

This document defines the structured pilot testing programme for validating SelfHeal's self-healing capabilities with external developers using real-world Playwright test suites. The goal is to determine whether an independent developer can install, integrate, and benefit from SelfHeal without direct assistance from the framework's author.

---

## 2. Participant Prerequisites

Before beginning the pilot, participants must have:

| Requirement | Minimum Version | Verification Command |
|---|---|---|
| Python | 3.11+ | `python --version` |
| pip | 23.0+ | `pip --version` |
| Node.js | 18+ (for Playwright browsers) | `node --version` |
| Playwright for Python | 1.40+ | `pip show playwright` |
| An existing Playwright test suite | Any | At least 1 working test file |
| Chromium browser | Latest via Playwright | `playwright install chromium` |

**Operating System:** Windows 10/11 or Ubuntu 22.04+ (macOS untested in 1.0.0).

---

## 3. Step-by-Step Integration Guide

### Step 1 — Install SelfHeal

```bash
pip install selfheal
# Or from the GitHub release:
pip install https://github.com/Optimus1o1/selfhealing-ui/releases/download/v1.0.0/selfheal-1.0.0-py3-none-any.whl
```

Verify installation:

```bash
selfheal --help
```

### Step 2 — Wrap Your Page Object

Replace Playwright's `page` with `SelfHealingPage`:

```python
# Before (standard Playwright):
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto("https://your-app.example.com")
    page.click("#submit-btn")

# After (SelfHeal-wrapped):
from playwright.sync_api import sync_playwright
from selfheal import SelfHealingPage

with sync_playwright() as p:
    browser = p.chromium.launch()
    raw_page = browser.new_page()
    page = SelfHealingPage(raw_page)
    page.goto("https://your-app.example.com")
    page.click("#submit-btn")
```

> **Key point:** `SelfHealingPage` is a transparent composition wrapper. All standard Playwright `page` methods work identically. No test logic changes are required.

### Step 3 — Create a Baseline Fingerprint

Run your existing test suite once against the current stable UI. SelfHeal automatically captures element fingerprints during this run.

```bash
python -m pytest your_tests/ -v
```

Verify the baseline was created:

```bash
selfheal report --format summary
```

You should see baseline entries for every locator your tests interacted with.

### Step 4 — Mutate the Application's UI

Make a controlled change to the application's frontend that would normally break a locator:

| Change Type | Example |
|---|---|
| Rename an `id` attribute | `id="submit-btn"` → `id="checkout-button"` |
| Change button text | `"Add to Cart"` → `"Add to Basket"` |
| Restructure a parent container | Move a `<button>` from one `<div>` to another |
| Change a CSS class | `class="btn-primary"` → `class="btn-action"` |
| Rename an `aria-label` | `aria-label="Submit Order"` → `aria-label="Place Order"` |

> **Important:** Change only the locator-relevant attributes. Do not remove the element entirely — that is an intentional deletion, not a UI evolution.

### Step 5 — Run the Unchanged Test

Execute the same test suite without modifying any test code:

```bash
python -m pytest your_tests/ -v
```

**Expected behaviour:**
1. The original locator fails (0 elements found).
2. SelfHeal's `FailureClassifier` detects a count-zero failure.
3. The `DOMScanner` extracts all candidate elements from the current page.
4. The `SimilarityScorer` computes 6-dimension similarity vectors.
5. The `HealingDecisionEngine` applies threshold (≥ 0.80) and margin (≥ 0.10) guards.
6. If approved, the test retries with the replacement locator — **once**.
7. The test passes without any code changes.

### Step 6 — Verify Healing

```bash
# CLI summary:
selfheal report --format summary

# Detailed healing events:
selfheal report --format detailed

# Launch the dashboard:
streamlit run -m selfheal.dashboard.app
```

Check the dashboard's **Healing Analytics** and **Audit Centre** sections to confirm:
- The correct element was selected.
- The similarity score exceeds 0.80.
- The score margin exceeds 0.10.
- No false positives occurred.

---

## 4. Reference Pilot Application

Participants who do not have a suitable application can use the bundled e-commerce demo:

```bash
# Clone the repository:
git clone https://github.com/Optimus1o1/selfhealing-ui.git
cd selfhealing-ui

# Install:
pip install -e .
playwright install chromium

# Run the full 12-step demonstration:
python scripts/run_academic_demo.py
```

This demonstrates baseline creation (V1), UI mutation (V2), automatic healing, and ambiguous-match rejection across seven e-commerce scenarios.

---

## 5. Structured Feedback Template

After completing the pilot, participants should complete this questionnaire:

### Participant Information

| Field | Response |
|---|---|
| Name / Handle | |
| Application type tested | |
| Number of test files | |
| Number of locators | |
| Python version | |
| Operating system | |
| Playwright version | |
| Date of pilot | |

### Pilot Results

| # | Question | Rating (1–5) | Notes |
|---|---|---|---|
| 1 | How easy was installation? | | |
| 2 | How clear was the integration process? | | |
| 3 | Did baseline creation complete without errors? | | |
| 4 | Did the healing trigger correctly after UI mutation? | | |
| 5 | Was the healed element the correct replacement? | | |
| 6 | Did the dashboard display healing events accurately? | | |
| 7 | How clear was the CLI output? | | |
| 8 | Did you encounter any unexpected errors? | | |
| 9 | How useful is the documentation? | | |
| 10 | Would you use SelfHeal in a production test suite? | | |

### Open Questions

1. What was the most confusing part of the integration?
2. What feature would you want added first?
3. Did SelfHeal heal anything incorrectly? If so, describe the scenario.
4. Any other observations?

---

## 6. Troubleshooting Common Issues

| Issue | Likely Cause | Resolution |
|---|---|---|
| `selfheal` command not found | Package not on PATH | `pip install selfheal` or activate virtualenv |
| No baseline entries after test run | Tests did not use `SelfHealingPage` | Ensure `SelfHealingPage(page)` wraps the raw page |
| Healing did not trigger | Element exists but is hidden/disabled | This is an actionability failure, not a healing candidate |
| Multiple candidates, no healing | Ambiguity guard activated | Expected behaviour — score margin < 0.10 |
| `playwright install` fails | Node.js not installed | Install Node.js 18+ first |

---

## 7. Data Collection and Privacy

- SelfHeal stores fingerprints in a **local SQLite database** only.
- No data is transmitted to external servers.
- Password-type input values are automatically redacted.
- Participants should not share their `selfheal.db` file if it contains sensitive element text.
- Pilot feedback is collected via the structured template above — not through any automated telemetry.

---

*Moon Sanctum Labs — Decode. Build. Evolve.*
