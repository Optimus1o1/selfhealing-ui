# SelfHeal — Pilot Onboarding Package

**Moon Sanctum Labs** — *Decode. Build. Evolve.*  
**Framework Version:** 1.0.0  
**Document Type:** Participant Onboarding — share this with pilot testers

---

## Invitation

Thank you for participating in the SelfHeal external pilot programme.

**SelfHeal** is a deterministic self-healing UI automation framework for Microsoft Playwright in Python. When a UI element changes and a Playwright locator breaks, SelfHeal automatically identifies the replacement element using a 6-dimension similarity algorithm — without cloud APIs, LLMs, or monkey-patching.

**What we need from you:**
- Install SelfHeal and integrate it into an existing Playwright test (or use our bundled demo).
- Make a controlled change to your application's UI.
- Run your unchanged test and observe whether SelfHeal heals the broken locator.
- Complete a structured feedback form.

**Time commitment:** approximately 60 minutes.

**What you get:** early access to the framework, your name (or handle) in the acknowledgements (optional), and direct influence on the product roadmap.

---

## Installation Guide

### Prerequisites

| Requirement | Minimum | Verify |
|---|---|---|
| Python | 3.11+ | `python --version` |
| pip | 23.0+ | `pip --version` |
| Node.js | 18+ | `node --version` |

### Step 1 — Create a Fresh Virtual Environment

```bash
# Windows:
python -m venv selfheal_pilot
selfheal_pilot\Scripts\activate

# Linux/macOS:
python3 -m venv selfheal_pilot
source selfheal_pilot/bin/activate
```

### Step 2 — Install SelfHeal from the Published Release

```bash
pip install https://github.com/Optimus1o1/selfhealing-ui/releases/download/v1.0.0/selfheal-1.0.0-py3-none-any.whl
```

### Step 3 — Install Playwright Browsers

```bash
# Linux (with system dependencies):
playwright install --with-deps chromium

# Windows:
playwright install chromium
```

### Step 4 — Verify Installation

```bash
selfheal --help
python -c "from selfheal import SelfHealingPage; print('SelfHeal ready')"
```

You should see the CLI help output and `SelfHeal ready`.

---

## Quick-Start Instructions

### If you have an existing Playwright test:

**1. Wrap your page object:**

```python
from selfheal import SelfHealingPage

# In your test setup, wrap the raw Playwright page:
page = SelfHealingPage(raw_page)
# All existing page.click(), page.fill(), page.locator() calls work unchanged.
```

**2. Run your tests to create a baseline:**

```bash
python -m pytest your_tests/ -v
```

**3. Make a UI change** (rename an `id`, change button text, move an element to a different container).

**4. Run your tests again** without modifying any test code.

**5. Check healing results:**

```bash
selfheal report --format summary
selfheal report --format detailed
```

### If you want to use the bundled demo:

```bash
git clone https://github.com/Optimus1o1/selfhealing-ui.git
cd selfhealing-ui
pip install -e .
playwright install chromium
python scripts/run_academic_demo.py
```

This runs a 12-step demonstration with 7 e-commerce healing scenarios.

---

## Consent & Authorisation Checklist

Before starting, please confirm the following by checking each box:

- [ ] I am testing an application I own or have explicit written permission to test.
- [ ] I understand SelfHeal stores element fingerprints (tag, text, attributes, position) in a local SQLite database only.
- [ ] I will not share my `selfheal.db` file if it contains sensitive element text from my application.
- [ ] I understand no data is transmitted to external servers by SelfHeal.
- [ ] I understand password-type input values are automatically redacted by SelfHeal.
- [ ] My participation is voluntary and I may withdraw at any time.
- [ ] I consent to my anonymised feedback being used to improve SelfHeal (no personal identifiers will be published).
- [ ] I will not test applications that contain confidential medical, financial, or classified data.

**Participant Code:** ______ (assigned by the pilot coordinator — e.g., P001)

---

## Pilot Execution Checklist

Complete each step in order. Check the box when done.

