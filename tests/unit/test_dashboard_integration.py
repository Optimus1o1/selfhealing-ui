"""
Dashboard & Repository Integration Test Suite.
Moon Sanctum Labs -- Decode. Build. Evolve.

Verifies the database query helpers, metric calculations, filtering logic,
audit promotion, repair rejection, and empty/missing database edge cases
used by the SelfHeal Engineering Dashboard.
"""

import pytest
import sqlite3
from pathlib import Path
from selfheal.database.connection import DatabaseManager
from selfheal.baseline.repository import BaselineRepository
from selfheal.baseline.fingerprint import ElementFingerprint, BoundingBox
from selfheal.database.models import HealingEventModel


@pytest.fixture
def temp_db(tmp_path: Path) -> DatabaseManager:
    db_file = tmp_path / "test_dash.db"
    return DatabaseManager(db_file)


@pytest.fixture
def repo(temp_db: DatabaseManager) -> BaselineRepository:
    return BaselineRepository(temp_db)


def test_empty_database_handling(repo: BaselineRepository):
    """
    Ensures that an empty database returns clean empty structures without division by zero.
    """
    stats = repo.get_run_statistics()
    assert stats["total_runs"] == 0
    assert stats["total_steps"] is None or stats["total_steps"] == 0
    
    events = repo.get_healing_events()
    assert events == []
    
    runs = repo.get_test_runs()
    assert runs == []
    
    fps = repo.get_all_active_fingerprints()
    assert fps == []
    
    keys = repo.get_all_target_keys()
    assert keys == []
    
    stab = repo.get_locator_stability_stats()
    assert stab == []
    
    lats = repo.get_latency_percentiles()
    assert lats["count"] == 0
    assert lats["mean"] == 0.0
    assert lats["p50"] == 0.0


def test_invalid_or_missing_record_lookups(repo: BaselineRepository):
    """
    Ensures querying missing target keys or non-existent event IDs returns None safely.
    """
    assert repo.get_healing_event_by_id(999999) is None
    assert repo.get_fingerprint_versions("non.existent.key") == []
    assert repo.get_active_fingerprint("non.existent.key") is None
    assert repo.get_locator_history("non.existent.key") == []


def test_metric_calculations_and_filtering(repo: BaselineRepository):
    """
    Populates realistic run and healing data and verifies metric calculations and filtering.
    """
    # 1. Create 2 test runs
    run1 = repo.create_test_run(project_name="ECommerce V1", policy="assisted")
    repo.finish_test_run(run1, total_steps=10, passed=8, failed=0, healed=2, status="COMPLETED")

    run2 = repo.create_test_run(project_name="ECommerce V2", policy="automatic")
    repo.finish_test_run(run2, total_steps=5, passed=3, failed=1, healed=1, status="FAILED")

    # 2. Add element fingerprints
    fp1 = ElementFingerprint(
        target_key="auth.submit",
        tag_name="button",
        element_id="loginBtn",
        inner_text="Login",
        original_selector="#loginBtn"
    )
    repo.save_fingerprint(fp1)

    fp2 = ElementFingerprint(
        target_key="cart.checkout",
        tag_name="button",
        element_id="checkoutBtn",
        inner_text="Checkout",
        original_selector="#checkoutBtn"
    )
    repo.save_fingerprint(fp2)

    # 3. Add healing events
    ev1 = HealingEventModel(
        run_id=run1,
        target_key="auth.submit",
        original_locator="#loginBtn",
        healed_locator="#signinBtn",
        similarity_score=0.88,
        decision="APPROVED",
        reason="Score above 0.80",
        status="pending_review",
        retry_success=True,
        latency_ms=1200.0
    )
    repo.record_healing_event(ev1)

    ev2 = HealingEventModel(
        run_id=run1,
        target_key="auth.submit",
        original_locator="#loginBtn",
        healed_locator="#otherBtn",
        similarity_score=0.82,
        decision="REJECTED_AMBIGUOUS_MATCH",
        reason="Margin < 0.10",
        status="rejected",
        retry_success=False,
        latency_ms=1500.0
    )
    repo.record_healing_event(ev2)

    ev3 = HealingEventModel(
        run_id=run2,
        target_key="cart.checkout",
        original_locator="#checkoutBtn",
        healed_locator="#payBtn",
        similarity_score=0.91,
        decision="APPROVED",
        reason="Score above 0.80",
        status="pending_review",
        retry_success=True,
        latency_ms=2100.0
    )
    repo.record_healing_event(ev3)

    # Verify run statistics
    runs = repo.get_test_runs()
    assert len(runs) == 2
    assert sum(r["total_steps"] for r in runs) == 15
    assert sum(r["passed_count"] for r in runs) == 11
    assert sum(r["healed_count"] for r in runs) == 3

    # Verify filtering by run_id
    run1_events = repo.get_healing_events(run_id=run1)
    assert len(run1_events) == 2

    run2_events = repo.get_healing_events(run_id=run2)
    assert len(run2_events) == 1

    # Verify latency percentiles
    lats = repo.get_latency_percentiles()
    assert lats["count"] == 3
    assert lats["min"] == 1200.0
    assert lats["max"] == 2100.0
    assert lats["mean"] == round((1200 + 1500 + 2100) / 3, 2)

    # Verify target keys & stability index
    keys = repo.get_all_target_keys()
    assert "auth.submit" in keys
    assert "cart.checkout" in keys

    stab = repo.get_locator_stability_stats()
    assert len(stab) == 2
    auth_stab = next(s for s in stab if s["target_key"] == "auth.submit")
    assert auth_stab["times_intercepted"] == 2
    assert auth_stab["times_approved"] == 1
    assert auth_stab["times_rejected"] == 1


