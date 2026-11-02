# Comprehensive Technical Viva Preparation & Defense Guide

**Moon Sanctum Labs** — *Decode. Build. Evolve.*  
**Lead Engineer:** Aniket Nandi (Kolkata, IST)  
**System Version:** `1.0.0rc1`  
**Focus:** Architectural Rigor, Algorithmic Foundations & Defense Trade-offs  

---

## Section A: Core Technical Questions & Answers (Questions 1 – 20)

### Q1: How does Microsoft Playwright differ from legacy Selenium WebDriver, and why did you choose Playwright as the base automation engine?
**Answer:**  
Selenium WebDriver relies on the W3C WebDriver HTTP wire protocol (sending individual HTTP JSON requests for every action, introducing network latency and external browser driver binaries like `chromedriver`). In contrast, Playwright communicates directly with browser rendering engines (Chromium, Firefox, WebKit) via a single, bidirectional WebSocket connection over the Chrome DevTools Protocol (CDP) and equivalent internal engine protocols. Playwright provides native auto-waiting for actionability (ensuring elements are attached, visible, stable, enabled, and unintercepted before dispatching clicks), eliminating arbitrary sleeps and dramatically reducing test flakiness.

---

### Q2: What is the "Brittle Locator Problem" in software test automation?
**Answer:**  
Web applications undergo frequent aesthetic and structural refactoring—such as migrating from Bootstrap to Tailwind CSS, regenerating automated class hashes (e.g. styled-components), or reorganizing `<div>` hierarchies for responsive flexbox layouts. Test scripts that hardcode rigid selectors (such as `#submit-v1` or fragile full XPaths like `/html/body/div[2]/form/button`) break immediately when developers rename attributes or reorganize containers, even though the core user flow remains functionally intact. This creates an unsustainable test maintenance burden.

---

### Q3: Why did you implement a wrapper pattern (`SelfHealingPage`, `SelfHealingLocator`) rather than monkey-patching Playwright's core classes?
**Answer:**  
Monkey-patching mutates global class definitions in the Python runtime. In enterprise testing, multiple test suites, plugins, and third-party libraries may interact with Playwright simultaneously; monkey-patching introduces hidden side effects, breaks IDE type autocompletion, causes race conditions in parallel test workers, and fails across minor Playwright version updates. The wrapper pattern uses composition and delegation: `SelfHealingPage` and `SelfHealingLocator` preserve 100% of native Playwright interfaces while encapsulating baseline capture and retry logic cleanly.

---

### Q4: What constitutes an "Element Fingerprint" in SelfHeal, and how is it captured?
**Answer:**  
An Element Fingerprint (`ElementFingerprint` in `src/selfheal/baseline/fingerprint.py`) is a serialized multi-dimensional snapshot of a DOM element captured prior to successful action execution. It stores:
1. **Identifiers:** `tag_name`, `element_id`, `class_list`, `name`, `input_type`.
2. **Semantics & Accessibility:** `inner_text`, `aria_role`, `accessible_name`, `placeholder`.
3. **Hierarchy Context:** `parent_tag`, `parent_id`, `parent_classes`, `children_count`, `children_tags`.
4. **Spatial Geometry:** Viewport bounding box coordinates $(x, y, w, h)$.
5. **Metadata:** Origin URL, selector, and creation timestamp.

---

### Q5: How does the framework sanitize sensitive user data (e.g. passwords) during baseline capture?
**Answer:**  
In `extract_fingerprint()`, before an element's attributes are persisted to SQLite, the element's `tag_name` and `type` attribute are evaluated. If `tag_name == "input"` and `type.lower() == "password"`, its `inner_text`, `value`, and `placeholder` attributes are sanitized to empty strings. Sensitive credentials are never persisted to disk or exposed in audit dashboards.

---

### Q6: How does the `FailureClassifier` distinguish between a broken locator and a genuine application bug?
**Answer:**  
When an action fails, `FailureClassifier.classify_failure()` evaluates the current DOM state:
1. **Assertion Errors & Syntax Errors:** If the exception is an `AssertionError` or malformed CSS selector, it is immediately flagged as `ASSERTION_FAILURE` or `INVALID_SELECTOR` and never healed.
2. **Locator Count Query:** It executes `page.locator(selector).count()`.
3. **Grace Period Wait:** If `count == 0`, it pauses for `grace_period_ms` (500 ms) to allow dynamic SPA hydration (AJAX rendering) and re-checks count.
4. **Actionability Defects:** If `count == 1`, it checks `is_visible()` and `is_enabled()`. If an element is present but hidden or disabled, it classifies it as `ELEMENT_HIDDEN` or `ELEMENT_DISABLED` (`is_healable = False`).
5. **True Absence:** Only if `count == 0` after the grace period is the failure classified as `LOCATOR_NOT_FOUND` (`is_healable = True`).

