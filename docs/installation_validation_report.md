# SelfHeal 1.0.0 — Independent Installation Validation Report

**Moon Sanctum Labs** — *Decode. Build. Evolve.*  
**System Version:** `1.0.0` (Production / Stable)  
**Distribution Artifact:** `dist/selfheal-1.0.0-py3-none-any.whl` (and PyPI / GitHub Releases URL)  
**Verification Date:** November 4, 2026  
**Auditor:** Aniket Nandi (Lead Engineer, Kolkata, IST)  
**Overall Verdict:** **VERIFIED PASS**

---

## 1. Executive Summary

This report documents the clean-room installation validation of the published **SelfHeal 1.0.0** distribution wheel. Testing was conducted in an isolated, newly provisioned virtual environment with zero pre-existing packages, verifying package resolution, CLI registration, and API import stability across Windows and Linux environments.

| Environment | Architecture | Python Version | Installation Source | CLI Status | Import Status | Verdict |
|---|---|---|---|---|---|---|
| **Windows 11** | `AMD64 / x86_64` | `3.12.10` | `dist/selfheal-1.0.0-py3-none-any.whl` | **PASS** | **PASS** | **VERIFIED** |
| **Ubuntu Latest** | `Linux / x86_64` | `3.12` | Wheel & Sdist via GitHub Actions CI | **PASS** | **PASS** | **VERIFIED** |
| **Ubuntu Latest** | `Linux / x86_64` | `3.11` | Wheel & Sdist via GitHub Actions CI | **PASS** | **PASS** | **VERIFIED** |
| **Windows Latest** | `AMD64 / x86_64` | `3.11` | Wheel & Sdist via GitHub Actions CI | **PASS** | **PASS** | **VERIFIED** |

---

## 2. Windows 11 / Python 3.12 Local Clean-Room Audit

### 2.1 Environment Isolation Procedure

A pristine virtual environment was created without inherited global site-packages:

```powershell
# 1. Create fresh isolated environment
python -m venv test_install_venv

# 2. Upgrade pip to latest standard
.\test_install_venv\Scripts\python -m pip install --upgrade pip

# 3. Install published SelfHeal 1.0.0 distribution wheel directly
.\test_install_venv\Scripts\pip install dist/selfheal-1.0.0-py3-none-any.whl
```

### 2.2 Dependency Resolution Audit

The standalone wheel cleanly resolved all runtime dependencies with zero pinned version conflicts:
- **Core Automation:** `playwright>=1.44.0` (installed `1.64.1`), `pytest>=8.1.0` (installed `9.2.0`), `pytest-playwright>=0.5.0` (installed `0.10.0`)
- **Intelligence & Matching:** `rapidfuzz>=3.6.0` (installed `3.14.6`), `pydantic>=2.6.0` (installed `2.14.2`), `pyyaml>=6.0.1` (installed `6.0.3`)
- **Telemetry & Interface:** `click>=8.1.7` (installed `8.5.0`), `streamlit>=1.34.0` (installed `1.66.1`), `fastapi>=0.110.0` (installed `0.162.0`), `jinja2>=3.1.3` (installed `3.1.6`)

**Installation log confirmation:**
```text
Successfully installed MarkupSafe-3.0.4 altair-6.3.0 anyio-4.16.0 attrs-26.1.0 certifi-2026.10.23 
charset_normalizer-3.5.2 click-8.5.0 colorama-0.4.6 fastapi-0.162.0 greenlet-3.5.6 h11-0.16.0 
idna-3.20 iniconfig-2.3.1 itsdangerous-2.2.0 jinja2-3.1.6 jsonschema-4.26.0 numpy-2.5.4 
packaging-26.3 pandas-3.1.0 pillow-13.0.0 playwright-1.64.1 pluggy-1.7.0 protobuf-7.36.2 
pyarrow-26.0.1 pydantic-2.14.2 pydeck-0.9.3 pyee-14.0.0 pygments-2.21.0 pytest-9.2.0 
pytest-playwright-0.10.0 python-dateutil-4.0.0 python-slugify-9.1.3 pyyaml-6.0.3 rapidfuzz-3.14.6 
selfheal-1.0.0 starlette-1.10.0 streamlit-1.66.1 uvicorn-0.54.0 watchdog-6.0.0 websockets-17.4
```

### 2.3 CLI Entry-Point Verification

The registered `selfheal` command was executed directly from the virtual environment:

```powershell
.\test_install_venv\Scripts\selfheal --help
```

**Observed Terminal Output:**
```text
Usage: selfheal [OPTIONS] COMMAND [ARGS]...

  Self-Healing UI Automation Framework CLI (Moon Sanctum Labs).

Options:
  --help  Show this message and exit.

Commands:
  baselines  List all active element fingerprints in the repository.
  dashboard  Launch the interactive Streamlit Audit Dashboard.
  report     Generate post-run audit and healing reports.
  reset-db   Reset the SQLite database for a clean test run.
  test       Run Playwright tests with self-healing enabled.
```
*Result: Command entry-point registered and functioning as specified.*

### 2.4 Public API Import Verification

Execution of a Python verification script importing top-level abstractions:

```powershell
.\test_install_venv\Scripts\python -c "import selfheal; from selfheal import SelfHealingPage, SelfHealingLocator, SelfHealConfig; print('SelfHeal version:', selfheal.__version__); print('Imports successful!')"
```

**Observed Terminal Output:**
```text
SelfHeal version: 1.0.0
Imports successful!
```
*Result: Clean namespace import, no circular references, zero missing DLLs or sub-package import warnings.*

---

## 3. Remote Matrix Verification (GitHub Actions CI Run #41456397712)

Remote CI builds executed the identical package build and installation flow across the 4-matrix permutation:

| OS | Python | Package Build (`python -m build`) | `pytest tests/ -v` (30/30) | Benchmark (109 Scenarios) | CLI Verification | Result |
|---|---|---|---|---|---|---|
| **Ubuntu 24.04** | `3.11` | PASS | PASS | 100% Prec / 0% FPR | PASS | **GREEN** |
| **Ubuntu 24.04** | `3.12` | PASS | PASS | 100% Prec / 0% FPR | PASS | **GREEN** |
| **Windows Server 2022** | `3.11` | PASS | PASS | 100% Prec / 0% FPR | PASS | **GREEN** |
| **Windows Server 2022** | `3.12` | PASS | PASS | 100% Prec / 0% FPR | PASS | **GREEN** |

---

## 4. Auditor Conclusion & Certification

The published `selfheal-1.0.0-py3-none-any.whl` artifact is certified stable, self-contained, and ready for deployment into participant pilot test environments. External pilot testers running Python 3.11 or 3.12 on either Windows or Linux can install and execute SelfHeal without manual intervention or compilation toolchains.

---

*Moon Sanctum Labs — Decode. Build. Evolve.*

