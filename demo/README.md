# SelfHeal Demonstration Environment

**Moon Sanctum Labs** — *Decode. Build. Evolve.*  
**Lead Engineer:** Aniket Nandi (Kolkata, IST)  
**Framework Version:** `1.0.0rc1` (Release Candidate 1)  

This directory contains the self-contained demonstration environment for **SelfHeal**, showcasing the framework's autonomous self-healing capabilities on a realistic, multi-page e-commerce application.

---

## 🏬 Demonstration Application Architecture

The demo application (`demo_app/ecommerce.py`) provides two distinct versions of a complete e-commerce storefront:

| Page / Capability | Version 1 (Baseline DOM) | Version 2 (Refactored DOM) | Mutation Types Applied |
| :--- | :--- | :--- | :--- |
| **Login** | `/ecommerce/v1/login` | `/ecommerce/v2/login` | ID renamed (`#btnLogin` $\rightarrow$ `#btnSignInSubmit`), Tailwind styling (`.btn-action-primary`), phrase change ("Login" $\rightarrow$ "Sign In") |
| **Registration** | `/ecommerce/v1/register` | `/ecommerce/v2/register` | Reordered input fields, modified wrapper styling |
| **Product Catalog** | `/ecommerce/v1/products` | `/ecommerce/v2/products` | Kebab-case IDs (`#btnAddToCart1` $\rightarrow$ `#btn-add-bag-101`), phrase change ("Add to Cart" $\rightarrow$ "Add to Bag"), **3 identical candidates** disambiguated by W3C accessible name |
| **Shopping Bag** | `/ecommerce/v1/cart` | `/ecommerce/v2/cart` | Button text change ("Proceed to Checkout" $\rightarrow$ "Continue to Payment"), ID renamed (`#btnProceedCheckout` $\rightarrow$ `#btn-checkout-step`) |
| **Checkout** | `/ecommerce/v1/checkout` | `/ecommerce/v2/checkout` | DOM restructured into nested `<fieldset>` containers, ID renamed (`#btnPlaceOrder` $\rightarrow$ `#btnCompletePurchase`), phrase change ("Place Order" $\rightarrow$ "Complete Purchase") |
| **Order Confirmation** | `/ecommerce/v1/order-success` | `/ecommerce/v2/order-success` | Layout updated, brand styling |
| **Safety Diagnostics** | `/ecommerce/ambiguous` | `/ecommerce/ambiguous` | **Ambiguity Guardrail:** 2 near-tie payment buttons (margin < 0.10)<br>**Actionability Guardrail:** Disabled express checkout button |

---

## 🎬 7 Core Demonstration Scenarios (A through G)

The demo runner verifies 7 core scenarios:

1. **Scenario A (Baseline Creation):** Captures multi-dimensional element fingerprints on Version 1 DOM during initial successful test run.
2. **Scenario B (ID Mutation):** Repairs `#btnLogin` after developer renames ID to `#btnSignInSubmit`.
3. **Scenario C (Text Mutation):** Repairs `#btnProceedCheckout` after label changes from "Proceed to Checkout" to "Continue to Payment".
4. **Scenario D (DOM Restructuring):** Repairs `#btnPlaceOrder` when the checkout form is restructured into nested fieldsets with brand styling.
5. **Scenario E (Multi-Candidate Disambiguation):** In a product catalog with 3 identical "Add to Bag" buttons, correctly identifies the targeted item (`#btn-add-bag-101`) using accessible name semantics without clicking the wrong product.
6. **Scenario F (Ambiguity Protection):** When 2 candidate buttons have identical text and structure (score margin = 0.0049 < 0.10), the engine **safely abstains** with `REJECTED_AMBIGUOUS_MATCH` rather than guessing.
7. **Scenario G (Actionability Protection):** When an element exists in the DOM but is disabled, the failure detector intercepts the state, classifies it as `ELEMENT_DISABLED`, and aborts without attempting healing.

---

## 🚀 Quick Start & Execution Instructions

### 1. Run Complete Demonstration (One Command)

From the project root:
```bash
# Autonomous headless run with colored terminal logs
python demo/run_demo.py

# Run in headed mode to visually inspect the browser actions live
python demo/run_demo.py --headed
```