---

### Q7: Why is in-browser JavaScript evaluation used for DOM scanning rather than recursive Playwright locator queries?
**Answer:**  
Making round-trip IPC calls from Python to Playwright for hundreds of DOM elements across the network socket would incur hundreds of milliseconds of latency. By executing `dom_extractor.js` in a single `page.evaluate()` call, the entire interactive subtree is scanned, filtered, and extracted inside the browser's native V8 engine in **2.30 milliseconds**, returning a compact JSON array of candidate models in one round-trip.

---

### Q8: Explain the role of RapidFuzz in the text similarity dimension.
**Answer:**  
RapidFuzz is a high-performance C++ implementation of string distance algorithms. The text similarity metric uses:
1. **Normalized Levenshtein:** Measures character edit operations, penalizing typos.
2. **Jaro-Winkler:** Prioritizes common prefixes, ideal for UI labels like "Submit" vs "Submit Now".
3. **Token Sort Ratio:** Alphabetizes word tokens before comparing, handling token reordering like "Sign In" vs "In Sign".
The composite fuzzy metric combines them: $0.40 \times \text{Levenshtein} + 0.30 \times \text{Jaro-Winkler} + 0.30 \times \text{TokenSort}$.

---

### Q9: How does the Deterministic UI Synonym Ontology work?
**Answer:**  
Web interfaces frequently substitute synonyms (e.g. "Cart" $\rightarrow$ "Bag", "Checkout" $\rightarrow$ "Payment", "Login" $\rightarrow$ "Sign In"). The framework maintains 12 curated synonym equivalence sets. When comparing two words, if both exist in the same set, the engine assigns an equivalence score of $0.95$. For multi-word phrases of equal length, if token-by-token synonym matches score $\ge 0.90$, the phrase similarity is computed as the average synonym score.

---

### Q10: How does the framework differentiate between identical buttons across repetitive cards (e.g. multiple "Add to Bag" buttons)?
**Answer:**  
In modern e-commerce product catalogs, several products display identical visible text: "Add to Bag". To resolve this, the text similarity algorithm prioritizes the W3C accessible name:
$$s_{\text{text}} = 0.70 \times \text{sim}(\text{acc\_name}_{\text{base}}, \text{acc\_name}_{\text{cand}}) + 0.30 \times \text{sim}(\text{text}_{\text{base}}, \text{text}_{\text{cand}})$$
If the card has an accessible label like `"Add to Bag - Wireless Headphones"`, the accessible name creates distinct separation, preventing false positive misclicks.

---

### Q11: Explain how Jaccard Similarity is used in HTML attribute matching.
**Answer:**  
Jaccard similarity measures the intersection over union of two sets:
$$J(A, B) = \frac{|A \cap B|}{|A \cup B|}$$
In `compute_attributes_similarity()`, Jaccard is computed across:
1. **Attribute Keys:** $J(K_{\text{base}}, K_{\text{cand}})$ (e.g. whether both have `id`, `class`, `data-testid`).
2. **Attribute Key-Value Pairs:** $J(P_{\text{base}}, P_{\text{cand}})$.
3. **Baseline Pair Overlap:** Evaluates what fraction of the baseline's attributes survived in the candidate.
The composite attribute score is: $0.30 \cdot J_{\text{keys}} + 0.70 \cdot (0.50 \cdot J_{\text{pairs}} + 0.50 \cdot \text{Overlap})$.

---

### Q12: How is spatial proximity computed and normalized?
**Answer:**  
The centroid of both the baseline bounding box $(x_b, y_b)$ and candidate bounding box $(x_c, y_c)$ is determined. The Euclidean distance is computed:
$$d = \sqrt{(x_b - x_c)^2 + (y_b - y_c)^2}$$
To convert this to a bounded similarity metric $[0, 1]$, $d$ is normalized against the standard viewport diagonal ($D = 1920\text{ px}$):
$$s_{\text{pos}} = \max\left(0, 1 - \frac{d}{1920}\right)$$

---

### Q13: What are the two confidence gating rules enforced by the `HealingDecisionEngine`?
**Answer:**  
1. **Minimum Confidence Threshold:** The top candidate's total similarity score must satisfy $S_1 \ge \tau_{\min} = 0.80$.
2. **Minimum Score Margin:** When multiple candidates exist, the score difference between the top candidate and the runner-up must satisfy:
   $$\Delta = S_1 - S_2 \ge \Delta_{\min} = 0.10$$
If $\Delta < 0.10$, the match is flagged as ambiguous and rejected (`REJECTED_AMBIGUOUS_MATCH`) to prevent random guessing between near-identical options.

---

