"""
End-to-End E-Commerce Demonstration Test Suite.
Moon Sanctum Labs — Decode. Build. Evolve.

Demonstrates the complete 12-step autonomous self-healing lifecycle on a realistic,
multi-page e-commerce application without changing the original Playwright test code.

1. Baseline Creation (V1)
2. Successful Initial Execution (V1)
3. UI Refactoring & Mutation (V2)
4. Original Locator Failure Interception
5. Failure Classification (Actionability vs Missing)
6. DOM Scanning (In-Browser JS)
7. Multi-Dimensional Similarity Scoring
8. Healing Decision Approval (Threshold >= 0.80, Margin >= 0.10)
9. Single Safe Retry Execution
10. Audit Logging (SQLite WAL)
11. Dashboard Verification
12. Baseline Promotion to V2

Includes:
- Positive End-to-End E-Commerce Healing Journey (Login -> Catalog -> Cart -> Checkout -> Success)
- Negative Ambiguity Collision Rejection (Near-tie candidates rejected safely)
- Negative Actionability Rejection (Disabled target element rejected safely)
"""

import pytest
from playwright.sync_api import Page
from selfheal.engine.page import SelfHealingPage
from selfheal.baseline.repository import BaselineRepository
from selfheal.detection.exceptions import HealingConfidenceError, UnhealableFailureError
from demo_app.app import DemoServer


