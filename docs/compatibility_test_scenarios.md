# SelfHeal — Compatibility Validation Test Scenarios

**Moon Sanctum Labs** — *Decode. Build. Evolve.*  
**Framework Version:** 1.0.0  
**Document Status:** Template — scenarios defined, results pending external testing

---

## Purpose

This document defines eight categories of real-world UI mutation scenarios for validating SelfHeal's compatibility across different application architectures. Each scenario specifies the DOM change, expected SelfHeal behaviour, and pass/fail criteria.

> **Important:** All result columns are intentionally blank. They are populated only after actual pilot testing with authorised applications.

---

## Category 1 — React Applications (Component Restructuring)

React applications frequently restructure component trees during refactors, changing parent containers while preserving element semantics.

| # | Scenario | DOM Change | Expected Behaviour | Pass/Fail |
|---|---|---|---|---|
| R1 | Component key remapping | `key="item-1"` → `key="product-1"`, element identity preserved | Heal via text + ARIA + attribute similarity | |
| R2 | Wrapper div insertion | `<Button>` gains a new parent `<div className="wrapper">` | Heal — parent path changes but element fingerprint matches | |
| R3 | Class name migration (CSS Modules) | `class="btn_abc123"` → `class="btn_def456"` (hash change) | Heal via text, ARIA, tag, position — class is one dimension only | |
| R4 | Component library swap | Material UI `<Button>` → Chakra `<Button>`, same text and role | Heal if tag + text + ARIA preserved; may fail if tag changes to `<a>` | |
| R5 | Conditional rendering toggle | Element rendered inside a different conditional branch | Heal if element attributes are preserved in new branch | |

---

## Category 2 — Single Page Applications (Dynamic Rendering)

SPAs render elements dynamically, often replacing entire DOM subtrees during navigation.

| # | Scenario | DOM Change | Expected Behaviour | Pass/Fail |
|---|---|---|---|---|
| S1 | Client-side route change | Element re-rendered after SPA navigation | Heal — fingerprint matched against re-rendered element | |
| S2 | Virtual DOM reconciliation | React/Vue re-keys elements during list update | Heal if text content and attributes remain similar | |
| S3 | Lazy-loaded component | Element appears after async module load | Heal after Playwright's wait timeout triggers DOM scan | |
| S4 | Portal-rendered modal | Modal moves from `<body>` to a portal container | Heal — position/parent changes but element identity preserved | |
| S5 | State-driven visibility | Element hidden via state, then re-shown with different parent | Heal if element is present in DOM when scan executes | |

---

## Category 3 — Dynamic Forms (Input Fields and Validation)

Forms with dynamic validation, conditional fields, and generated IDs are common sources of locator brittleness.

| # | Scenario | DOM Change | Expected Behaviour | Pass/Fail |
|---|---|---|---|---|
| F1 | Generated input ID | `id="field_7f3a"` → `id="field_9b2c"` (session-generated) | Heal via name, placeholder, label, and position | |
| F2 | Validation wrapper change | Input gains `<div class="error-wrapper">` parent | Heal — parent path changes but input fingerprint matches | |
| F3 | Placeholder text update | `placeholder="Enter email"` → `placeholder="Your email address"` | Heal via fuzzy text matching (RapidFuzz) | |
| F4 | Input type change | `type="text"` → `type="email"` (same field) | Heal — tag and other attributes preserved | |
| F5 | Conditional field insertion | New field inserted before target, shifting position | Heal if position weight is low enough (default 0.05) | |

---

## Category 4 — Navigation Menus (Structural Changes)

Navigation restructuring is one of the most frequent causes of broken locators in regression suites.

| # | Scenario | DOM Change | Expected Behaviour | Pass/Fail |
|---|---|---|---|---|
| N1 | Nav item text rename | `"Products"` → `"Our Products"` | Heal via fuzzy text similarity | |
| N2 | Dropdown to mega-menu | `<li>` items move from `<ul>` to grid container | Heal — text and ARIA preserved despite structural change | |
| N3 | Hamburger menu refactor | Desktop nav items move inside mobile drawer | Heal if elements are present in DOM (not display:none) | |
| N4 | Link to button conversion | `<a href="#">Contact</a>` → `<button>Contact</button>` | May not heal — tag change from `a` to `button` reduces score | |
| N5 | Aria-label update | `aria-label="Main navigation"` → `aria-label="Site navigation"` | Heal via fuzzy ARIA matching | |

