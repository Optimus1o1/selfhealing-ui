# Google Flow Video Generation Kit: SelfHeal v1.0.0

**Project:** SelfHeal — Intelligent Self-Healing UI Automation Framework for Playwright  
**Brand:** Moon Sanctum Labs — *Decode. Build. Evolve.*  
**Lead Engineer:** Aniket Nandi (Kolkata, IST)  
**Target Video Duration:** 3:30 Minutes (9 Curated Scenes)  
**Style & Aesthetic:** Cinematic Dark Tech Minimalist (Ink `#0F1013`, Bone `#F2EFE8`, Copper `#E0A45C`, Slate `#8B9099`)  
**Resolution:** 1080p60 / 1440p60 (16:9 Widescreen)

---

## 🤖 Master Prompt for Google Flow / Google Vids Project Initialization

Copy and paste this master context prompt into Google Flow / Google Vids to establish global project style, voice, pacing, and visual assets:

```text
Create a cinematic, high-production-value engineering product video for "SelfHeal" (v1.0.0), a deterministic self-healing test automation framework for Microsoft Playwright in Python built by Moon Sanctum Labs (Tagline: "Decode. Build. Evolve.").

VISUAL STYLE & PALETTE:
- Premium engineering dark mode. Deep Obsidian/Ink (#0F1013), crisp Bone White (#F2EFE8), glowing warm Copper (#E0A45C) for interactive highlights, and Slate Grey (#8B9099) for secondary data.
- Crisp typography: Space Grotesk for bold architectural titles, Manrope for telemetry and UI text.
- Screen layouts: 60/40 split-screens (Terminal/Code on left, Live Web Browser/Dashboard on right), smooth floating camera dollying, subtle glassmorphic bezels, and 60fps micro-animations.
- Avoid generic stock video clips. Rely on authentic technical assets: terminal outputs with colored syntax, live Playwright browser interactions, SVG architectural workflows, and real Streamlit audit dashboard screens.

AUDIO & PACING:
- Pacing: Confident, fast-paced, authoritative, senior-engineer tone. No marketing fluff or hyperbolic buzzwords.
- Music: Low-frequency rhythmic electronic synth / ambient tech pulse (110–120 BPM) that dips automatically beneath voiceover.
- Voiceover Persona: Deep, calm, articulate, professional engineering narration (neutral global or British/Indian English accent).

KEY NARRATIVE THREAD:
Traditional UI tests break constantly during routine frontend redesigns (wasting 30-40% of QA time). Cloud LLMs fail in CI/CD due to 4-second latency, hallucinations, token costs, and dangerous false positive clicks. SelfHeal solves this deterministically with sub-millisecond RapidFuzz vector scoring, zero false positives (100% precision across 109 benchmark scenarios), and a 9-section Streamlit governance dashboard.
```

---

## 🎬 Scene-by-Scene Generation Prompts, Resources & Narration Scripts

---

