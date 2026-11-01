import pytest
from selfheal.engine.page import SelfHealingPage
from selfheal.baseline.repository import BaselineRepository
from demo_app.app import DemoServer


def test_baseline_creation_and_healing_workflow(
    healed_page: SelfHealingPage,
    selfheal_repo: BaselineRepository,
    demo_server: DemoServer
):
    base_url = f"http://{demo_server.host}:{demo_server.port}"

    # -------------------------------------------------------------
    # PHASE 1: Baseline Generation on V1
    # -------------------------------------------------------------
    healed_page.goto(f"{base_url}/v1")
    
    # Fill inputs
    healed_page.healed_locator("#username", key="login.username").fill("admin_user")
    healed_page.healed_locator("#password", key="login.password").fill("admin_pass")

    # Click login button with stable target_key
    submit_btn = healed_page.healed_locator("#loginBtn", key="login.submit_button")
    submit_btn.click()

    # Verify navigation to dashboard
    healed_page.wait_for_load_state("networkidle")
    assert "/dashboard" in healed_page.raw_page.url

    # Verify baseline was saved
    fp = selfheal_repo.get_active_fingerprint("login.submit_button")
    assert fp is not None, "Baseline fingerprint was not stored!"
    assert fp.target_key == "login.submit_button"
    assert fp.original_selector == "#loginBtn"
    assert fp.inner_text == "Login"
    assert fp.tag_name == "button"

    # -------------------------------------------------------------
    # PHASE 2: UI Refactoring & Self-Healing on V2
    # In V2, #loginBtn is gone. Replaced by #signinBtn ("Sign In")
    # -------------------------------------------------------------
    healed_page.goto(f"{base_url}/v2")

    healed_page.healed_locator("#userEmail", key="login.user_email_v2").fill("admin@moonsanctum.com")
    healed_page.healed_locator("#userSecret", key="login.user_pwd_v2").fill("secure_pass")

    # Test script uses OLD locator (#loginBtn) with bound target_key
    old_button_locator = healed_page.healed_locator("#loginBtn", key="login.submit_button")
    
    # This should heal autonomously!
    old_button_locator.click()

    # Verify navigation succeeded via the healed locator
    healed_page.wait_for_load_state("networkidle")
    assert "/dashboard" in healed_page.raw_page.url

    # Verify healing event was logged in SQLite
    events = selfheal_repo.get_healing_events()
    assert len(events) >= 1

    latest_event = next(e for e in events if e["target_key"] == "login.submit_button")
    assert latest_event["decision"] == "APPROVED"
    assert latest_event["retry_success"] == 1
    assert latest_event["original_locator"] == "#loginBtn"
    assert latest_event["similarity_score"] >= 0.85
    assert latest_event["healed_locator"] in ('[data-testid="auth-submit"]', '#signinBtn')