---

## Category 5 — Repeated Accessible Names (Ambiguity Testing)

Multiple elements with identical or near-identical accessible names test SelfHeal's ambiguity rejection guards.

| # | Scenario | DOM Change | Expected Behaviour | Pass/Fail |
|---|---|---|---|---|
| A1 | Three "Submit" buttons | Page has 3 `<button>Submit</button>` in different forms | **Reject** — ambiguity margin < 0.10 between candidates | |
| A2 | Two "Add to Cart" with different parents | Same text, different parent containers | Heal if parent hierarchy distinguishes them (margin ≥ 0.10) | |
| A3 | Icon buttons with same aria-label | Multiple `<button aria-label="Delete">` | **Reject** — ambiguity guard should prevent incorrect healing | |
| A4 | Table action buttons | "Edit" button in every table row | **Reject** unless row-specific attributes differentiate | |
| A5 | Accordion section headers | Multiple "Show Details" toggles | **Reject** or heal only if positional/hierarchical difference is sufficient | |

---

## Category 6 — Asynchronous Rendering

Content that appears after API calls, animations, or lazy loading introduces timing-dependent DOM states.

| # | Scenario | DOM Change | Expected Behaviour | Pass/Fail |
|---|---|---|---|---|
| Y1 | Skeleton to content transition | Skeleton placeholder replaced by real element after API response | Heal if scan executes after content renders | |
| Y2 | Infinite scroll pagination | Elements appended after scroll trigger | Heal — new elements scanned when failure triggers DOM extraction | |
| Y3 | Debounced search results | Results appear after typing delay | Heal if candidate element exists at scan time | |
| Y4 | Animation-delayed element | Element enters DOM via CSS animation with `opacity: 0` → `1` | May fail if element is not yet actionable during scan window | |
| Y5 | Web Worker rendered content | Content injected by background worker thread | Heal if element is in DOM when `DOMScanner` executes | |

---

## Category 7 — Responsive Layouts

Elements that reposition, resize, or restructure across breakpoints test SelfHeal's position-weight tolerance.

| # | Scenario | DOM Change | Expected Behaviour | Pass/Fail |
|---|---|---|---|---|
| L1 | Sidebar to bottom bar | Navigation moves from left sidebar to bottom on mobile | Heal — text and ARIA preserved, position change tolerated (weight 0.05) | |
| L2 | Grid to stack layout | 3-column grid collapses to single column | Heal — position changes but element identity preserved | |
| L3 | Desktop-only element | Element hidden via `display:none` on mobile | **Not healed** — actionability failure (element exists but hidden) | |
| L4 | Responsive image swap | `<img>` replaced by `<picture>` with different `srcset` | May not heal — tag change from `img` to `picture` | |
| L5 | Breakpoint-conditional rendering | Element only rendered above 768px viewport | Heal if element is in DOM at test viewport size | |

---

## Category 8 — Locator Chaining and Complex Selectors

Tests that use chained or compound locators stress the fingerprint matching system.

| # | Scenario | DOM Change | Expected Behaviour | Pass/Fail |
|---|---|---|---|---|
| C1 | Parent locator chain break | `page.locator(".container").locator("#btn")` — container class changes | Healing applies to the failing locator in the chain | |
| C2 | Nth-match index shift | `page.locator("button").nth(2)` — new button inserted before target | May not heal — nth-index strategies are not fingerprinted | |
| C3 | has-text filter | `page.locator("div", has_text="Welcome")` | Heal via text similarity if "Welcome" text changes | |
| C4 | Role-based locator | `page.get_by_role("button", name="Submit")` | Heal via ARIA role + text matching | |
| C5 | XPath locator | `page.locator("//div[@class='old']/button")` | Heal — XPath locator evaluated, element fingerprinted | |

---

## Scoring Guide

For each scenario after testing:

| Result | Meaning |
|---|---|
| **PASS** | SelfHeal behaved exactly as expected (healed correctly or rejected correctly) |
| **FAIL — False Positive** | SelfHeal healed to the wrong element |
| **FAIL — False Negative** | SelfHeal failed to heal when it should have |
| **EXPECTED REJECT** | SelfHeal correctly rejected an ambiguous match |
| **UNEXPECTED REJECT** | SelfHeal rejected a match that should have been unambiguous |
| **NOT TESTED** | Scenario not applicable to the pilot application |

---

*Moon Sanctum Labs — Decode. Build. Evolve.*
