# Technical Demonstration Video Script & Recording Guide

**Project:** SelfHeal — Intelligent Self-Healing UI Automation Framework  
**Brand:** Moon Sanctum Labs — *Decode. Build. Evolve.*  
**Lead Engineer & Presenter:** Aniket Nandi (Kolkata, IST)  
**System Version:** `1.0.0` (Stable)  
**Target Duration:** 4 Minutes (Acceptable Range: 3:30 – 5:00 Minutes)  
**Format:** 1080p60 / 1440p60 Video with Voiceover & Split-Screen Terminal / Browser Layout

---

## 🎬 Pre-Recording Technical Checklist

### 1. Recording Setup & Software Settings
- [ ] **Recording Tool:** OBS Studio (or equivalent lossless screen recorder).
- [ ] **Canvas Resolution:** $1920 \times 1080$ at $60\text{ fps}$ (or $2560 \times 1440$).
- [ ] **Audio Settings:** 48 kHz / 24-bit audio, noise suppression filter enabled, microphone gain normalized to $-6\text{ dB}$.
- [ ] **Display Scaling:** Set Windows display scaling to $100\%$ or $125\%$ to ensure crisp font rendering without blur.
- [ ] **Editor Theme:** Dark Theme matching Moon Sanctum Labs aesthetic (Ink `#0F1013`, Bone `#F2EFE8`, Copper `#E0A45C`, Slate `#8B9099`).

### 2. Workspace Pre-Conditions
- [ ] **Terminal 1 (Bottom/Left):** PowerShell in repository root `c:\Users\ANIKET\OneDrive\Documents\SelfHealing_UI`.
- [ ] **Terminal 2 (Background):** Ready to launch Streamlit dashboard.
- [ ] **Browser Window (Top/Right):** Clean Chromium window at `1280x720` or half-screen width.
- [ ] **Database State:** Clean database initialized:
  ```powershell
  python -m selfheal.cli reset-db
  ```
- [ ] **Headless vs Headed Mode:** For video recording, run the demo runner with `--headed` so viewers can visually see browser interactions:
  ```powershell
  python scripts/run_academic_demo.py --headed
  ```

---

## ⏱️ Video Timeline & Scene Breakdown

```
00:00 - 00:30 | Scene 1: The Problem & Introduction (Title & Context)
00:30 - 01:15 | Scene 2: V1 Baseline Execution (Clean Pass & Fingerprint Capture)
01:15 - 02:15 | Scene 3: V2 Mutation & Autonomous Self-Healing in Action
02:15 - 03:00 | Scene 4: Safety Guardrails (Ambiguity & Actionability Rejection)
03:00 - 03:45 | Scene 5: Streamlit Governance Dashboard & V2 Baseline Promotion
03:45 - 04:00 | Scene 6: Architectural Summary & Engineering Wrap-Up
```

---

## 🎙️ Scene-by-Scene Screenplay & Voiceover

### Scene 1: The Problem & Introduction [00:00 – 00:30]
* **Visual Layout:** 
  * Full screen title card featuring the Moon Sanctum Labs lockup (*Decode. Build. Evolve.*), system badges (100% Precision, 0% FPR, 30/30 Tests Passed), and repository title: **SelfHeal — Deterministic Self-Healing UI Automation for Playwright**.
* **Voiceover (Calm, precise, professional):**
  > *"Every test automation engineer knows the pain of flaky end-to-end tests. A frontend team changes a button ID from kebab-case to camelCase, tweaks text from 'Log In' to 'Sign In', or wraps an element in a new container—and instantly, your CI pipeline turns red.*
  >
  > *Teams waste 30 to 40% of their time updating broken locators. While some attempt to solve this with cloud LLMs, generative AI introduces 4-second network latency, unpredictable hallucinations, and dangerous false-positive clicks.*
  >
  > *This is SelfHeal: a production-grade, deterministic self-healing framework for Playwright in Python that repairs broken locators locally in under 3 milliseconds, with a 100% precision guarantee."*

---

### Scene 2: V1 Baseline Execution [00:30 – 01:15]
* **Visual Layout:** Split-screen. Left half: VS Code showing `tests/demo/test_ecommerce_demonstration.py`. Right half: Chromium browser loading `http://localhost:5000/v1`.
* **Action:**
  1. Highlight test code:
     ```python
     page.healed_locator("#btnLogin", key="auth.login_submit").click()
     ```
  2. Point out that the test script uses standard Playwright syntax with a stable `key`.
  3. Run baseline test:
     ```powershell
     python scripts/run_academic_demo.py --headed
     ```
* **Voiceover:**
  > *"Here is our e-commerce demonstration application. In Version 1, elements use standard semantic selectors: `#btnLogin`, `#btnAddToCart1`, and `#btnProceedCheckout`.*
  >
  > *Notice our test script. We simply wrap Playwright's Page with `SelfHealingPage` and define our target locators. When the test runs for the first time, SelfHeal passively captures a 10-dimensional DOM fingerprint of each element into an embedded SQLite WAL database—including text, ARIA roles, attributes, parent hierarchy, and bounding boxes—with zero execution overhead."*

---

### Scene 3: V2 Mutation & Autonomous Self-Healing [01:15 – 02:15]
* **Visual Layout:** 
  * Show browser switching to `http://localhost:5000/v2`.
  * Zoom in on the refactored DOM:
    * `#btnLogin` is now `#sign-in-btn`.
    * Text is changed from `"Log In"` to `"Sign In"`.
    * Button is wrapped in an additional `<div class="flex flex-col">`.
  * Terminal running the exact same test script against V2.