def test_baseline_promotion_and_rejection_workflow(repo: BaselineRepository):
    """
    Tests that approving and promoting a healed locator updates the baseline version,
    writes to locator_history, and marks the event as promoted. Also tests repair rejection.
    """
    # 1. Establish baseline v1
    base_fp = ElementFingerprint(
        target_key="user.register",
        tag_name="button",
        element_id="btnRegister",
        inner_text="Register",
        original_selector="#btnRegister"
    )
    repo.save_fingerprint(base_fp)

    active_v1 = repo.get_active_fingerprint("user.register")
    assert active_v1.version == 1
    assert active_v1.original_selector == "#btnRegister"

    # 2. Record healing event
    ev_id = repo.record_healing_event(HealingEventModel(
        target_key="user.register",
        original_locator="#btnRegister",
        healed_locator="#btnSignUpSubmit",
        similarity_score=0.89,
        decision="APPROVED",
        reason="Match approved",
        status="pending_review",
        retry_success=True,
        latency_ms=1340.0
    ))

    # 3. Promote to V2
    repo.promote_healed_locator(
        target_key="user.register",
        new_locator="#btnSignUpSubmit",
        similarity_score=0.89,
        approved_by="qa_automation_lead"
    )

    # Verify version 2 is now active
    active_v2 = repo.get_active_fingerprint("user.register")
    assert active_v2.version == 2
    assert active_v2.original_selector == "#btnSignUpSubmit"
    assert active_v2.status == "active"

    # Verify version history has both v1 (archived) and v2 (active)
    versions = repo.get_fingerprint_versions("user.register")
    assert len(versions) == 2
    assert versions[0].version == 1 and versions[0].status == "archived"
    assert versions[1].version == 2 and versions[1].status == "active"

    # Verify locator_history audit log
    history = repo.get_locator_history("user.register")
    assert len(history) == 1
    assert history[0]["old_locator"] == "#btnRegister"
    assert history[0]["new_locator"] == "#btnSignUpSubmit"
    assert history[0]["approved_by"] == "qa_automation_lead"

    # Verify healing event status was updated to promoted
    ev_updated = repo.get_healing_event_by_id(ev_id)
    assert ev_updated["status"] == "promoted"

    # 4. Test Rejecting an event
    ev_reject_id = repo.record_healing_event(HealingEventModel(
        target_key="user.register",
        original_locator="#btnSignUpSubmit",
        healed_locator="#btnRandomWrong",
        similarity_score=0.81,
        decision="APPROVED",
        status="pending_review"
    ))
    repo.reject_healing_event(ev_reject_id)
    ev_rejected = repo.get_healing_event_by_id(ev_reject_id)
    assert ev_rejected["status"] == "rejected"