### Q14: What is the "Strict Candidate Uniqueness" rule before action retry?
**Answer:**  
Even if the decision engine synthesizes a selector with a high score, `ExecutionManager` executes `page.locator(healed_selector).count()`. If `count != 1`, the action is **not** executed, and the event is rejected with `REJECTED_AMBIGUOUS_RETRY`. A selector matching multiple elements could click the wrong element; strict uniqueness ensures exactly one element receives the retried event.

---

### Q15: Why is the retry limit strictly constrained to 1?
**Answer:**  
Unbounded retry loops or multi-step backtracking can alter application state (e.g. submitting multiple payments, toggling state back and forth, or exhausting timeouts). A single safe retry guarantees that an interaction either cleanly recovers on the verified replacement or terminates immediately without polluting the application state.

---

### Q16: Why is SQLite in WAL mode used for persistence instead of JSON files or a remote SQL server?
**Answer:**  
JSON files lack ACID transaction guarantees; concurrent writes from parallel test runners can corrupt JSON files. A remote SQL server (PostgreSQL/MySQL) requires external network infrastructure, Docker, credentials, and maintenance. SQLite in Write-Ahead Logging (`WAL`) mode runs in-process with zero network overhead, supports concurrent readers without blocking writers, and guarantees atomic commits for all audit and baseline records.

---

### Q17: What are the three healing policies supported by the framework?
**Answer:**  
1. **`observe`:** Locators are evaluated and logged when they break, but actions are **never retried**. The original test fails cleanly. Useful for passive audits.
2. **`assisted` (Default):** The engine heals the locator and retries the action to keep the test green. The healing event is stored as `pending_review` in SQLite, requiring QA sign-off in the Audit Centre before promoting to Baseline V2.
3. **`automatic`:** The engine heals, retries, and immediately auto-promotes the replacement selector to Baseline V2 without human intervention.

---

### Q18: What is the difference between Precision and Recall in this evaluation, and why is Precision prioritized?
**Answer:**  
- **Precision:** $\frac{TP}{TP + FP}$ — The percentage of repaired locators that were truly the correct element.
- **Recall:** $\frac{TP}{TP + FN}$ — The percentage of eligible broken locators that the framework successfully recovered.
In test automation, a **False Positive** clicks the wrong element, causing silent assertion corruption or destructive state changes (e.g. deleting test accounts). A **False Negative** simply fails the test normally, which is the baseline behavior of vanilla Playwright. Thus, maintaining **100% Precision (0% FPR)** is mandatory, even if Recall is slightly lower ($87.30\%$).

---

### Q19: What were the verified latency percentiles across the 500+ iteration performance benchmark?
**Answer:**  
- **Pure Algorithm Scoring:** Mean 0.69 ms, Median (P50) 0.61 ms, P95 1.13 ms.
- **Decision Engine Gating:** Mean 0.005 ms, P50 0.004 ms.
- **In-Browser DOM Extraction:** Mean 2.30 ms, P50 2.18 ms.
- **Normal Execution Overhead:** Mean 23.72 ms, P50 23.34 ms.
- **Standard Complete Healing ($2,500$ ms timeout):** Mean 3,072.27 ms, P50 3,071.61 ms.
- **Fast Complete Healing ($1,000$ ms timeout):** Mean 1,572.06 ms, P50 1,567.89 ms.

---

### Q20: What is the Latency Dominance Breakdown of complete healing?
**Answer:**  
In standard configuration ($2,500$ ms action timeout), the Playwright native action timeout accounts for **81.37%** of the latency, and the dynamic SPA grace period ($500$ ms) accounts for **16.27%**. The pure computational overhead of SelfHeal (DOM extraction + vector scoring + decision gating) is **2.998 ms**, which is **less than 0.1%** of total healing duration.

---

## Section B: 10 Challenging Architectural Trade-Off Questions (Questions 21 – 30)

### Q21: Why choose deterministic heuristics over Large Language Models (LLMs) like GPT-4 or Claude for locator healing?
**Answer:**  
1. **Determinism:** LLMs are probabilistic token predictors with non-zero temperature variance; identical DOM inputs can produce different locator suggestions across runs, creating unreproducible test results.
2. **Latency:** LLM API round-trips take between $800$ ms and $3,500$ ms per call. Our deterministic RapidFuzz algorithm computes similarity in **0.69 milliseconds**—three orders of magnitude faster.
3. **Cost & Privacy:** Passing entire DOM trees containing internal attributes and enterprise data to cloud LLM APIs incurs token fees and violates data privacy policies. SelfHeal runs 100% locally with zero cloud dependencies.
4. **Reliability:** Deterministic scoring with strict margin gating achieved **0.00% False Positive Rate** across 109 scenarios, a guarantee LLMs cannot provide.

---

