# SelfHeal — Product Roadmap

**Moon Sanctum Labs** — *Decode. Build. Evolve.*  
**Framework Version:** 1.0.0  
**Last Updated:** November 2026  
**Document Status:** Prioritised backlog — no implementation has begun

---

## Roadmap Philosophy

This roadmap prioritises enhancements based on five criteria:

| Criterion | Weight | Definition |
|---|---|---|
| Pilot Demand | 30% | Number of pilot participants requesting the feature |
| Reliability Impact | 25% | Effect on precision, recall, and false positive rate |
| Technical Feasibility | 20% | Implementation complexity and risk |
| User Adoption | 15% | Impact on installation, integration, or onboarding |
| Development Effort | 10% | Estimated engineering time |

> **Important:** This is a prioritised backlog. Features move to active development only after pilot feedback validates demand and the implementation does not compromise SelfHeal's core reliability guarantees.

---

## Tier 1 — Near-Term (Pilot-Driven)

These enhancements address known limitations and are candidates for SelfHeal 1.x releases.

| # | Feature | Priority Score | Status | Description |
|---|---|---|---|---|
| 1.1 | Shadow DOM support | High | Planned | Extend `DOMScanner` to traverse shadow roots and fingerprint elements inside Web Components. |
| 1.2 | iframe element healing | High | Planned | Support healing for elements inside `<iframe>` documents by switching context during DOM scanning. |
| 1.3 | CSS selector baseline strategy | Medium | Planned | Add CSS selector as an additional locator strategy for baseline fingerprinting alongside text, ARIA, and attribute matching. |
| 1.4 | Configurable weight profiles | Medium | Planned | Allow per-application weight profiles (e.g., higher text weight for content sites, higher ARIA weight for accessible apps). |
| 1.5 | Healing event notifications | Medium | Planned | Optional webhook or callback on healing events for CI/CD pipeline integration. |
| 1.6 | Baseline migration tooling | Medium | Planned | CLI commands to diff, merge, and migrate baselines between application versions. |
| 1.7 | Python 3.13 support | Low | Planned | Test and certify compatibility with Python 3.13 when released. |

---

## Tier 2 — Mid-Term (Community-Driven)

These features expand SelfHeal's reach and are candidates for a 2.x major release.

| # | Feature | Priority Score | Status | Description |
|---|---|---|---|---|
| 2.1 | Selenium WebDriver adapter | High | Research | Port the `SelfHealingPage` composition pattern to Selenium, providing the same fingerprint-and-heal lifecycle. |
| 2.2 | Visual regression integration | Medium | Research | Use pixel-level comparison (OpenCV / Pixelmatch) as a supplementary verification layer after healing — confirm the healed element renders similarly to the baseline. |
| 2.3 | Healing event export | Medium | Planned | Export healing events and audit trails in JSON, CSV, and JUnit XML formats for CI/CD reporting. |
| 2.4 | Multi-browser fingerprinting | Medium | Research | Normalise fingerprints across Chromium, Firefox, and WebKit to support cross-browser test suites. |
| 2.5 | Playwright pytest plugin | Medium | Planned | Provide a `pytest` plugin that auto-wraps Playwright pages in `SelfHealingPage` via fixtures, eliminating manual integration. |
| 2.6 | Baseline versioning and rollback | Low | Planned | Git-style baseline version history with rollback capabilities. |
| 2.7 | Team dashboard | Low | Research | Multi-user dashboard with role-based access for team-wide healing event monitoring. |

---

## Tier 3 — Research (SelfHeal 2.0 Directions)

These are exploratory research tracks. No implementation timeline is set.

| # | Feature | Feasibility | Description |
|---|---|---|---|
| 3.1 | Local vision model verification | Medium | Use a lightweight local vision model (e.g., CLIP) to verify that a healed element is visually consistent with the baseline — not for candidate selection, but as a post-healing confidence check. |
| 3.2 | Distributed analytics platform | Medium | Aggregate healing telemetry across multiple projects and teams to identify common failure patterns and weight optimisation opportunities. |
| 3.3 | Cross-browser fingerprint normalisation | High | Develop a normalisation layer that produces consistent fingerprints regardless of browser engine (Chromium vs Firefox vs WebKit). |
| 3.4 | Playwright for Java / .NET adapters | Medium | Extend the SelfHeal architecture to Playwright's Java and .NET bindings. |
| 3.5 | Adaptive weight learning | Low | Use historical healing event data to automatically adjust similarity dimension weights per application — while maintaining deterministic, explainable decisions. |
| 3.6 | DOM diffing integration | Medium | Compare baseline DOM snapshots with current DOM to detect structural patterns and improve candidate ranking. |
| 3.7 | Accessibility tree healing | High | Use the browser's accessibility tree (rather than raw DOM) as the primary fingerprinting source for screen-reader-focused test suites. |

---

## Version Planning

| Version | Scope | Timeline |
|---|---|---|
| **1.0.x** | Bug fixes, documentation improvements, pilot feedback | Current |
| **1.1.0** | Tier 1 items 1.1–1.3 (Shadow DOM, iframe, CSS selector) | After pilot completion |
| **1.2.0** | Tier 1 items 1.4–1.6 (weight profiles, notifications, migration) | Community-driven |
| **2.0.0** | Tier 2 items (Selenium adapter, visual regression, pytest plugin) | Research-validated |

---

## How to Propose a Feature

1. Search [existing issues](https://github.com/Optimus1o1/selfhealing-ui/issues) for duplicates.
2. Open a [Feature Request](https://github.com/Optimus1o1/selfhealing-ui/issues/new?template=feature_request.yml).
3. Community discussion determines priority score.
4. Features are added to this roadmap after evaluation.

---

## Contribution Guidelines

- All contributions must maintain or improve the canonical benchmark metrics (100% precision, 0% FPR).
- New scoring dimensions or weight changes require a full benchmark run with before/after comparison.
- See [CONTRIBUTING.md](../CONTRIBUTING.md) for development setup and PR guidelines.

---

*Moon Sanctum Labs — Decode. Build. Evolve.*