Visual evidence screenshots are automatically saved to `artifacts/screenshots/demo/`:
- `01_scenario_a_v1_login_baseline.png`
- `02_scenario_a_v1_checkout_baseline.png`
- `03_scenario_b_v2_login_mutated.png`
- `04_scenario_b_v2_login_healed_success.png`
- `05_scenario_e_catalog_grid_candidates.png`
- `06_scenario_e_catalog_item_added_to_cart.png`
- `07_scenario_d_v2_checkout_restructured.png`
- `08_scenario_d_v2_order_success.png`
- `09_scenario_f_ambiguous_candidates.png`
- `10_scenario_g_disabled_target.png`

---

### 2. Manual Version Switching & Exploration

To manually view or interact with the demonstration application:

1. Start the local server:
   ```bash
   python -c "from demo_app.app import DemoServer; s = DemoServer(port=8089); s.start(); import time; print('Server running at http://127.0.0.1:8089/ecommerce/v1'); time.sleep(3600)"
   ```
2. Navigate in any browser:
   - **Version 1 (Original):** `http://127.0.0.1:8089/ecommerce/v1/login`
   - **Version 2 (Mutated):** `http://127.0.0.1:8089/ecommerce/v2/login`
   - **Diagnostics Page:** `http://127.0.0.1:8089/ecommerce/ambiguous`

---

### 3. Run Automated Pytest Scenarios

```bash
# Run the complete demonstration test suite
python -m pytest tests/demo/test_ecommerce_demonstration.py -v

# Run the complete regression test suite (26 tests)
python -m pytest tests/ -v
```

---

### 4. Launch Streamlit Audit Dashboard

To inspect the captured healing events, score breakdowns, and human-in-the-loop promotion workflow:
```bash
streamlit run src/selfheal/dashboard/app.py
```
Open `http://localhost:8501` to view:
- **Tab 1: Test Execution Overview:** Summary of test runs and healed counters.
- **Tab 2: Healing Events & Score Inspector:** Side-by-side locator diff and 6-dimension score breakdown (Text, Role, Attributes, Parent, Children, Position).
- **Tab 3: Assisted Review & Promotion:** One-click **Approve & Promote** to baseline v2 or **Reject Repair**.
- **Tab 4: Baseline Version Comparison:** Side-by-side evolution of baseline versions (v1 vs v2).
- **Tab 5: Performance & Latency Analytics:** Percentiles (P50, P90, P95) and action timeout dominance analysis.

---

## 📋 Expected Output Example