* **Action:**
  1. Terminal displays live execution logs:
     ```text
     [WARN] Locator '#btnLogin' timed out after 2500ms
     [INFO] Scanning live DOM... extracted 14 candidates in 2.1ms
     [INFO] Computing multi-dimensional similarity scores...
     [MATCH] Candidate 'button:has-text("Sign In")' -> Score: 0.8640 (Threshold: 0.80, Margin: 0.2840)
     [RETRY] Single safe retry dispatched... SUCCESS
     [HEALED] Target 'auth.login_submit' healed autonomously!
     ```
  2. Browser window visibly logs in, adds item to cart, and proceeds to checkout without test failure.
* **Voiceover:**
  > *"Now we deploy Version 2 of our application. The frontend has been heavily refactored. The login button ID is now `#sign-in-btn`, the text has changed to 'Sign In', and the container layout is modified.*
  >
  > *Watch what happens when we execute the exact same test script without changing a single line of test code.*
  >
  > *When `#btnLogin` fails to appear, SelfHeal's Failure Classifier confirms the element is truly absent, not merely disabled or hidden. It extracts candidates from the live DOM and executes our multi-dimensional similarity algorithm using RapidFuzz, Jaccard attribute overlap, and semantic action synonym clustering.*
  >
  > *The replacement button scores 0.8640—well above our 0.80 threshold. SelfHeal verifies candidate uniqueness, dispatches a single retry, and the test continues uninterrupted."*

---

### Scene 4: Safety Guardrails — Ambiguity & Actionability Rejection [02:15 – 03:00]
* **Visual Layout:** Split-screen showing the terminal logs for Scenario F (Ambiguous Match) and Scenario G (Disabled Button), with visual callout overlays on the browser window.
* **Action:**
  1. Show Scenario F: Two near-identical payment buttons (`"Pay with Card"` vs `"Pay with Debit"`).
  2. Terminal logs:
     ```text
     [CANDIDATE 1] Score: 0.8420
     [CANDIDATE 2] Score: 0.8150
     [GUARDRAIL] Score Margin Delta: 0.0270 < 0.10 (Minimum Margin Violation)
     [REJECTED] REJECTED_AMBIGUOUS_MATCH — Halting execution to prevent incorrect click
     ```
  3. Show Scenario G: Checkout button is disabled. Failure classifier identifies `ELEMENT_DISABLED` and immediately fails fast without attempting healing.
* **Voiceover:**
  > *"In test automation, clicking the wrong button is catastrophic. That is why SelfHeal enforces two strict mathematical safety guardrails.*
  >
  > *First, the **Ambiguity Margin Guardrail**: in Scenario F, two competing payment buttons both scored above 0.80, but the score margin was only 0.027—below our required 0.10 gap. Instead of guessing, SelfHeal intentionally abstained, reporting `REJECTED_AMBIGUOUS_MATCH`.*
  >
  > *Second, the **Failure Classifier**: in Scenario G, an order button was disabled. SelfHeal identified this as an actionability defect, not a missing locator, and failed fast. This guarantees that real application bugs are never masked by false healing. Across 109 evaluation scenarios, our observed False Positive Rate is exactly 0.00%."*

---

### Scene 5: Streamlit Governance Dashboard & V2 Promotion [03:00 – 03:45]
* **Visual Layout:** Full screen browser displaying the Streamlit Engineering Dashboard at `http://localhost:8501`.
* **Action:**
  1. Click on **Overview**: Show 100% precision, total healed interactions, and latency breakdown.
  2. Click on **Intelligence Inspector**: Select `auth.login_submit`. Show the 6-dimension bar chart (Text 30%, Tag/Role 20%, Attributes 20%, Parent 15%, Children 10%, Geometry 5%) and the natural language explanation.
  3. Click on **Fingerprint Inspector**: Show the color-coded attribute diff table (MATCHED / CHANGED / NEW).
  4. Click on **Audit Centre**: Show the pending review item, click the safety confirmation checkbox, and click **Approve & Promote to V2**.
  5. Show that future runs now use the promoted V2 selector with zero healing latency.
* **Voiceover:**
  > *"SelfHeal provides an enterprise 9-section Streamlit governance dashboard.*
  >
  > *In the Intelligence Inspector, QA engineers can view the exact mathematical breakdown across all six similarity dimensions.*
  >
  > *In the Audit Centre, every automated repair enters a pending review queue. A QA engineer can inspect the side-by-side DOM diff, check the confirmation gate, and promote the repair to Version 2 in our SQLite baseline. On the next test run, Playwright targets the new selector directly, restoring full execution speed."*

---

### Scene 6: Architectural Summary & Engineering Wrap-Up [03:45 – 04:00]
* **Visual Layout:** Return to the Moon Sanctum Labs closing card with GitHub URL (`https://github.com/Optimus1o1/selfhealing-ui`), documentation links, and MIT License badge.
* **Voiceover:**
  > *"SelfHeal is open-source under the MIT license, backed by 30 automated tests, a 6-job CI matrix, and comprehensive academic documentation.*
  >
  > *Check out the repository on GitHub, try the interactive demonstration yourself, and eliminate brittle test flakiness forever.*
  >
  > *Moon Sanctum Labs — Decode. Build. Evolve. Thank you."*

---

## 📋 Post-Recording & Editing Checklist
- [ ] Trim leading and trailing dead air.
- [ ] Add subtle zoom-ins on terminal similarity scores and dashboard radar charts.
- [ ] Ensure audio level remains consistently balanced between $-14\text{ LUFS}$ and $-16\text{ LUFS}$.
- [ ] Render video as MP4 (H.264 / AAC) at high bitrate ($12\text{–}16\text{ Mbps}$).
- [ ] Export thumbnail using `docs/assets/dashboard/01_overview.png` with brand overlay.