### Scene 1: The Hook — The Brittle Locator Tax [00:00 – 00:25]
* **Scene Objective:** Establish the widespread pain point of test maintenance and red CI pipelines caused by benign UI changes.
* **Duration:** 25 seconds
* **Exact Asset / Resource to Feed:**
  * File: [`docs/assets/demo/03_scenario_b_v2_login_mutated.png`](file:///c:/Users/ANIKET/OneDrive/Documents/SelfHealing_UI/docs/assets/demo/03_scenario_b_v2_login_mutated.png)
  * File: [`docs/assets/diagrams/architecture_overview.svg`](file:///c:/Users/ANIKET/OneDrive/Documents/SelfHealing_UI/docs/assets/diagrams/architecture_overview.svg)
* **Prompt for Google Flow:**
  ```text
  Cinematic slow zoom into a dark engineering terminal in an aesthetic developer workstation. The terminal screen flashes red with a Playwright timeout error: "TimeoutError: locator.click: Timeout 2500ms exceeded on selector #btnLogin". In the background, a modern software dashboard shows automated build pipelines failing. Overlay clean typography in copper (#E0A45C): "30–40% OF QA ENGINEERING CAPACITY IS LOST TO BRITTLE LOCATORS". Transition with a clean horizontal wipe to an e-commerce login page undergoing redesign.
  ```
* **Voiceover Script:**
  > *"Every test automation engineer knows the frustration of flaky end-to-end builds. A frontend team renames a button ID from kebab-case to camelCase, tweaks text from 'Log In' to 'Sign In', or wraps an input in a new container—and instantly, your entire CI pipeline fails.*
  >
  > *Teams waste over thirty percent of their sprint capacity fixing broken selectors on code that isn't actually broken."*

---

### Scene 2: The Fallacy of LLMs vs. Deterministic Intelligence [00:25 – 00:50]
* **Scene Objective:** Contrast slow, hallucination-prone cloud LLMs against SelfHeal's sub-millisecond local vector similarity.
* **Duration:** 25 seconds
* **Exact Asset / Resource to Feed:**
  * File: [`docs/assets/diagrams/feature_weights.svg`](file:///c:/Users/ANIKET/OneDrive/Documents/SelfHealing_UI/docs/assets/diagrams/feature_weights.svg)
* **Prompt for Google Flow:**
  ```text
  Split screen comparison graphic on a dark obsidian (#0F1013) background. Left side labeled "Cloud LLM Approach" in dull red: shows an API loading spinner taking 4.2 seconds, a high token billing counter ticking up, and a hallucinated click on the wrong button. Right side labeled "SelfHeal Deterministic Engine" in luminous copper (#E0A45C): shows a clean mathematical vector calculation resolving in 3.2 milliseconds with 100% precision. Zoom into the feature weight chart displaying the 6 dimensions: Text (30%), Role (20%), Attributes (20%), Parent (15%), Children (10%), and Position (5%).
  ```
* **Voiceover Script:**
  > *"Recent tools attempt to solve this with cloud LLMs, but generative AI introduces fatal flaws in production CI: four-second API latency, expensive token consumption, and dangerous false positive clicks.*
  >
  > *In automated testing, clicking the wrong button is catastrophic.*
  >
  > *SelfHeal replaces probabilistic guesswork with deterministic mathematics: a multi-dimensional vector similarity engine running locally in three milliseconds."*

---

### Scene 3: System Architecture & Non-Invasive Proxying [00:50 – 01:15]
* **Scene Objective:** Showcase the 4-tier clean architecture without monkey-patching.
* **Duration:** 25 seconds
* **Exact Asset / Resource to Feed:**
  * File: [`docs/assets/diagrams/architecture_overview.svg`](file:///c:/Users/ANIKET/OneDrive/Documents/SelfHealing_UI/docs/assets/diagrams/architecture_overview.svg)
* **Prompt for Google Flow:**
  ```text
  Animate a 4-tier isometric architectural schematic on a deep slate background. Glowing copper tracer lines flow between Tier 1 (Test Execution Layer with SelfHealingPage proxy), Tier 2 (Failure Classifier and In-Browser DOM Scanner), Tier 3 (Similarity Engine with RapidFuzz and Decision Gating), and Tier 4 (SQLite WAL Repository and Streamlit Dashboard). Highlight the code snippet showing zero monkey-patching: "sh_page = SelfHealingPage(page)".
  ```
* **Voiceover Script:**
  > *"SelfHeal operates through clean proxy composition—wrapping Playwright's Page and Locator interfaces with zero monkey-patching.*
  >
  > *The architecture separates execution, triage, scoring, and audit into four isolated layers, backed by an embedded SQLite Write-Ahead Logging database that stores versioned element baselines with complete privacy redaction."*

---

### Scene 4: Version 1 Baseline Capture [01:15 – 01:40]
* **Scene Objective:** Demonstrate normal test execution capturing baseline element fingerprints.
* **Duration:** 25 seconds
* **Exact Asset / Resource to Feed:**
  * File: [`docs/assets/demo/01_scenario_a_v1_login_baseline.png`](file:///c:/Users/ANIKET/OneDrive/Documents/SelfHealing_UI/docs/assets/demo/01_scenario_a_v1_login_baseline.png)
  * File: [`docs/assets/demo/02_scenario_a_v1_checkout_baseline.png`](file:///c:/Users/ANIKET/OneDrive/Documents/SelfHealing_UI/docs/assets/demo/02_scenario_a_v1_checkout_baseline.png)
* **Prompt for Google Flow:**
  ```text
  Split screen layout. On the left: a dark terminal running "python scripts/run_academic_demo.py --headed". On the right: a live Chromium browser navigating the e-commerce demo at Version 1. As the test clicks the "#btnLogin" button, a glowing copper bounding box highlights the button, and a visual HUD overlay animates the capture of a 10-dimensional DOM fingerprint (tag, classes, accessible name, parent ID, geometry) into SQLite. Terminal outputs green: "[BASELINE CAPTURED] Target 'auth.login_submit'".
  ```
* **Voiceover Script:**
  > *"During initial test runs on Version 1 of your application, SelfHeal passively captures a comprehensive 10-dimensional DOM fingerprint of every target element—recording text, ARIA roles, test IDs, container hierarchy, and spatial bounding boxes.*
  >
  > *Passwords and authentication tokens are automatically sanitized before persistence, ensuring zero sensitive data exposure."*

---

### Scene 5: Version 2 Mutation & Autonomous Self-Healing [01:40 – 02:10]
* **Scene Objective:** Show the core self-healing capability when the application DOM undergoes severe refactoring.
* **Duration:** 30 seconds
* **Exact Asset / Resource to Feed:**
  * File: [`docs/assets/demo/03_scenario_b_v2_login_mutated.png`](file:///c:/Users/ANIKET/OneDrive/Documents/SelfHealing_UI/docs/assets/demo/03_scenario_b_v2_login_mutated.png)
  * File: [`docs/assets/demo/04_scenario_b_v2_login_healed_success.png`](file:///c:/Users/ANIKET/OneDrive/Documents/SelfHealing_UI/docs/assets/demo/04_scenario_b_v2_login_healed_success.png)
* **Prompt for Google Flow:**
  ```text
  Dynamic before-and-after UI transition. Show the application upgraded to Version 2: the login button ID is renamed from "#btnLogin" to "#sign-in-btn", text is altered to "Sign In", and styling switched to Tailwind CSS. The test runner encounters the broken locator. The failure classifier confirms locator absence, triggers in-browser DOM extraction in 2.1 milliseconds, and computes RapidFuzz similarity scores. Show the score badge: "Score: 0.8640 >= 0.80". The browser retries automatically and completes authentication. Display green banner: "AUTONOMOUS HEALING SUCCESSFUL".
  ```
* **Voiceover Script:**
  > *"When Version 2 deploys, the DOM changes completely: new IDs, modernized classes, and altered copy.*
  >
  > *Without changing a single line of test code, the original script executes against Version 2.*
  >
  > *When '#btnLogin' times out, SelfHeal's Failure Classifier confirms the element is truly absent, extracts live DOM candidates in two milliseconds, and matches the replacement button with an 86.4% confidence score.*
  >
  > *SelfHeal executes a single safe retry, and your test suite passes without human intervention."*

---

### Scene 6: Candidate Disambiguation in Complex Grids [02:10 – 02:30]
* **Scene Objective:** Demonstrate disambiguation when multiple identical buttons exist on a page.
* **Duration:** 20 seconds
* **Exact Asset / Resource to Feed:**
  * File: [`docs/assets/demo/05_scenario_e_catalog_grid_candidates.png`](file:///c:/Users/ANIKET/OneDrive/Documents/SelfHealing_UI/docs/assets/demo/05_scenario_e_catalog_grid_candidates.png)
  * File: [`docs/assets/demo/06_scenario_e_catalog_item_added_to_cart.png`](file:///c:/Users/ANIKET/OneDrive/Documents/SelfHealing_UI/docs/assets/demo/06_scenario_e_catalog_item_added_to_cart.png)
* **Prompt for Google Flow:**
  ```text
  Camera focuses on a multi-card e-commerce product catalog displaying three identical "Add to Bag" buttons. Visual HUD markers highlight all three candidate buttons. The AI scanner analyzes the enclosing card hierarchy and accessible name to isolate the exact intended product ("Voyager Tech Pack"). The target card highlights in copper, the button clicks smoothly, and the shopping cart badge updates to 1. Overlay text: "CONTEXTUAL PARENT DISAMBIGUATION".
  ```
* **Voiceover Script:**
  > *"What happens when multiple identical buttons exist on a page?*
  >
  > *In complex product grids, SelfHeal uses enclosing parent context and accessible names to disambiguate identical buttons, ensuring the exact intended item is selected without misclicks."*

---

### Scene 7: Zero False Positives — Mathematical Guardrails [02:30 – 02:55]
* **Scene Objective:** Prove that SelfHeal prevents false positive clicks through margin gating and failure classification.
* **Duration:** 25 seconds
* **Exact Asset / Resource to Feed:**
  * File: [`docs/assets/demo/09_scenario_f_ambiguous_candidates.png`](file:///c:/Users/ANIKET/OneDrive/Documents/SelfHealing_UI/docs/assets/demo/09_scenario_f_ambiguous_candidates.png)
  * File: [`docs/assets/demo/10_scenario_g_disabled_target.png`](file:///c:/Users/ANIKET/OneDrive/Documents/SelfHealing_UI/docs/assets/demo/10_scenario_g_disabled_target.png)
  * File: [`docs/assets/diagrams/healing_workflow.svg`](file:///c:/Users/ANIKET/OneDrive/Documents/SelfHealing_UI/docs/assets/diagrams/healing_workflow.svg)
* **Prompt for Google Flow:**
  ```text
  Split screen demonstrating two negative safety controls. Left panel (Scenario F): Two competing payment buttons ("Pay with Card" vs "Pay with Debit") score within 0.027 of each other. An alert badge appears: "AMBIGUITY MARGIN VIOLATION: Delta 0.027 < 0.10 -> REJECTED". Right panel (Scenario G): A checkout button is disabled. Failure classifier flags "ELEMENT_DISABLED" and halts healing immediately. Overlay headline: "100.00% PRECISION · 0.00% FALSE POSITIVE RATE (109 SCENARIOS)".
  ```
* **Voiceover Script:**
  > *"SelfHeal guarantees zero false positive interactions through two mathematical guardrails.*
  >
  > *First, the Ambiguity Margin: if two candidates score within 0.10 of each other, SelfHeal safely abstains rather than making an unverified guess.*
  >
  > *Second, Actionability Triage: if an element is disabled or hidden, it is flagged as an application defect, ensuring genuine bugs are never masked.*
  >
  > *Across 109 empirical evaluation scenarios, our observed False Positive Rate is exactly zero percent."*

---

### Scene 8: Streamlit Engineering Audit Dashboard [02:55 – 03:20]
* **Scene Objective:** Showcase the 9-section governance portal, dimensional radar, DOM diff, and one-click V2 baseline promotion.
* **Duration:** 25 seconds
* **Exact Asset / Resource to Feed:**
  * File: [`docs/assets/dashboard/01_overview.png`](file:///c:/Users/ANIKET/OneDrive/Documents/SelfHealing_UI/docs/assets/dashboard/01_overview.png)
  * File: [`docs/assets/dashboard/06_intelligence_inspector.png`](file:///c:/Users/ANIKET/OneDrive/Documents/SelfHealing_UI/docs/assets/dashboard/06_intelligence_inspector.png)
  * File: [`docs/assets/dashboard/07_audit_centre.png`](file:///c:/Users/ANIKET/OneDrive/Documents/SelfHealing_UI/docs/assets/dashboard/07_audit_centre.png)
  * File: [`docs/assets/dashboard/09_performance_monitor.png`](file:///c:/Users/ANIKET/OneDrive/Documents/SelfHealing_UI/docs/assets/dashboard/09_performance_monitor.png)
* **Prompt for Google Flow:**
  ```text
  Smooth cinematic dolly across the dark-themed Streamlit Engineering Dashboard. Quick cuts between: (1) Overview KPIs showing total test runs and latency percentiles; (2) Intelligence Inspector showing the 6-dimension score breakdown bar chart; (3) Fingerprint Inspector with color-coded side-by-side DOM attribute diff; and (4) Audit Centre where a QA engineer checks the safety confirmation box and clicks "Approve & Promote to V2". Show the locator committed as the new permanent baseline.
  ```
* **Voiceover Script:**
  > *"For engineering governance, SelfHeal provides a comprehensive 9-section Streamlit audit dashboard.*
  >
  > *In the Intelligence Inspector, QA leads can inspect dimensional score breakdowns for every healed interaction.*
  >
  > *In the Audit Centre, repairs enter a review queue where engineers can inspect side-by-side DOM diffs and promote verified locators to Version 2 with one click, restoring instant native execution speed."*

---

### Scene 9: Outro & Call to Action [03:20 – 03:30]
* **Scene Objective:** Professional branding, open source availability, and call to action.
* **Duration:** 10 seconds
* **Exact Asset / Resource to Feed:**
  * Repository: `https://github.com/Optimus1o1/selfhealing-ui`
  * Release: `v1.0.0`
* **Prompt for Google Flow:**
  ```text
  Cinematic centered title card with dark background and copper particle glow. Display the Moon Sanctum Labs logo and slogan: "Moon Sanctum Labs — Decode. Build. Evolve." Below, show GitHub badges: "v1.0.0 Stable | 30/30 Tests Passing | MIT License". Display the URL: "github.com/Optimus1o1/selfhealing-ui". Smooth fade to black.
  ```
* **Voiceover Script:**
  > *"SelfHeal v1.0.0 is open source on GitHub under the MIT License, verified across multi-OS CI/CD pipelines.*
  >
  > *Eliminate brittle test flakiness today. Moon Sanctum Labs — Decode. Build. Evolve."*

---

## 📁 Resource Mapping Summary Table for Google Flow Uploads

| Scene # | Scene Title | Exact File Path to Upload / Reference | Key Visual Focus |
|:---:|:---|:---|:---|
| **1** | The Hook / Broken Locators | `docs/assets/demo/03_scenario_b_v2_login_mutated.png` | Playwright timeout error, red build failure |
| **2** | LLM vs. Deterministic | `docs/assets/diagrams/feature_weights.svg` | 6-dimension feature weights, 3.2ms latency |
| **3** | System Architecture | `docs/assets/diagrams/architecture_overview.svg` | 4-tier layer diagram, proxy composition |
| **4** | Baseline Capture (V1) | `docs/assets/demo/01_scenario_a_v1_login_baseline.png` | Fingerprint capture HUD on login form |
| **5** | V2 Mutation & Healing | `docs/assets/demo/04_scenario_b_v2_login_healed_success.png` | Repaired locator `#sign-in-btn` ($S=0.8640$) |
| **6** | Grid Disambiguation | `docs/assets/demo/05_scenario_e_catalog_grid_candidates.png` | 3 identical "Add to Bag" buttons isolated |
| **7** | Zero False Positives | `docs/assets/demo/09_scenario_f_ambiguous_candidates.png` | Ambiguity margin ($\Delta < 0.10$) rejection |
| **8** | Streamlit Dashboard | `docs/assets/dashboard/06_intelligence_inspector.png` | 6-dimension score radar & V2 promotion |
| **9** | Outro / GitHub Showcase | GitHub URL + Brand lockup | `github.com/Optimus1o1/selfhealing-ui` |