### Q22: Why not use Computer Vision (e.g. OpenCV template matching or CNNs) instead of DOM feature extraction?
**Answer:**  
Pixel-based visual matching is extremely sensitive to minor rendering discrepancies: font anti-aliasing variations across operating systems, sub-pixel shifting on different screen DPRs, theme toggles (dark/light mode), and dynamic content resizing. Furthermore, visual models can locate an $(x, y)$ coordinate on screen, but they cannot synthesize a stable, semantic CSS/XPath selector required for automated script evolution and accessibility validation.

---

### Q23: Why did you enforce a linear weighted combination of scores rather than training a machine learning classifier (e.g. Random Forest or XGBoost)?
**Answer:**  
Supervised machine learning classifiers require large, labeled training datasets of before/after DOM mutations, which suffer from dataset bias toward specific web development styles. Furthermore, ML models operate as "black boxes" in production; when a model makes an incorrect decision, explaining why feature weights triggered that prediction is difficult. Our linear weighted inner product is fully transparent: every healing event displays the exact 6-dimension breakdown in the Intelligence Inspector, allowing QA engineers to mathematically verify the decision.

---

### Q24: What happens if a web page uses Shadow DOM? Does SelfHeal support it?
**Answer:**  
In open Shadow DOM components, Playwright's native locators pierce shadow roots seamlessly using standard CSS selectors (`piercing selectors`). However, closed Shadow DOM trees cannot be traversed from outside the component root by design. In our current implementation, `dom_extractor.js` traverses standard DOM trees and open shadow roots, but closed shadow roots represent an explicit architectural limitation.

---

### Q25: How does the framework prevent infinite healing cascades if an entire page structure is completely redesigned?
**Answer:**  
1. **Confidence Threshold:** If the entire page changes, candidate elements will score well below the $0.80$ threshold, triggering `REJECTED_LOW_CONFIDENCE`.
2. **Ambiguity Margin:** Redesigned layouts with multiple similar components will fail the $\Delta \ge 0.10$ margin check, triggering `REJECTED_AMBIGUOUS_MATCH`.
3. **Single-Retry Limit:** Each locator action is attempted at most once; the framework never cascades or loops.
4. **Baseline Lock:** In `assisted` mode, healed locators are held in `pending_review` until an engineer approves them; the database will not blindly adopt unverified changes.

---

### Q26: Why is the confidence margin set to 0.10 instead of 0.05 or 0.20?
**Answer:**  
In our empirical sensitivity analysis:
- At $\Delta = 0.05$, near-tie buttons (such as competing payment methods or tabs in a tabset) occasionally slipped through, increasing false positive risk.
- At $\Delta = 0.20$, legitimate candidates that had minor attribute changes alongside other buttons on the page were excessively rejected, reducing healing recall to under $65\%$.
- A threshold of $\Delta = 0.10$ provided the optimal Pareto frontier: **0.00% False Positive Rate** while maintaining **87.30% Combined Recall**.

---

### Q27: How does SelfHeal handle dynamic Single Page Applications (SPAs) where elements render asynchronously after network requests?
**Answer:**  
When an action fails, `FailureClassifier` does not immediately conclude that the locator is missing. If initial count is 0, it initiates a configured `grace_period_ms` (500 ms default) to accommodate AJAX responses and microtask queue flushing, followed by a secondary verification count. If the element hydrates within this window, the classifier flags it as a timing/delay issue rather than a broken locator, preventing unnecessary healing attempts.

---

### Q28: How does the Audit Centre prevent accidental baseline corruption by junior QA engineers?
**Answer:**  
In the Streamlit Audit Centre (Section 7), the "Approve & Promote to V2" button is disabled by default. It is gated behind a mandatory confirmation checkbox:
`[ ] I have verified this locator change and confirm promoting it as the official baseline version.`
Only when the engineer explicitly checks this box does the action button unlock. Furthermore, every promotion requires recording the approver's identifier in `locator_history`, providing full non-repudiation and auditability.

---

### Q29: Can SelfHeal heal Canvas, WebGL, or SVG embedded controls?
**Answer:**  
SelfHeal inspects the Document Object Model (DOM). Standard SVG elements (`<svg>`, `<path>`, `<circle>`) that exist in the DOM tree can be matched using tag and attribute rules. However, `<canvas>` and WebGL applications render pixels onto an internal framebuffer without DOM nodes for individual UI controls; therefore, canvas-rendered widgets cannot be extracted or healed via DOM heuristics. This is an explicit scope limitation.

---

### Q30: How does Write-Ahead Logging (WAL) prevent database lockups during parallel test execution?
**Answer:**  
In traditional SQLite rollback journals, any writer acquires an exclusive database lock, blocking all readers and other writers. With `PRAGMA journal_mode = WAL;`, changes are appended sequentially to a separate write-ahead log (`selfheal.db-wal`). Readers read consistent point-in-time snapshots from the main database file while writers append to the WAL. This eliminates `database is locked` errors when pytest executes multi-threaded tests while the Streamlit dashboard queries real-time metrics simultaneously.