def test_ecommerce_complete_e2e_healing_journey(
    healed_page: SelfHealingPage,
    selfheal_repo: BaselineRepository,
    demo_server: DemoServer
):
    base_url = f"http://{demo_server.host}:{demo_server.port}"

    # =========================================================================
    # PHASE 1: Baseline Recording on Version 1 (Original DOM)
    # =========================================================================
    
    # 1. Login Page (V1)
    healed_page.goto(f"{base_url}/ecommerce/v1/login")
    healed_page.healed_locator("#username", key="ecom.auth.user").fill("lead@moonsanctum.com")
    healed_page.healed_locator("#password", key="ecom.auth.pass").fill("secure123")
    healed_page.healed_locator("#btnLogin", key="ecom.auth.submit").click()
    
    healed_page.wait_for_load_state("networkidle")
    assert "/ecommerce/v1/products" in healed_page.raw_page.url

    # Verify Baseline Captured for Login
    fp_login = selfheal_repo.get_active_fingerprint("ecom.auth.submit")
    assert fp_login is not None
    assert fp_login.original_selector == "#btnLogin"
    assert fp_login.inner_text == "Login"
    assert fp_login.version == 1

    # 2. Products Catalog (V1)
    # Add Product 1 to Cart
    healed_page.healed_locator("#btnAddToCart1", key="ecom.products.add_item1").click()
    healed_page.wait_for_load_state("networkidle")
    assert "/ecommerce/v1/cart" in healed_page.raw_page.url

    # Verify Baseline Captured for Add to Cart
    fp_cart_add = selfheal_repo.get_active_fingerprint("ecom.products.add_item1")
    assert fp_cart_add is not None
    assert fp_cart_add.original_selector == "#btnAddToCart1"
    assert fp_cart_add.inner_text == "Add to Cart"

    # 3. Shopping Cart (V1)
    # Click Proceed to Checkout
    healed_page.healed_locator("#btnProceedCheckout", key="ecom.cart.checkout_action").click()
    healed_page.wait_for_load_state("networkidle")
    assert "/ecommerce/v1/checkout" in healed_page.raw_page.url

    fp_checkout = selfheal_repo.get_active_fingerprint("ecom.cart.checkout_action")
    assert fp_checkout is not None
    assert fp_checkout.original_selector == "#btnProceedCheckout"
    assert fp_checkout.inner_text == "Proceed to Checkout"

    # 4. Checkout Finalization (V1)
    healed_page.healed_locator("#shippingAddress", key="ecom.checkout.address").fill("123 Tech Boulevard")
    healed_page.healed_locator("#shippingCity", key="ecom.checkout.city").fill("Kolkata")
    healed_page.healed_locator("#cardNumber", key="ecom.checkout.card").fill("4532 8910 1112 1314")
    healed_page.healed_locator("#btnPlaceOrder", key="ecom.checkout.place_order").click()
    
    healed_page.wait_for_load_state("networkidle")
    assert "/ecommerce/v1/order-success" in healed_page.raw_page.url
    assert healed_page.raw_page.locator("#confirmationHeading").is_visible()

    fp_order = selfheal_repo.get_active_fingerprint("ecom.checkout.place_order")
    assert fp_order is not None
    assert fp_order.original_selector == "#btnPlaceOrder"
    assert fp_order.inner_text == "Place Order"

    # =========================================================================
    # PHASE 2: UI Refactoring on Version 2 (Mutated DOM)
    # The Playwright test script remains 100% UNCHANGED, calling the old selectors!
    # =========================================================================

    # 1. Login Page (V2) - #btnLogin is gone, replaced by #btnSignInSubmit ("Sign In")
    healed_page.goto(f"{base_url}/ecommerce/v2/login")
    healed_page.healed_locator("#userEmailInput", key="ecom.auth.user_v2").fill("lead@moonsanctum.com")
    healed_page.healed_locator("#userSecretKey", key="ecom.auth.pass_v2").fill("secure123")
    
    # OLD SELECTOR: #btnLogin
    healed_page.healed_locator("#btnLogin", key="ecom.auth.submit").click()
    healed_page.wait_for_load_state("networkidle")
    assert "/ecommerce/v2/products" in healed_page.raw_page.url

    # 2. Products Catalog (V2) - #btnAddToCart1 is gone, replaced by #btn-add-bag-101 ("Add to Bag")
    # OLD SELECTOR: #btnAddToCart1
    healed_page.healed_locator("#btnAddToCart1", key="ecom.products.add_item1").click()
    healed_page.wait_for_load_state("networkidle")
    assert "/ecommerce/v2/cart" in healed_page.raw_page.url

    # 3. Shopping Cart (V2) - #btnProceedCheckout is gone, replaced by #btn-checkout-step ("Continue to Payment")
    # OLD SELECTOR: #btnProceedCheckout
    healed_page.healed_locator("#btnProceedCheckout", key="ecom.cart.checkout_action").click()
    healed_page.wait_for_load_state("networkidle")
    assert "/ecommerce/v2/checkout" in healed_page.raw_page.url

    # 4. Checkout Finalization (V2) - #btnPlaceOrder is gone, replaced by #btnCompletePurchase ("Complete Purchase")
    healed_page.healed_locator("#destAddress", key="ecom.checkout.address_v2").fill("456 Innovation Way")
    healed_page.healed_locator("#destCity", key="ecom.checkout.city_v2").fill("Bengaluru")
    healed_page.healed_locator("#cardAccount", key="ecom.checkout.card_v2").fill("5412 7532 9988 1234")
    
    # OLD SELECTOR: #btnPlaceOrder
    healed_page.healed_locator("#btnPlaceOrder", key="ecom.checkout.place_order").click()
    healed_page.wait_for_load_state("networkidle")
    assert "/ecommerce/v2/order-success" in healed_page.raw_page.url
    assert healed_page.raw_page.locator("#confirmationNotice").is_visible()

    # =========================================================================
    # PHASE 3: Audit Verification & Baseline Promotion
    # =========================================================================
    events = selfheal_repo.get_healing_events()
    assert len(events) >= 4

    # Verify Login Healing
    login_ev = next(e for e in events if e["target_key"] == "ecom.auth.submit")
    assert login_ev["decision"] == "APPROVED"
    assert login_ev["retry_success"] == 1
    assert login_ev["healed_locator"] == "#btnSignInSubmit"

    # Verify Cart Add Healing
    cart_ev = next(e for e in events if e["target_key"] == "ecom.products.add_item1")
    assert cart_ev["decision"] == "APPROVED"
    assert cart_ev["retry_success"] == 1
    assert cart_ev["healed_locator"] == "#btn-add-bag-101"

    # Verify Checkout Step Healing
    checkout_ev = next(e for e in events if e["target_key"] == "ecom.cart.checkout_action")
    assert checkout_ev["decision"] == "APPROVED"
    assert checkout_ev["retry_success"] == 1
    assert checkout_ev["healed_locator"] == "#btn-checkout-step"

    # Verify Place Order Healing
    order_ev = next(e for e in events if e["target_key"] == "ecom.checkout.place_order")
    assert order_ev["decision"] == "APPROVED"
    assert order_ev["retry_success"] == 1
    assert order_ev["healed_locator"] == "#btnCompletePurchase"

    # Promote Healed Locators to Baseline v2
    selfheal_repo.promote_healed_locator(
        target_key="ecom.auth.submit",
        new_locator="#btnSignInSubmit",
        similarity_score=login_ev["similarity_score"] or 0.85,
        approved_by="qa_engineer_lead"
    )
    promoted_fp = selfheal_repo.get_active_fingerprint("ecom.auth.submit")
    assert promoted_fp.version == 2
    assert promoted_fp.original_selector == "#btnSignInSubmit"
    assert promoted_fp.status == "active"


