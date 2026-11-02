# 5–7 Minute Academic Demonstration & Defense Presentation Script

**Moon Sanctum Labs** — *Decode. Build. Evolve.*  
**Lead Engineer & Presenter:** Aniket Nandi (Kolkata, IST)  
**System Version:** `1.0.0` (Stable)  
**Duration:** 6 Minutes (Target Range: 5:00 – 7:00 Minutes)  

---

## Technical Demonstration Setup Checklist (Before Starting)
1. **Terminal 1:** Ready in workspace root `c:\Users\ANIKET\OneDrive\Documents\SelfHealing_UI`.
2. **Terminal 2:** Streamlit Dashboard command pre-typed: `streamlit run src/selfheal/dashboard/app.py`.
3. **Browser Window:** Chrome/Edge open at `http://localhost:8501`.
4. **Clean Baseline:** Database cleanly initialized (`artifacts/selfheal.db`).

---

## Timed Presentation Script

```
00:00 - 00:45 | 1. Introduction & The Problem of Brittle Locators
00:45 - 01:30 | 2. System Architecture & Deterministic Heuristics
01:30 - 02:45 | 3. Live Demonstration: Baseline & Autonomous Healing
02:45 - 03:45 | 4. Live Demonstration: Guardrails & Ambiguity Rejection
03:45 - 05:00 | 5. Streamlit Audit Dashboard & Human Governance
05:00 - 06:00 | 6. Empirical Results, Latency Budget & Conclusion
```

---

### Segment 1: Introduction & Problem Statement [00:00 – 00:45]
- **Visual Cue:** Title Slide / Terminal Header showing `Moon Sanctum Labs — Decode. Build. Evolve.`
- **Spoken Narration:**
  > "Respected committee members, good morning. I am Aniket Nandi, presenting **SelfHeal**, a production-grade, deterministic self-healing test automation framework for Microsoft Playwright.
  >
  > In modern continuous delivery, end-to-end web testing is plagued by the **brittle locator problem**. Routine aesthetic refactoring—such as migrating from custom CSS to Tailwind, reorganizing DOM trees for responsive layouts, or updating copy—breaks automated test suites, even though the application's underlying business logic remains 100% functional. 
  >
  > Existing commercial tools often rely on non-deterministic cloud LLMs or pixel-based computer vision, which introduce unacceptable latency, token costs, and privacy risks. SelfHeal solves this problem deterministically using a multi-dimensional string, structural, and spatial vector similarity model that operates entirely in-browser in under 3 milliseconds."

---

### Segment 2: Architecture Overview [00:45 – 01:30]
- **Visual Cue:** Architecture Diagram (Figure from `docs/architecture_diagrams.md`).
- **Spoken Narration:**
  > "The architecture comprises five distinct layers:
  > 1. **Execution Layer:** A clean wrapper around Playwright's `Page` and `Locator` APIs, requiring zero monkey-patching and preserving 100% of native test patterns.
  > 2. **Detection Layer:** A failure triage engine that differentiates true locator disappearance from actionability defects like hidden or disabled elements.
  > 3. **Intelligence Layer:** An in-browser JavaScript extractor coupled with RapidFuzz string metrics, UI synonym ontologies, ARIA accessibility blending, and spatial proximity.
  > 4. **Persistence Layer:** An embedded SQLite database running in Write-Ahead Logging (WAL) mode, providing versioned baseline management and full audit history.
  > 5. **Governance Layer:** A 9-section Streamlit engineering dashboard providing human-in-the-loop audit sign-off."

---

### Segment 3: Live Demonstration — Baseline & Autonomous Healing [01:30 – 02:45]
- **Action Cue:** Execute the autonomous demonstration runner in Terminal 1:
  ```powershell
  python scripts/run_academic_demo.py
  ```
