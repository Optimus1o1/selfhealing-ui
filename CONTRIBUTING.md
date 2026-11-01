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
   git clone https://github.com/moonsanctum/selfhealing-ui.git
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
- Ensure all 23 unit and integration tests pass before opening a PR.
- Conventional Commits format is enforced: `feat:`, `fix:`, `test:`, `docs:`, `refactor:`.
