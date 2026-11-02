# LinkedIn Launch Package: SelfHeal v1.0.0

**Brand:** Moon Sanctum Labs — *Decode. Build. Evolve.*  
**Lead Engineer:** Aniket Nandi (Kolkata, IST)  
**System Version:** `1.0.0` (Stable)  
**Repository:** [github.com/Optimus1o1/selfhealing-ui](https://github.com/Optimus1o1/selfhealing-ui)

---

## 📢 Main Launch Post (Long-Form Technical Post)

```markdown
End-to-end UI tests break constantly in modern CI/CD.

Most of the time, the application isn't broken—a frontend team simply renamed an ID from camelCase to kebab-case, migrated to Tailwind utility classes, or wrapped a button in an extra flex container. 

QA teams spend an estimated 30–40% of their engineering capacity maintaining brittle selectors.

Recent attempts to solve this using cloud LLMs introduce fatal operational flaws: 4-second round-trip latency, non-deterministic hallucinations, high token costs, and dangerous false-positive clicks.

To solve this, I built SelfHeal: a production-grade, deterministic self-healing test automation framework for Microsoft Playwright in Python.

Rather than relying on probabilistic generative models, SelfHeal uses a multi-dimensional mathematical similarity engine running entirely in-process:
1. Multi-Vector Scoring: Evaluates candidate elements across 6 orthogonal dimensions (RapidFuzz text metrics, ARIA roles, Jaccard attribute overlap, parent hierarchy, child layout, and spatial geometry).
2. Action Synonym Ontology: Deterministically recognizes standard UI intent ("Log In" ↔ "Sign In", "Continue to Payment" ↔ "Proceed to Payment") without remote API calls.
3. Two-Tier Mathematical Guardrails: Enforces an absolute confidence threshold (S ≥ 0.80) and an ambiguity margin (Δ ≥ 0.10). If two candidates are too close in score, SelfHeal safely abstains rather than making an unverified guess.
4. Failure Classification Gatekeeper: Differentiates true locator disappearance from actionability defects (disabled, hidden, or invalid selectors) so real application bugs are never masked.
5. Enterprise Governance: Features an embedded SQLite WAL database and a 9-section Streamlit audit dashboard for human-in-the-loop review and baseline promotion.

Across 109 empirical evaluation scenarios (57 baseline + 52 independent holdout scenarios):
• Precision: 100.00% (0 false positive interactions dispatched)
• False Positive Rate: 0.00%
• Recall: 88.89%
• Overall Accuracy: 93.58%
• Algorithmic Scoring Speed: ~3.2 ms per candidate evaluation

The framework wraps Playwright cleanly via proxy composition—no monkey-patching, no global mutation, and zero boilerplate pytest integration (`healed_page` fixture).

SelfHeal v1.0.0 is open-source under the MIT license, backed by 30 automated tests, a 6-job CI matrix, and complete academic documentation.

Check out the code, architecture diagrams, and interactive e-commerce demonstration on GitHub:
🔗 https://github.com/Optimus1o1/selfhealing-ui

Moon Sanctum Labs — Decode. Build. Evolve.
```

---

## 🎥 Short Demonstration Video / GIF Caption

```markdown
Watch Playwright heal broken locators in real time without cloud LLMs or brittle monkey-patching.

In this demonstration:
1. Version 1 captures an element baseline into SQLite.
2. Version 2 introduces severe UI mutations (renamed IDs, changed text, restructured DOM).
3. The exact same test script runs against V2 without code modifications.
4. SelfHeal's deterministic similarity engine detects the absent locator, extracts live candidates, scores them across 6 dimensions in 3.2 ms, and completes the action cleanly.
5. In Scenario F, near-identical payment buttons trigger our ambiguity margin guardrail (Δ < 0.10), safely aborting to prevent an incorrect checkout.

109 scenarios evaluated. 100% precision. 0% false positives.

Full project and case study on GitHub:
👉 https://github.com/Optimus1o1/selfhealing-ui

#Playwright #Python #SoftwareEngineering #TestAutomation #DevOps #QualityEngineering
```

---

## 🖼️ Carousel Slide Deck Copy (5-Slide Visual Summary)

### Slide 1 (Cover)
* **Title:** Why We Replaced LLMs with Deterministic Mathematics for UI Self-Healing
* **Subtitle:** Solving the Brittle Locator Problem in Microsoft Playwright
* **Branding:** Moon Sanctum Labs — *Decode. Build. Evolve.* · Aniket Nandi

### Slide 2 (The Problem)
* **Heading:** The Flaky Test Maintenance Tax
* **Key Points:**
  * 30–40% of QA engineering time is spent diagnosing broken selectors.
  * Minor CSS and ID refactoring breaks automated builds even when functionality works.
  * Cloud LLMs fail: 4-second latency, non-deterministic flakiness, and dangerous false clicks.

### Slide 3 (The Architecture)
* **Heading:** 6-Dimension Deterministic Similarity
* **Key Points:**
  * Text & Accessible Name (30%): RapidFuzz token sorting + UI synonym ontology.
  * Type & ARIA Role (20%): Tag matching and interactive role compatibility.
  * Attributes (20%): Jaccard token set overlap on test IDs and names.
  * Parent Hierarchy (15%): Form affinity and container CSS.
  * Children Subtree (10%): Nested icons, SVGs, and spans.
  * Spatial Position (5%): Viewport-normalized Euclidean distance.
  * **Algorithmic latency: ~3.2 ms local execution.**

### Slide 4 (The Safety Guardrails)
* **Heading:** Zero False Positives by Design
* **Key Points:**
  * **Confidence Threshold:** $S \ge 0.80$ required to consider a candidate.
  * **Ambiguity Margin:** $\Delta \ge 0.10$ gap between #1 and #2 candidate required.
  * **Failure Classifier:** Aborts on disabled/hidden elements so real bugs are never hidden.
  * **Single Safe Retry:** Strict execution limit to eliminate infinite loops.
  * **Result:** $0 / 109$ false positive clicks dispatched ($0.00\%$ FPR).

### Slide 5 (Try It)
* **Heading:** Open Source & Production Ready (v1.0.0)
* **Key Points:**
  * Drop-in Pytest plugin (`healed_page`).
  * 9-section Streamlit governance and audit dashboard.
  * 30/30 automated unit and integration tests passing.
  * MIT License · Available now on GitHub.
* **Link:** `github.com/Optimus1o1/selfhealing-ui`

---

## 🏷️ Technical Hashtags
`#SoftwareEngineering` `#TestAutomation` `#Playwright` `#Python` `#QualityEngineering` `#DevOps` `#ContinuousDelivery` `#OpenSource` `#SoftwareArchitecture` `#RapidFuzz`

