# Module Reference & API Specification

**Moon Sanctum Labs** — *Decode. Build. Evolve.*  
**Lead Engineer:** Aniket Nandi (Kolkata, IST)  
**System Version:** `1.0.0rc1`  
**Package:** `selfheal`  

---

## Architecture & Module Directory

```
src/selfheal/
├── cli.py                        # Command Line Interface (Click)
├── config.py                     # Configuration models & YAML loader
├── pytest_plugin.py              # Pytest fixture & test hook provider
├── baseline/
│   ├── fingerprint.py            # DOM Fingerprint representation & extraction
│   └── repository.py             # SQLite WAL repository & versioning
├── dashboard/
│   └── app.py                    # Streamlit 9-Section Engineering Dashboard
├── database/
│   ├── connection.py             # SQLite Connection Manager & WAL setup
│   ├── models.py                 # Pydantic / dataclass database models
│   └── schema.sql                # SQLite DDL Schema definition
├── detection/
│   ├── exceptions.py             # Custom exception hierarchy
│   └── failure_detector.py       # Failure Classifier & Actionability Triage
├── engine/
│   ├── executor.py               # Action interception, single-retry, healing flow
│   ├── locator.py                # SelfHealingLocator wrapper
│   └── page.py                   # SelfHealingPage wrapper
├── intelligence/
│   ├── decision_engine.py        # Threshold & Margin Gating Engine
│   ├── scoring.py                # Multi-dimensional candidate scorer
│   └── similarity.py             # RapidFuzz string & geometric algorithms
├── reporting/
│   ├── report_generator.py       # HTML / JSON Test Report Generator
│   └── templates/
│       └── report_template.html  # Jinja2 auto-escaped HTML report template
└── scanner/
    ├── dom_extractor.js          # In-browser JavaScript element scanner
    └── dom_scanner.py            # Playwright page evaluator bridge
```

---

## 1. Engine Layer

### 1.1 `src/selfheal/engine/page.py`
- **Responsibility:** High-level wrapper around Playwright's `Page` object. Intercepts locator creation and manages test execution lifecycle.
- **Dependencies:** `playwright.sync_api.Page`, `selfheal.engine.locator.SelfHealingLocator`, `selfheal.engine.executor.ExecutionManager`, `selfheal.baseline.repository.BaselineRepository`.
- **Classes:**
  - `SelfHealingPage`:
    - `__init__(page: Page, config_path: Optional[str] = None)`: Initializes wrapper, loads configuration, connects database repository, and instantiates `ExecutionManager`.
    - `healed_locator(selector: str, key: Optional[str] = None) -> SelfHealingLocator`: Returns a wrapped locator. If `key` is omitted, an inferred logical key is derived deterministically from the selector.
    - `goto(url: str, **kwargs) -> Response`: Navigates to a URL.
    - `screenshot(path: Optional[str] = None, **kwargs) -> bytes`: Captures visual snapshot.
    - `close()`: Closes browser page and releases resources.
    - `raw_page`: Property exposing the underlying Playwright `Page` for direct access when needed.

### 1.2 `src/selfheal/engine/locator.py`
- **Responsibility:** Wraps Playwright's `Locator` object to intercept user interactions (`click`, `fill`, etc.) and route them through `ExecutionManager`.
- **Dependencies:** `playwright.sync_api.Locator`, `selfheal.engine.executor.ExecutionManager`.
- **Classes:**
  - `SelfHealingLocator`:
    - `click(**kwargs) -> None`: Delegates click action to `ExecutionManager.execute_action()`.
    - `fill(value: str, **kwargs) -> None`: Delegates fill action with input text.
    - `text_content(**kwargs) -> Optional[str]`: Retrieves element text.
    - `inner_text(**kwargs) -> str`: Retrieves inner text.
    - `is_visible(**kwargs) -> bool`: Checks element visibility.
    - `is_enabled(**kwargs) -> bool`: Checks element actionability.
    - `first -> SelfHealingLocator`: Supports chaining by resolving to the first matched locator while preserving `target_key`.
    - `last -> SelfHealingLocator`: Chaining to the last matched locator.
    - `nth(index: int) -> SelfHealingLocator`: Chaining to the $n$-th matched locator.

