"""
Complete 10-Step Lifecycle End-to-End Validation Test.
Verifies:
1. Baseline Creation
2. UI Modification
3. Original Locator Failure
4. Failure Classification
5. DOM Scanning
6. Candidate Ranking
7. Healing Decision
8. Single Safe Retry
9. Audit Logging
10. Dashboard Approval & Promotion
"""

import pytest
from selfheal.engine.page import SelfHealingPage
from selfheal.baseline.repository import BaselineRepository
from demo_app.app import DemoServer


def test_complete_ten_step_lifecycle(
    healed_page: SelfHealingPage,
    selfheal_repo: BaselineRepository,
    demo_server: DemoServer
):
    base_url = f"http://{demo_server.host}:{demo_server.port}"

    # -----------------------------------------------------------------
    # STEP 1: Baseline Creation on Original V1 Page
    # -----------------------------------------------------------------
    healed_page.goto(f"{base_url}/v1")

    # Interact with inputs and button using stable target keys
    healed_page.healed_locator("#username", key="auth.user_input").fill("test_qa_lead")
    healed_page.healed_locator("#password", key="auth.pass_input").fill("password123")
    healed_page.healed_locator("#loginBtn", key="auth.login_submit").click()

    healed_page.wait_for_load_state("networkidle")
    assert "/dashboard" in healed_page.raw_page.url

    # Verify Step 1: Baseline records created with version 1
    fp = selfheal_repo.get_active_fingerprint("auth.login_submit")
    assert fp is not None
    assert fp.target_key == "auth.login_submit"
    assert fp.original_selector == "#loginBtn"
    assert fp.version == 1
    assert fp.status == "active"

    # -----------------------------------------------------------------
    # STEP 2-8: UI Modification -> Failure -> Classify -> Scan ->
    #           Rank -> Decision -> Single Safe Retry
    # -----------------------------------------------------------------
    healed_page.goto(f"{base_url}/v2")

    healed_page.healed_locator("#userEmail", key="v2.user_field").fill("lead@moonsanctum.com")
    healed_page.healed_locator("#userSecret", key="v2.pass_field").fill("securepass")

    # Script calls OLD locator (#loginBtn) bound to stable identity
    # Framework intercepts failure, scans, scores, and retries with new locator
    healed_page.healed_locator("#loginBtn", key="auth.login_submit").click()

    # Step 8 Verification: Successfully navigated to dashboard
    healed_page.wait_for_load_state("networkidle")
    assert "/dashboard" in healed_page.raw_page.url

    # -----------------------------------------------------------------
    # STEP 9: Audit Logging in SQLite
    # -----------------------------------------------------------------
    events = selfheal_repo.get_healing_events()
    matching_events = [e for e in events if e["target_key"] == "auth.login_submit"]
    assert len(matching_events) >= 1

    event = matching_events[0]
    assert event["decision"] == "APPROVED"
    assert event["status"] == "pending_review"  # Assisted mode policy
    assert event["retry_success"] == 1
    assert event["original_locator"] == "#loginBtn"
    assert event["healed_locator"] in ('[data-testid="auth-submit"]', '#signinBtn')
    assert event["similarity_score"] >= 0.80

    # -----------------------------------------------------------------
    # STEP 10: Dashboard Approval, Baseline Promotion & Locator History
    # -----------------------------------------------------------------
    # Simulate QA Engineer clicking "Approve & Promote" in Dashboard
    selfheal_repo.promote_healed_locator(
        target_key="auth.login_submit",
        new_locator=event["healed_locator"],
        similarity_score=event["similarity_score"],
        approved_by="qa_engineer_lead"
    )

    # Verify promoted baseline in repository (version incremented to 2)
    promoted_fp = selfheal_repo.get_active_fingerprint("auth.login_submit")
    assert promoted_fp is not None
    assert promoted_fp.version == 2
    assert promoted_fp.status == "active"
    assert promoted_fp.original_selector == event["healed_locator"]

    # Verify locator history log recorded
    history = selfheal_repo.get_locator_history("auth.login_submit")
    assert len(history) >= 1
    latest_hist = history[0]
    assert latest_hist["old_locator"] == "#loginBtn"
    assert latest_hist["new_locator"] == event["healed_locator"]
    assert latest_hist["approved_by"] == "qa_engineer_lead"
    assert latest_hist["change_type"] == "HEALED_PROMOTED"