- **Spoken Narration:**
  > "I will now run our live demonstration suite against a realistic multi-page e-commerce application.
  >
  > In Phase 1, the test suite executes against **Version 1** of our application. As you can see in the terminal, the framework captures an initial multi-dimensional element fingerprint before interacting with each element—storing the tag, classes, accessible name, parent hierarchy, and bounding box.
  >
  > Now, in Phase 2, the application is upgraded to **Version 2**. In Version 2:
  > - The login button `#btnLogin` has been renamed to `#btnSignInSubmit` with Tailwind utility classes.
  > - The button text mutated from 'Login' to 'Sign In'.
  > - In the product catalog, three identical 'Add to Bag' buttons exist side-by-side.
  > - The checkout page has been completely restructured into nested fieldsets.
  >
  > Notice something crucial: **the Playwright test script was not modified by even a single character.** 
  > 
  > As the locator fails, SelfHeal intercepts the timeout. It extracts candidates in 2.3 milliseconds, scores them, confirms the score exceeds our 0.80 threshold, verifies that exactly one element matches the synthesized selector, and executes the click. All four broken locators across authentication, catalog, cart, and checkout are successfully repaired with an average score above 0.84!"

---

### Segment 4: Live Demonstration — Safety Guardrails & Ambiguity Rejection [02:45 – 03:45]
- **Visual Cue:** Terminal output highlighting `REJECTED_AMBIGUOUS_MATCH` and `REJECTED_ACTIONABILITY`.
- **Spoken Narration:**
  > "Self-healing is only viable if it is safe. In test automation, a **false positive** click is disastrous. Our framework introduces two hard mathematical guardrails:
  >
  > 1. **Ambiguity Margin Protection:** On our payment selection screen, two near-tie buttons—`#payMethodOption1` and `#payMethodOption2`—score 0.8769 and 0.8720. Because the score difference is only 0.0049—well below our required 0.10 margin—the engine refuses to guess and cleanly rejects the repair.
  > 2. **Actionability Guardrail:** On the express checkout button, the element exists in the DOM but is disabled. Our failure classifier recognizes this as `ELEMENT_DISABLED`, immediately aborting the test without attempting to heal.
  >
  > This is why SelfHeal achieves a **0.00% False Positive Rate** across all benchmarks."

---

### Segment 5: Streamlit Audit Dashboard & Human Governance [03:45 – 05:00]
- **Action Cue:** Switch to the browser at `http://localhost:8501`.
- **Spoken Narration:**
  > "Let us now inspect the live system via our 9-section Streamlit Audit Dashboard.
  >
  > - In **Overview**, we see live KPIs directly queried from SQLite: 100% healing success rate, total runs, and latency.
  > - In **Fingerprint Inspector**, we can select any healed element and view a side-by-side DOM attribute diff highlighting attributes as `MATCHED`, `CHANGED`, or `NEW`.
  > - In **Intelligence Inspector**, we provide complete algorithmic transparency. For every decision, we visualize the exact 6-dimension breakdown: Text 30%, Tag/Role 20%, Attributes 20%, Parent 15%, Children 10%, Geometry 5%.
  > - In **Audit Centre**, we enforce strict human-in-the-loop governance. A healed locator remains in `pending_review` until an authorized QA engineer inspects it. Notice that the 'Approve & Promote to V2' button is strictly disabled until I check this mandatory confirmation box. Clicking promote advances the baseline to Version 2 in our SQLite WAL log."

---

### Segment 6: Empirical Results, Latency Budget & Conclusion [05:00 – 06:00]
- **Visual Cue:** Performance Monitor Tab / Final Results Table.
- **Spoken Narration:**
  > "Finally, let us review our empirical benchmark results:
  > - Across **109 independent mutation scenarios** (combining our 57-case baseline and 52-case unseen holdout suite), SelfHeal achieved **100.00% Precision**, **0.00% False Positive Rate**, **87.30% Recall**, and **92.66% Overall Accuracy**.
  > - Across 500+ profiling iterations, pure algorithm scoring took just **0.69 milliseconds**, and DOM extraction took **2.30 milliseconds**. The 3-second total healing time is dominated by Playwright's native action timeout (81.37%) and SPA dynamic grace wait (16.27%). By tuning the timeout to 1 second, healing completes in **1.57 seconds**—a 48.8% latency reduction.
  >
  > In conclusion, SelfHeal proves that deterministic heuristics can eliminate test brittleness with zero cloud dependencies, sub-millisecond scoring, and zero false positives.
  >
  > Thank you. I am now open to questions from the committee."