| # | Task | Command / Action | Done |
|---|---|---|---|
| 1 | Create a fresh virtual environment | `python -m venv selfheal_pilot` | [ ] |
| 2 | Install SelfHeal from release | `pip install <wheel URL>` | [ ] |
| 3 | Verify CLI | `selfheal --help` | [ ] |
| 4 | Verify import | `python -c "from selfheal import SelfHealingPage"` | [ ] |
| 5 | Install Playwright browser | `playwright install chromium` | [ ] |
| 6 | Wrap page in existing test | Add `SelfHealingPage(page)` | [ ] |
| 7 | Run tests to create baseline | `python -m pytest your_tests/ -v` | [ ] |
| 8 | Verify baseline entries | `selfheal report --format summary` | [ ] |
| 9 | Mutate the application UI | Change 1–3 element attributes | [ ] |
| 10 | Run unchanged tests | `python -m pytest your_tests/ -v` | [ ] |
| 11 | Check healing result | `selfheal report --format detailed` | [ ] |
| 12 | Launch dashboard | `streamlit run -m selfheal.dashboard.app` | [ ] |
| 13 | Inspect healing in dashboard | Check Healing Analytics + Audit Centre | [ ] |
| 14 | Export healing events | `python scripts/pilot/extract_healing_events.py` | [ ] |
| 15 | Complete feedback form | Fill `docs/pilot_feedback_form.md` | [ ] |
| 16 | Submit results | Send feedback + JSON export to pilot coordinator | [ ] |

---

## Troubleshooting Guide

| # | Issue | Likely Cause | Resolution |
|---|---|---|---|
| 1 | `selfheal` command not found | Package not on PATH | Activate virtualenv first, then `pip install selfheal` |
| 2 | `ModuleNotFoundError: selfheal` | Wrong Python environment | Ensure virtualenv is activated: `which python` should point to venv |
| 3 | `playwright install` fails | Node.js not installed | Install Node.js 18+ from nodejs.org |
| 4 | `Error: Browser chromium not found` | Playwright browsers not installed | Run `playwright install chromium` |
| 5 | No baseline entries after test run | Tests didn't use `SelfHealingPage` | Ensure `page = SelfHealingPage(raw_page)` wraps the Playwright page |
| 6 | Healing did not trigger | Element exists but is hidden/disabled | This is an actionability failure — SelfHeal correctly does not heal |
| 7 | Healing did not trigger | Element was completely removed from DOM | Correct behaviour — no replacement exists |
| 8 | `REJECTED_AMBIGUOUS` in report | Multiple candidates scored within margin | Expected safety behaviour — score margin < 0.10 |
| 9 | Healing selected wrong element | False positive (please report!) | File an [Incorrect Healing Report](https://github.com/Optimus1o1/selfhealing-ui/issues/new?template=incorrect_healing_report.yml) |
| 10 | Dashboard won't launch | Streamlit not installed | `pip install streamlit` (included in `selfheal[dev]`) |
| 11 | `sqlite3.OperationalError: database is locked` | Concurrent access to selfheal.db | Close other processes accessing the database |
| 12 | Tests pass but no healing events | Locators didn't break (UI change insufficient) | Verify the attribute you changed is actually used in your locator |
| 13 | `pip install` fails with version error | Python < 3.11 | SelfHeal requires Python 3.11+ |
| 14 | Slow healing (> 5 seconds) | Large DOM with many candidate elements | Expected for pages with 500+ elements — check `max_candidates` in config |

---

## What Happens Next

1. **Submit your results** — send the completed feedback form and JSON export to the pilot coordinator.
2. **Your feedback shapes the roadmap** — every response directly influences which features are prioritised.
3. **Acknowledgement** — participants who consent will be credited in the project's acknowledgements section.

---

## Contact

- **GitHub:** [github.com/Optimus1o1/selfhealing-ui](https://github.com/Optimus1o1/selfhealing-ui)
- **Issues:** [Report a bug](https://github.com/Optimus1o1/selfhealing-ui/issues/new?template=bug_report.yml)
- **Compatibility:** [Report compatibility](https://github.com/Optimus1o1/selfhealing-ui/issues/new?template=compatibility_report.yml)

---

*Moon Sanctum Labs — Decode. Build. Evolve.*

