# SelfHeal — Developer Experience Evaluation Methodology

**Moon Sanctum Labs** — *Decode. Build. Evolve.*  
**Framework Version:** 1.0.0  
**Document Status:** Methodology template — no fabricated findings

---

## 1. Purpose

This document defines a structured methodology for evaluating the developer experience (DX) of integrating and using SelfHeal. The evaluation measures seven dimensions of usability across a standardised task-based protocol.

All scoring rubrics and interview questions are defined here. **No results have been fabricated.** Result sections are populated only after real participants complete the evaluation.

---

## 2. Evaluation Dimensions

### 2.1 Installation Complexity

*How difficult is it to install SelfHeal and its dependencies?*

| Score | Criteria |
|---|---|
| 5 — Trivial | Single `pip install` command, no additional setup |
| 4 — Easy | Install + one additional step (e.g., `playwright install chromium`) |
| 3 — Moderate | Requires reading documentation to resolve a dependency issue |
| 2 — Difficult | Multiple attempts needed, error messages not self-explanatory |
| 1 — Blocking | Could not install without direct assistance |

**Evaluation tasks:**
1. Install SelfHeal from PyPI (or wheel) in a clean virtual environment.
2. Verify the CLI works: `selfheal --help`.
3. Record time from start to successful verification.

---

### 2.2 Integration Complexity

*How difficult is it to integrate SelfHeal into an existing Playwright test suite?*

| Score | Criteria |
|---|---|
| 5 — Drop-in | Only 1–2 lines of code changed per test file |
| 4 — Easy | Minor refactoring (import + page wrapper), no logic changes |
| 3 — Moderate | Required reading docs to understand wrapper pattern |
| 2 — Difficult | Had to restructure test architecture (fixtures, conftest) |
| 1 — Blocking | Could not integrate without direct assistance |

**Evaluation tasks:**
1. Wrap an existing Playwright `page` with `SelfHealingPage`.
2. Run the existing test suite unchanged.
3. Confirm all tests still pass (no regressions from wrapping).
4. Record number of files modified and lines changed.

---

### 2.3 Configuration Clarity

*How clear and well-documented are SelfHeal's configuration options?*

| Score | Criteria |
|---|---|
| 5 — Self-explanatory | Default config works perfectly, options clearly documented |
| 4 — Clear | Needed to read config docs once, then fully understood |
| 3 — Adequate | Some options required experimentation to understand |
| 2 — Confusing | Config structure unclear, had to read source code |
| 1 — Opaque | Could not determine what configuration options exist |

**Evaluation tasks:**
1. Locate and read the default configuration (`configs/default.yaml`).
2. Modify one threshold (e.g., `minimum_similarity_score`).
3. Verify the modified threshold affects healing behaviour.

---

### 2.4 API Usability

*How intuitive is SelfHeal's public API?*

| Score | Criteria |
|---|---|
| 5 — Pythonic | API follows Python conventions, IDE autocomplete works |
| 4 — Clean | Clear method names, minimal surprises |
| 3 — Adequate | Some methods require documentation lookup |
| 2 — Awkward | Method signatures or return types feel inconsistent |
| 1 — Confusing | Could not determine how to use the API without examples |

**Evaluation tasks:**
1. Create a `SelfHealingPage` instance.
2. Call `page.click()`, `page.fill()`, and `page.locator()`.
3. Access healing event data programmatically.
4. Rate whether the API felt natural compared to standard Playwright.

---

### 2.5 Error Message Quality

*How helpful are SelfHeal's error messages and log output?*

| Score | Criteria |
|---|---|
| 5 — Actionable | Error messages explain what went wrong and suggest a fix |
| 4 — Clear | Error messages identify the problem clearly |
| 3 — Adequate | Error messages point to the right area but lack specifics |
| 2 — Vague | Error messages are generic or misleading |
| 1 — Silent | Failures occur without any diagnostic output |

**Evaluation tasks:**
1. Trigger a healing event and review the console output.
2. Trigger an ambiguity rejection and review the log message.
3. Attempt an operation that should fail (e.g., element genuinely removed) and review the error.