### 1.3 `src/selfheal/engine/executor.py`
- **Responsibility:** The core runtime coordinator. Intercepts failures, triages actionability, triggers DOM scanning and candidate scoring, enforces single-retry uniqueness, and persists audit logs.
- **Dependencies:** `selfheal.detection.failure_detector`, `selfheal.scanner.dom_scanner`, `selfheal.intelligence.scoring`, `selfheal.intelligence.decision_engine`, `selfheal.baseline.repository`.
- **Classes:**
  - `ExecutionManager`:
    - `execute_action(page, original_selector, target_key, action_name, action_fn, **action_kwargs) -> Any`:
      1. Pre-captures baseline fingerprint if none exists.
      2. Executes action with configured timeout (`action_timeout_ms`).
      3. On failure, passes exception to `FailureClassifier`.
      4. If eligible (`LOCATOR_NOT_FOUND`), scans DOM via `DOMScanner`.
      5. Ranks candidates via `SimilarityScorer`.
      6. Evaluates candidates via `HealingDecisionEngine`.
      7. Enforces candidate uniqueness (`count == 1`).
      8. Retries action **once** with healed selector.
      9. Logs healing event to `BaselineRepository`.
    - `_capture_baseline_snapshot(page, selector, target_key) -> Optional[ElementFingerprint]`: Extracts and sanitizes element properties prior to interaction.

---

## 2. Detection & Extraction Layer

### 2.1 `src/selfheal/detection/failure_detector.py`
- **Responsibility:** Triages test failures to differentiate true locator disappearance from actionability bugs or script errors.
- **Dependencies:** `playwright.sync_api.Page`, `selfheal.detection.exceptions`.
- **Classes:**
  - `FailureType(Enum)`: `LOCATOR_NOT_FOUND`, `ELEMENT_HIDDEN`, `ELEMENT_DISABLED`, `AMBIGUOUS_LOCATOR`, `INVALID_SELECTOR`, `NETWORK_OR_NAV_ERROR`, `ASSERTION_FAILURE`, `UNKNOWN_ERROR`.
  - `FailureClassification(BaseModel)`: Holds `failure_type`, `is_healable: bool`, `reason: str`, `element_count: int`.
  - `FailureClassifier`:
    - `classify_failure(page, selector, original_exception) -> FailureClassification`:
      - Inspects exception type and message for syntax/assertion errors.
      - Checks `page.locator(selector).count()`.
      - Applies grace period sleep (`grace_period_ms`) for SPA hydration.
      - Checks `is_visible()` and `is_enabled()` if element count == 1.
      - Marks `is_healable = True` **only** if count is strictly 0.

### 2.2 `src/selfheal/scanner/dom_scanner.py` & `dom_extractor.js`
- **Responsibility:** Fast in-browser extraction of all interactive candidate DOM elements.
- **Dependencies:** `playwright.sync_api.Page`.
- **Classes:**
  - `CandidateElement(BaseModel)`: Holds `tag_name`, `element_id`, `class_list`, `inner_text`, `aria_role`, `accessible_name`, `input_type`, `attributes`, `parent_tag`, `parent_id`, `parent_classes`, `children_count`, `children_tags`, `bounding_box`, `generated_selector`.
  - `DOMScanner`:
    - `scan(page: Page, max_candidates: int = 100) -> List[CandidateElement]`: Injects and executes `dom_extractor.js` via `page.evaluate()`, extracting candidates in a single JavaScript round-trip ($~2.3$ ms).

---

## 3. Intelligence & Decision Layer

### 3.1 `src/selfheal/intelligence/similarity.py`
- **Responsibility:** Pure mathematical calculation of string, attribute, structural, and spatial metrics.
- **Dependencies:** `rapidfuzz.distance.Levenshtein`, `rapidfuzz.distance.JaroWinkler`, `rapidfuzz.fuzz`.
- **Functions:**
  - `compute_text_similarity(base_text, cand_text, base_acc, cand_acc) -> float`: Combines Levenshtein, Jaro-Winkler, Token Sort, and UI synonym ontology with accessible name blending.
  - `check_ui_synonym(text_a, text_b) -> float`: Evaluates single and multi-word phrase UI synonym mappings.
  - `compute_type_and_role_similarity(base, cand) -> float`: Evaluates HTML tag match, ARIA role compatibility, and input type match.
  - `compute_attributes_similarity(base, cand) -> float`: Computes Jaccard similarity across attribute keys, attribute key-value pairs, and baseline pair overlap.
  - `compute_parent_similarity(base, cand) -> float`: Evaluates parent tag, parent ID Jaro-Winkler, and parent class Jaccard.
  - `compute_children_similarity(base, cand) -> float`: Evaluates child count delta and child tag distribution.
  - `compute_position_similarity(base_box, cand_box, viewport_diag=1920.0) -> float`: Evaluates centroid Euclidean distance normalized against viewport diagonal.

