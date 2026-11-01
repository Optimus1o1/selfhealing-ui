# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.0.0rc1| :white_check_mark: |
| < 1.0.0 | :x:                |

---

## Security Architecture & Data Protection

The Self-Healing UI Automation Framework is designed with local-first, privacy-preserving, and deterministic principles.

### 1. Zero External LLM or Cloud Leakage
- All similarity scoring, token parsing, and DOM classification are computed **locally and deterministically** within the Python process and Playwright browser context.
- No DOM snapshots, page text, form values, or screenshots are ever transmitted across external networks or third-party AI APIs.

### 2. Sensitive Attribute & Input Redaction
- During baseline fingerprint generation and DOM extraction, input values are sanitized:
  - Input fields of `type="password"` automatically have their `inner_text`, `value`, and `placeholder` suppressed to empty strings before persistence.
  - Attributes matching sensitive keys (`password`, `token`, `secret`, `auth`, `apikey`, `api_key`, `access_token`, `credit_card`, `cvv`, `ssn`) are purged or excluded during DOM scanning.

### 3. SQL Injection Prevention
- All database operations in `selfheal.database` and `selfheal.baseline.repository` use strictly **parameterized SQL queries** (`?` placeholders via Python's standard `sqlite3`).
- No raw string interpolation is performed on table names or locator expressions.

### 4. Cross-Site Scripting (XSS) Prevention in HTML Reports
- HTML report generation in `selfheal.reporting.report_generator` enforces strict autoescaping via Jinja2:
  ```python
  Environment(loader=..., autoescape=select_autoescape(["html", "xml"]))
  ```
- Untrusted DOM content or attribute strings extracted during test execution cannot execute arbitrary JavaScript in generated test reports or audits.

### 5. Single-Retry Safeguard
- Autonomous healing is limited to a single retry per locator failure (`retry_limit = 1`).
- Cascading retry loops, non-deterministic action repeats, and runaway automated clicks are structurally prevented.

---

## Reporting a Vulnerability

If you discover a security vulnerability in this framework:
1. Please report it privately by contacting **security@moonsanctum.com** or reaching out directly to the maintainers.
2. Please do not open a public issue on GitHub until the vulnerability has been evaluated and patched.
3. Include detailed steps to reproduce the issue, including Playwright scripts or DOM fixtures if applicable.