---

### 2.6 Dashboard Usability

*How effective is the Streamlit monitoring dashboard?*

| Score | Criteria |
|---|---|
| 5 — Excellent | All sections intuitive, data immediately useful |
| 4 — Good | Most sections clear, minor navigation confusion |
| 3 — Adequate | Needed time to understand the layout and data meaning |
| 2 — Confusing | Section purposes unclear, data hard to interpret |
| 1 — Unusable | Could not extract useful information from the dashboard |

**Evaluation tasks:**
1. Launch the dashboard: `streamlit run -m selfheal.dashboard.app`.
2. Navigate to each of the 9 sections.
3. Locate a specific healing event in the Healing Analytics section.
4. Inspect the 6-dimension score breakdown in the Intelligence Inspector.
5. Rate overall data clarity and navigation.

---

### 2.7 Documentation Quality

*How complete and accurate is the project documentation?*

| Score | Criteria |
|---|---|
| 5 — Comprehensive | All questions answered by documentation alone |
| 4 — Good | Most questions answered, minor gaps |
| 3 — Adequate | Core concepts covered, some advanced topics missing |
| 2 — Sparse | Had to read source code to understand key concepts |
| 1 — Insufficient | Documentation missing or misleading |

**Evaluation tasks:**
1. Follow the README quickstart without any external help.
2. Find the answer to "How does SelfHeal decide when NOT to heal?" in the docs.
3. Find the answer to "What similarity dimensions are used?" in the docs.
4. Rate whether the documentation matched the actual framework behaviour.

---

## 3. Task-Based Evaluation Protocol

Each participant follows this standardised protocol:

| Step | Task | Time Limit | Measured Outcome |
|---|---|---|---|
| 1 | Install SelfHeal in a clean virtualenv | 10 min | Success/fail, time taken |
| 2 | Integrate into an existing test (or demo app) | 15 min | Files changed, lines changed |
| 3 | Create a baseline by running tests | 5 min | Baseline entries created |
| 4 | Mutate the UI (change 1 attribute) | 5 min | Mutation applied |
| 5 | Run the unchanged test | 5 min | Healing triggered (yes/no) |
| 6 | Verify healing via CLI | 5 min | Correct element healed |
| 7 | Verify healing via dashboard | 10 min | Dashboard data accurate |
| 8 | Modify a configuration threshold | 5 min | Config change applied |
| 9 | Complete the feedback questionnaire | 10 min | All dimensions scored |

**Total estimated time:** 60–70 minutes per participant.

---

## 4. Structured Interview Questions

After the task-based evaluation, conduct a 10–15 minute semi-structured interview:

1. What was your first impression of SelfHeal?
2. At what point (if any) did you feel stuck?
3. How does SelfHeal compare to other test stability tools you have used?
4. What would you change about the integration process?
5. Did the framework ever do something unexpected?
6. How confident are you that the healed locators are correct?
7. Would you trust SelfHeal in a CI/CD pipeline?
8. What is the single most important improvement you would suggest?
9. Would you recommend SelfHeal to another QA engineer?
10. Any concerns about the deterministic (non-LLM) approach?

---

## 5. Aggregate Scoring

After collecting responses from all participants, compute:

| Metric | Formula |
|---|---|
| Mean dimension score | Average of all participants' scores per dimension |
| Overall DX score | Average across all 7 dimensions |
| Net Promoter Score (NPS) | % promoters (9–10) minus % detractors (0–6) on Q10 of feedback |
| Task completion rate | % of participants who completed all 9 protocol steps |
| Mean integration time | Average time for Steps 1–5 |

**Target thresholds for 1.0.0:**

| Metric | Target |
|---|---|
| Overall DX score | ≥ 3.5 / 5.0 |
| Task completion rate | ≥ 80% |
| Mean integration time | ≤ 40 minutes |

---

## 6. Results

> **Status: PENDING**
>
> No pilot evaluation has been conducted yet. This section will be populated with actual participant data after the pilot programme completes.

---

*Moon Sanctum Labs — Decode. Build. Evolve.*
