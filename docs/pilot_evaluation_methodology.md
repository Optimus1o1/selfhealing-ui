# SelfHeal — Pilot Evaluation Methodology

**Moon Sanctum Labs** — *Decode. Build. Evolve.*  
**Framework Version:** 1.0.0  
**Document Status:** Methodology defined — awaiting pilot execution

---

## 1. Purpose

This document defines the measurement framework for evaluating SelfHeal's real-world performance during the external pilot programme. All metrics defined here are **strictly separate** from the canonical 109-scenario benchmark and must never be conflated with it.

---

## 2. Canonical Benchmark vs. Pilot Metrics

| Aspect | Canonical Benchmark | Pilot Evaluation |
|---|---|---|
| **Dataset** | 109 controlled scenarios (56 TP, 46 TN, 0 FP, 7 FN) | Real-world applications, variable scenarios |
| **Environment** | Bundled `demo_app/ecommerce.py` V1/V2 | External participant applications |
| **Mutability** | **IMMUTABLE** — never modified | Grows with each pilot participant |
| **Purpose** | Reproducible accuracy measurement | Real-world compatibility validation |
| **Location** | `tests/evaluation/benchmark.py`, `holdout_benchmark.py` | `docs/real_world_pilot_report.md` (results section) |

> **Rule:** Pilot results are NEVER merged into the canonical benchmark. They are reported separately and used to identify compatibility gaps and improvement priorities.

---

## 3. Primary Metrics

### 3.1 Pilot Precision

$$\text{Pilot Precision} = \frac{\text{Correct Healings}}{\text{Total Healing Attempts}}$$

- **Correct healing:** The replacement element is functionally equivalent to the original.
- **Incorrect healing (false positive):** The replacement element is a different, unrelated element.
- **Collection method:** Manual review of each healing event in the dashboard Audit Centre.
- **Target:** ≥ 95% (relaxed from canonical 100% given uncontrolled environments).

### 3.2 Pilot Recall

$$\text{Pilot Recall} = \frac{\text{Successful Healings}}{\text{Total Eligible Failures}}$$

- **Eligible failure:** A locator failure caused by a UI mutation where the correct replacement element exists in the DOM.
- **Ineligible failure:** Element genuinely removed, hidden, or disabled (actionability failure).
- **Collection method:** Participant's mutation checklist cross-referenced with healing event log.
- **Target:** ≥ 80%.

### 3.3 False Positive Rate

$$\text{FPR} = \frac{\text{Incorrect Healings}}{\text{Total Negative Cases}}$$

- **Negative case:** A scenario where healing should NOT occur (ambiguous, element removed, actionability failure).
- **Collection method:** Dashboard audit trail review.
- **Target:** ≤ 2%.

### 3.4 Abstention Rate

$$\text{Abstention Rate} = \frac{\text{Rejected Ambiguous Matches}}{\text{Total Eligible Failures}}$$

- **Rejected ambiguous:** Score margin below 0.10 threshold.
- High abstention indicates conservative safety but may frustrate users.
- **Target range:** 5–15% (too low suggests insufficient safety; too high suggests overly conservative thresholds).

### 3.5 Healing Latency

| Tier | Measurement | Collection Method |
|---|---|---|
| Pure algorithm scoring | Time for `SimilarityScorer.score()` | Performance logs |
| Decision engine | Time for threshold + margin evaluation | Performance logs |
| DOM extraction | Time for `DOMScanner` JavaScript execution | Performance logs |
| End-to-end healing | Total time from failure detection to successful retry | Playwright trace timing |

**Target:** End-to-end healing ≤ 5 seconds (including configurable timeout).

### 3.6 Integration Time

| Phase | Measurement |
|---|---|
| Installation | Time from `pip install` to `selfheal --help` success |
| Code integration | Time from first code change to first test run with `SelfHealingPage` |
| Baseline creation | Time from first wrapped test run to confirmed baseline entries |
| First healing | Time from UI mutation to first observed healing event |
| Total | Sum of all phases |

**Collection method:** Participant self-report with stopwatch.  
**Target:** Total ≤ 40 minutes for a developer familiar with Playwright.

### 3.7 Developer Feedback Score

Composite score from the [Developer Experience Evaluation](developer_experience_evaluation.md) methodology:

| Dimension | Weight |
|---|---|
| Installation complexity | 10% |
| Integration complexity | 20% |
| Configuration clarity | 10% |
| API usability | 20% |
| Error message quality | 15% |
| Dashboard usability | 15% |
| Documentation quality | 10% |

**Weighted DX Score** = Σ (dimension score × weight)  
**Target:** ≥ 3.5 / 5.0

---

## 4. Data Collection Protocol

### Per-Participant Collection

For each pilot participant, record:

```yaml
participant:
  id: "P001"
  application_type: ""
  framework: ""
  os: ""
  python_version: ""
  playwright_version: ""
  selfheal_version: "1.0.0"
  date: ""

mutations:
  total_attempted: 0
  eligible_failures: 0
  healing_attempts: 0
  correct_healings: 0
  incorrect_healings: 0
  rejected_ambiguous: 0
  not_triggered: 0

timing:
  installation_minutes: 0
  integration_minutes: 0
  baseline_creation_minutes: 0
  first_healing_minutes: 0

feedback:
  installation_score: 0  # 1-5
  integration_score: 0
  configuration_score: 0
  api_score: 0
  error_message_score: 0
  dashboard_score: 0
  documentation_score: 0
  would_recommend: false
  top_improvement: ""
```

### Aggregate Reporting

After collecting data from ≥ 3 participants, compute:

| Metric | Formula |
|---|---|
| Aggregate Precision | Total correct healings / total healing attempts (all participants) |
| Aggregate Recall | Total successful healings / total eligible failures |
| Aggregate FPR | Total incorrect / total negatives |
| Mean Abstention Rate | Average abstention rate across participants |
| Mean Integration Time | Average total integration time |
| Mean DX Score | Weighted average across all dimensions and participants |
| Compatibility Coverage | Number of distinct application types successfully tested |

---

## 5. Reporting Format

Pilot results are reported in [Real-World Pilot Report](real_world_pilot_report.md) using this structure:

1. **Per-participant summary table** (anonymised if requested)
2. **Aggregate metric table** with targets and actual values
3. **Compatibility matrix** (application type × healing success rate)
4. **Top failure modes** (ranked by frequency)
5. **Improvement recommendations** (prioritised by impact)

---

## 6. Results

> **Status: PENDING**
>
> No pilot data has been collected. This section will be populated after the first pilot participant completes the evaluation protocol.

---

*Moon Sanctum Labs — Decode. Build. Evolve.*