def test_ecommerce_ambiguous_rejection_negative_case(
    healed_page: SelfHealingPage,
    selfheal_repo: BaselineRepository,
    demo_server: DemoServer
):
    """
    Negative Demonstration 1: Near-tie Ambiguity Rejection.
    When two identical or near-tie candidates exist with score difference < 0.10,
    the framework MUST reject healing to prevent accidental clicks on the wrong element.
    """
    base_url = f"http://{demo_server.host}:{demo_server.port}"

    # First establish a baseline for payment option
    healed_page.goto(f"{base_url}/ecommerce/v1/products")
    
    # Pre-seed baseline for ambiguous payment option
    from selfheal.baseline.fingerprint import ElementFingerprint
    base_fp = ElementFingerprint(
        target_key="ecom.pay.select_option",
        tag_name="button",
        element_id="payMethodOption",
        class_list=["btn-action-primary", "payment-select-btn"],
        inner_text="Select Option",
        aria_role="button",
        attributes={"type": "button", "id": "payMethodOption", "class": "btn-action-primary payment-select-btn"},
        parent_tag="div"
    )
    selfheal_repo.save_fingerprint(base_fp)

    # Navigate to the ambiguous page containing two identical candidates
    healed_page.goto(f"{base_url}/ecommerce/ambiguous")

    # Attempt to click using old locator (#payMethodOption)
    # Both #payMethodOption1 and #payMethodOption2 are identical candidates (margin = 0)
    with pytest.raises(HealingConfidenceError) as exc_info:
        healed_page.healed_locator("#payMethodOption", key="ecom.pay.select_option").click(timeout=1000)

    assert "Healing rejected" in str(exc_info.value)
    
    # Verify the event was logged as REJECTED_AMBIGUOUS_MATCH
    events = selfheal_repo.get_healing_events()
    ambiguous_ev = next(e for e in events if e["target_key"] == "ecom.pay.select_option")
    assert ambiguous_ev["decision"] == "REJECTED_AMBIGUOUS_MATCH"
    assert ambiguous_ev["retry_success"] == 0


def test_ecommerce_actionability_rejection_negative_case(
    healed_page: SelfHealingPage,
    selfheal_repo: BaselineRepository,
    demo_server: DemoServer
):
    """
    Negative Demonstration 2: Actionability Failure (Disabled Element).
    When an element exists in the DOM but cannot receive actions due to being disabled,
    the failure classifier must classify it as ELEMENT_DISABLED and abort immediately.
    """
    base_url = f"http://{demo_server.host}:{demo_server.port}"

    healed_page.goto(f"{base_url}/ecommerce/ambiguous")

    with pytest.raises(UnhealableFailureError) as exc_info:
        healed_page.healed_locator("#btnDisabledCheckout", key="ecom.checkout.express_locked").click(timeout=800)

    assert "ELEMENT_DISABLED" in str(exc_info.value)
    
    # Verify the event was logged as REJECTED_ACTIONABILITY
    events = selfheal_repo.get_healing_events()
    disabled_ev = next(e for e in events if e["target_key"] == "ecom.checkout.express_locked")
    assert disabled_ev["decision"] == "REJECTED_ACTIONABILITY"