### 3.2 `src/selfheal/intelligence/scoring.py`
- **Responsibility:** Aggregates individual dimension metrics into a weighted total score.
- **Classes:**
  - `ScoreBreakdown(BaseModel)`: Holds individual scores for text, type/role, attributes, parent, children, position, and total score.
  - `ScoredCandidate(BaseModel)`: Pairs `CandidateElement` with its `ScoreBreakdown`.
  - `SimilarityScorer`:
    - `score_candidate(base, cand) -> ScoredCandidate`: Computes the 6 dimensions and weighted inner product.
    - `rank_candidates(base, candidates) -> List[ScoredCandidate]`: Scores all candidates and returns them sorted descending by `total_score`.

### 3.3 `src/selfheal/intelligence/decision_engine.py`
- **Responsibility:** Applies conservative gating rules to decide whether a candidate can safely heal the locator.
- **Classes:**
  - `DecisionStatus(Enum)`: `APPROVED`, `REJECTED_LOW_CONFIDENCE`, `REJECTED_AMBIGUOUS_MATCH`, `REJECTED_NO_CANDIDATES`.
  - `HealingDecision(BaseModel)`: Outcome metadata, winner selector, score, breakdown, and decision reason.
  - `HealingDecisionEngine`:
    - `evaluate(target_key, original_locator, ranked_candidates) -> HealingDecision`: Enforces threshold ($\ge 0.80$) and margin ($\ge 0.10$) guardrails.
    - `synthesize_locator(candidate) -> str`: Generates robust selector (`generated_selector`, `data-testid`, `#id`, text, or class).

---

## 4. Persistence & Repository Layer

### 4.1 `src/selfheal/baseline/repository.py`
- **Responsibility:** Manages all CRUD operations against SQLite WAL storage.
- **Classes:**
  - `BaselineRepository`:
    - `get_active_fingerprint(target_key) -> Optional[ElementFingerprint]`
    - `save_fingerprint(fp: ElementFingerprint) -> int`
    - `log_healing_event(event: HealingEventModel) -> int`
    - `promote_healed_locator(target_key, new_locator, similarity_score, approved_by) -> None`
    - `get_healing_events(limit, offset, status, target_key) -> List[Dict]`
    - `get_healing_event_by_id(event_id) -> Optional[Dict]`
    - `get_locator_stability_stats() -> List[Dict]`
    - `get_latency_percentiles() -> Dict[str, float]`: Computes sample count, mean, P50, P90, P95, min, and max using standard Python statistics.

### 4.2 `src/selfheal/baseline/fingerprint.py`
- **Responsibility:** Data structures and extraction routines for DOM snapshots.
- **Classes:**
  - `BoundingBox(BaseModel)`: Viewport coordinates $(x, y, w, h)$ and centroid calculation.
  - `ElementFingerprint(BaseModel)`: Full serialized representation of baseline DOM state.
  - `extract_fingerprint(page, selector, target_key) -> ElementFingerprint`: Extracts element state and enforces password privacy sanitization.

---

## 5. Presentation & Governance Layer

### 5.1 `src/selfheal/dashboard/app.py`
- **Responsibility:** Enterprise-grade engineering monitoring, inspection, and audit dashboard built with Streamlit.
- **Modules Implemented:**
  1. `render_overview()`: Executive KPIs and execution throughput trends.
  2. `render_live_execution()`: Real-time session monitoring with run selector and step breakdown.
  3. `render_healing_analytics()`: Decision triage, failure distributions, and retry success rates.
  4. `render_locator_explorer()`: Target key catalog, stability index, and mutation timeline.
  5. `render_fingerprint_inspector()`: Side-by-side DOM attribute diff (`MATCHED`, `CHANGED`, `NEW`).
  6. `render_intelligence_inspector()`: 6-dimension score breakdown, threshold & margin gating, diagnostics.
  7. `render_audit_centre()`: Pending review queue, confirmation checkbox gate, Promote to V2 / Reject Repair.
  8. `render_baseline_manager()`: Version evolution tracking (v1 $\rightarrow$ v2) with active vs archived status.
  9. `render_performance_monitor()`: Real SQLite WAL latency percentiles ($P_{50}, P_{90}, P_{95}$) vs benchmarks.

### 5.2 `src/selfheal/cli.py`
- **Responsibility:** Click-based command-line interface for local framework management.
- **Commands:**
  - `selfheal run <test_path>`: Executes pytest test suite with self-healing enabled.
  - `selfheal dashboard [--port 8501]`: Spawns the Streamlit monitoring interface.
  - `selfheal baselines`: Lists registered baseline element fingerprints.
  - `selfheal reset-db`: Re-executes `schema.sql` to initialize a clean SQLite database.
  - `selfheal report [--run-id ID]`: Generates standalone HTML and JSON audit reports.