When running `python demo/run_demo.py`, you should see:
```text
================================================================================
   SELFHEAL -- REPRODUCIBLE DEMONSTRATION SUITE (SCENARIOS A - G)
   Moon Sanctum Labs | Decode. Build. Evolve. | Lead: Aniket Nandi
================================================================================

[INIT] SQLite database cleanly reset at 'artifacts/selfheal.db' (WAL Mode)
[INIT] Demo E-Commerce server online at http://127.0.0.1:8089/ecommerce/v1

[SCENARIO A] Successful Baseline Creation (Version 1)
            Capturing multi-dimensional DOM fingerprints during initial test run
            -> [SCREENSHOT] Saved evidence to: 01_scenario_a_v1_login_baseline.png
            -> [BASELINE SAVED] ecom.auth.submit -> #btnLogin (Version 1 Active)
            -> [BASELINE SAVED] ecom.products.add_item1 -> #btnAddToCart1 (Version 1 Active)
            -> [BASELINE SAVED] ecom.cart.checkout_action -> #btnProceedCheckout (Version 1 Active)
            -> [SCREENSHOT] Saved evidence to: 02_scenario_a_v1_checkout_baseline.png
            -> [BASELINE SAVED] ecom.checkout.place_order -> #btnPlaceOrder (Version 1 Active)
            -> [SUCCESS] V1 Order placed! Confirmation: Order Confirmed!

================================================================================
   SWITCHING TO VERSION 2: EXECUTING UNCHANGED PLAYWRIGHT SCRIPTS
================================================================================

[SCENARIO B] Successful Healing After an ID Change
            Original #btnLogin mutated to #btnSignInSubmit with Tailwind classes
            -> [SCREENSHOT] Saved evidence to: 03_scenario_b_v2_login_mutated.png
            -> [HEALED] Original: #btnLogin -> Healed: #btnSignInSubmit | Score: 0.8487 | Time: 3589.2ms
            -> [SCREENSHOT] Saved evidence to: 04_scenario_b_v2_login_healed_success.png

[SCENARIO E] Disambiguation with Multiple Candidates (Catalog Grid)
            3 identical 'Add to Bag' buttons exist; matching #btnAddToCart1 to #btn-add-bag-101 using accessible names
            -> [SCREENSHOT] Saved evidence to: 05_scenario_e_catalog_grid_candidates.png
            -> [HEALED] Original: #btnAddToCart1 -> Healed: #btn-add-bag-101 | Score: 0.8331 | Time: 3583.3ms
            -> [SCREENSHOT] Saved evidence to: 06_scenario_e_catalog_item_added_to_cart.png

[SCENARIO C] Healing After a Button Text Change
            Button text changed from 'Proceed to Checkout' to 'Continue to Payment'
            -> [HEALED] Original: #btnProceedCheckout -> Healed: #btn-checkout-step | Score: 0.8493 | Time: 3600.4ms

[SCENARIO D] Healing After DOM Restructuring
            Checkout form restructured into nested fieldsets, renamed inputs, and mutated #btnCompletePurchase
            -> [SCREENSHOT] Saved evidence to: 07_scenario_d_v2_checkout_restructured.png
            -> [HEALED] Original: #btnPlaceOrder -> Healed: #btnCompletePurchase | Score: 0.8512 | Time: 3603.8ms
            -> [VERIFIED] V2 Order Confirmed: Transaction Complete
            -> [SCREENSHOT] Saved evidence to: 08_scenario_d_v2_order_success.png

[SCENARIO F] Correct Rejection of Ambiguous Candidates
            Two near-tie payment buttons (#payMethodOption1 vs #payMethodOption2) trigger safety margin guardrail
            -> [SCREENSHOT] Saved evidence to: 09_scenario_f_ambiguous_candidates.png
            -> [REJECTED_AMBIGUOUS_MATCH] Safety Triggered: Margin < 0.10

[SCENARIO G] Correct Rejection of Missing or Disabled Elements
            Disabled button classified as ELEMENT_DISABLED and aborted without healing
            -> [SCREENSHOT] Saved evidence to: 10_scenario_g_disabled_target.png
            -> [REJECTED_ACTIONABILITY] Safety Triggered: ELEMENT_DISABLED

================================================================================
   BASELINE PROMOTION: AUDITED PROMOTION TO VERSION 2
================================================================================
            -> [PROMOTED] ecom.auth.submit is now at version 2 with selector '#btnSignInSubmit'

================================================================================
   ALL SCENARIOS A THROUGH G SUCCESSFULLY DEMONSTRATED
================================================================================
```

---

## 🔧 Troubleshooting Guide

### 1. Port 8089 or 8501 Already in Use
- **Symptom:** `OSError: [Errno 48] Address already in use` or `[Errno 10048]`.
- **Solution:**
  - Close any existing Python processes:
    - On Windows PowerShell: `Get-Process python* | Stop-Process -Force`
    - On macOS/Linux: `pkill -f "python.*demo"`
  - Or specify an alternate port in `demo/run_demo.py` or `streamlit run src/selfheal/dashboard/app.py --server.port 8502`.

### 2. Playwright Browser Binaries Missing
- **Symptom:** `playwright._impl._errors.Error: Executable doesn't exist at ...`
- **Solution:** Run the Playwright installer to install the local Chromium engine:
  ```bash
  playwright install chromium
  ```

### 3. SQLite Database Locked
- **Symptom:** `sqlite3.OperationalError: database is locked`.
- **Solution:** SelfHeal uses SQLite with Write-Ahead Logging (`PRAGMA journal_mode = WAL`) and a 5,000 ms busy timeout. If a previous test was forcibly killed, remove any stale journal files:
  ```bash
  selfheal reset-db
  ```

### 4. Terminal Encoding (Windows PowerShell)
- **Symptom:** `UnicodeEncodeError: 'charmap' codec can't encode character...`.
- **Solution:** Ensure your console supports UTF-8:
  ```powershell
  $OutputEncoding = [Console]::InputEncoding = [Console]::OutputEncoding = New-Object System.Text.UTF8Encoding
  ```

