# Contributing to Self-Healing UI Automation Framework

Thank you for your interest in contributing to the **Self-Healing UI Automation Framework** by **Moon Sanctum Labs** (*Decode. Build. Evolve.*).

---

## Development Principles

1. **Deterministic Over Heuristic**: The intelligence engine relies on strict, verifiable mathematical similarities (RapidFuzz, Jaccard, Token Sort, positional geometry, DOM hierarchy) — no probabilistic LLMs or non-reproducible APIs.
2. **Actionability Before Healing**: An element failure is only a candidate for healing if the original locator matches 0 elements. If the element exists but is hidden, disabled, or occluded, it is an actionability failure and must NOT be healed.
3. **Ambiguity Protection**: When multiple candidates score within `minimum_score_margin` (default `0.10`) of each other, the engine must abstain rather than guess.
4. **Safety & Security**: Never commit credentials, private data, or unescaped HTML templates. All input values of type `password` must remain redacted.

---

## Setting Up Your Development Environment

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Optimus1o1/selfhealing-ui.git
   cd selfhealing-ui
   ```

2. **Create and activate a virtual environment**:
   ```bash
   python -m venv .venv
   # Windows:
   .venv\Scripts\activate
   # Linux/macOS:
   source .venv/bin/activate
   ```

3. **Install editable package and test dependencies**:
   ```bash
   pip install -e ".[dev]"
   playwright install chromium
   ```

---

## Running Tests and Benchmarks

- **Run all automated tests**:
  ```bash
  python -m pytest tests/ -v
  ```

- **Run the 57-scenario baseline benchmark**:
  ```bash
  python tests/evaluation/benchmark.py
  ```

- **Run the 52-scenario independent holdout validation**:
  ```bash
  python tests/evaluation/holdout_benchmark.py
  ```

- **Run the multi-tier performance profiler (500+ iterations)**:
  ```bash
  python tests/evaluation/profile_performance.py
  ```

---

## Pull Request Guidelines

- Format code using standard PEP 8 conventions.
- All new features or locator scoring adaptations must include unit tests in `tests/unit/`.
- Ensure all 30 unit and healing tests pass before opening a PR.
- Conventional Commits format is enforced: `feat:`, `fix:`, `test:`, `docs:`, `refactor:`.
- Use the [Pull Request Template](/.github/PULL_REQUEST_TEMPLATE.md) — it will load automatically when you open a PR on GitHub.

---

## Release Contribution Policy

### What Can Be Contributed

| Contribution Type | Requirements |
|---|---|
| Bug fixes | Must include a regression test and pass the full benchmark suite |
| Documentation | Factual accuracy required — no invented claims or results |
| New test scenarios | Must not modify existing benchmark datasets |
| Configuration options | Must be backward-compatible with existing `configs/default.yaml` |
| Dashboard improvements | Must not alter healing engine behaviour |
| Compatibility reports | Submit via the [Compatibility Report](https://github.com/Optimus1o1/selfhealing-ui/issues/new?template=compatibility_report.yml) issue template |

### What Requires Discussion First

- Changes to similarity scoring weights or dimensions
- Changes to threshold or margin defaults
- New locator strategy support
- New dependencies
- Breaking API changes

Open a [Feature Request](https://github.com/Optimus1o1/selfhealing-ui/issues/new?template=feature_request.yml) and wait for maintainer feedback before submitting a PR for these.

### Benchmark Protection

Any PR that modifies the healing engine (`intelligence.py`, `detection.py`, `scanner.py`) must include:

1. Full benchmark run before the change (109 scenarios).
2. Full benchmark run after the change.
3. Before/after comparison table in the PR description.
4. No reduction in precision (must remain 100%).
5. No increase in false positive rate (must remain 0%).

---

## Discussion Guidelines

- **Be specific.** Include version numbers, OS, Python version, and Playwright version.
- **Provide evidence.** Attach CLI output, dashboard screenshots, or healing event logs.
- **One topic per issue.** Do not combine unrelated bugs or feature requests.
- **Search first.** Check existing issues before opening a new one.
- **Be constructive.** Focus on the technical problem, not on the person.
- **Respect the philosophy.** SelfHeal is deterministic by design. Proposals that introduce non-reproducible behaviour (cloud APIs, probabilistic models) must clearly justify the trade-off.

