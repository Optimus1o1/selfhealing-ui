# SelfHeal — Pilot Feedback Form

**Moon Sanctum Labs** — *Decode. Build. Evolve.*  
**Framework Version:** 1.0.0  
**Instructions:** Complete all sections. Rate questions on a 1–5 scale (1 = poor, 5 = excellent). Add free-text notes where indicated.

---

## Participant Information

| Field | Response |
|---|---|
| Participant Code | |
| Date | |
| Operating System | |
| Python Version | |
| Playwright Version | |
| Application Type Tested | |
| Number of Test Files | |
| Number of Locators Tested | |
| Total Time Spent (minutes) | |

---

## Section 1 — Installation Experience

| # | Question | Score (1–5) | Notes |
|---|---|---|---|
| 1.1 | How easy was it to install SelfHeal from the published wheel? | | |
| 1.2 | Were there any dependency conflicts during installation? | | |
| 1.3 | Did the CLI (`selfheal --help`) work immediately after installation? | | |

**Free text:** Describe any installation issues you encountered.

> 

---

## Section 2 — Integration Complexity

| # | Question | Score (1–5) | Notes |
|---|---|---|---|
| 2.1 | How easy was it to integrate `SelfHealingPage` into your existing tests? | | |
| 2.2 | How many lines of code did you need to change per test file? | | |
| 2.3 | Did the integration cause any regressions in existing tests? | | |

**Free text:** Describe the integration process and any difficulties.

> 

---

## Section 3 — API Usability

| # | Question | Score (1–5) | Notes |
|---|---|---|---|
| 3.1 | How intuitive is the `SelfHealingPage` API? | | |
| 3.2 | Did the API behave as you expected from reading the documentation? | | |
| 3.3 | How well does `SelfHealingPage` work as a drop-in replacement for Playwright's `page`? | | |

**Free text:** Any API surprises or suggestions?

> 

---

## Section 4 — Healing Accuracy

| # | Question | Score (1–5) | Notes |
|---|---|---|---|
| 4.1 | When healing triggered, did it select the correct replacement element? | | |
| 4.2 | How many mutations did you test? | | |
| 4.3 | How many healed correctly? | | |
| 4.4 | How many healed incorrectly (false positives)? | | |

**Describe each mutation you tested:**

| Mutation # | What You Changed | Expected Result | Actual Result |
|---|---|---|---|
| 1 | | | |
| 2 | | | |
| 3 | | | |
| 4 | | | |
| 5 | | | |

---

## Section 5 — Rejection Behaviour

| # | Question | Score (1–5) | Notes |
|---|---|---|---|
| 5.1 | When SelfHeal rejected a match (ambiguity), was the rejection appropriate? | | |
| 5.2 | Did SelfHeal ever fail to reject when it should have (multiple similar elements)? | | |

**Free text:** Describe any rejection scenarios.

> 

---

## Section 6 — Execution Performance

| # | Question | Score (1–5) | Notes |
|---|---|---|---|
| 6.1 | How acceptable was the healing latency (time for the test to recover)? | | |
| 6.2 | Did healing noticeably slow down your test suite? | | |

**Measured latency (if available):** _____ ms per healing event

---

## Section 7 — Dashboard Usability

| # | Question | Score (1–5) | Notes |
|---|---|---|---|
| 7.1 | How easy was it to find healing events in the dashboard? | | |
| 7.2 | How clear is the 6-dimension similarity score breakdown? | | |
| 7.3 | Which dashboard sections did you use? | | |

**Sections used (check all that apply):**

- [ ] Overview
- [ ] Live Execution Monitor
- [ ] Healing Analytics
- [ ] Locator Explorer
- [ ] Fingerprint Inspector
- [ ] Intelligence Inspector
- [ ] Audit Centre
- [ ] Baseline Manager
- [ ] Performance Monitor

**Free text:** Dashboard feedback or suggestions.

> 

---

## Section 8 — Feature Requests

**8.1** What is the single most important feature you would want added to SelfHeal?

> 

**8.2** What limitation affected your pilot experience the most?

> 

**8.3** Would you recommend SelfHeal to another QA engineer or developer? Why or why not?

> 

---

## Overall Assessment

| Question | Response |
|---|---|
| Overall satisfaction (1–5) | |
| Would you use SelfHeal in a production CI/CD pipeline? (Yes / No / Maybe) | |
| Biggest strength of SelfHeal | |
| Biggest weakness of SelfHeal | |

---

## Consent

- [ ] I consent to my anonymised feedback being used to improve SelfHeal.
- [ ] I consent to being credited in the project acknowledgements (optional).

**Preferred credit name (optional):** ______

---

*Thank you for participating in the SelfHeal pilot programme.*  
*Moon Sanctum Labs — Decode. Build. Evolve.*

