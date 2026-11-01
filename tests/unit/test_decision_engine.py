import pytest
from selfheal.config import Thresholds
from selfheal.intelligence.decision_engine import HealingDecisionEngine, DecisionStatus
from selfheal.intelligence.scoring import ScoredCandidate, ScoreBreakdown
from selfheal.scanner.dom_scanner import CandidateElement
from selfheal.baseline.fingerprint import BoundingBox


def create_dummy_candidate(text: str, element_id: str = "", testid: str = "") -> CandidateElement:
    attrs = {}
    if testid:
        attrs["data-testid"] = testid
    return CandidateElement(
        tag_name="button",
        element_id=element_id,
        inner_text=text,
        attributes=attrs,
        bounding_box=BoundingBox(x=10, y=10, width=100, height=30)
    )


def test_decision_rejects_low_score():
    engine = HealingDecisionEngine(Thresholds(minimum_score=0.85, minimum_score_margin=0.10))
    cand = create_dummy_candidate("Cancel", "cancelBtn")
    breakdown = ScoreBreakdown(
        text_score=0.5, type_and_role_score=1.0, attributes_score=0.5,
        parent_score=0.5, children_score=0.5, position_score=0.5,
        total_score=0.74
    )
    scored = [ScoredCandidate(candidate=cand, score_breakdown=breakdown)]

    decision = engine.evaluate("btn.test", "#oldBtn", scored)
    assert decision.decision == DecisionStatus.REJECTED_LOW_CONFIDENCE
    assert "below minimum threshold" in decision.reason


def test_decision_rejects_ambiguous_margin():
    engine = HealingDecisionEngine(Thresholds(minimum_score=0.85, minimum_score_margin=0.10))
    cand1 = create_dummy_candidate("Sign In", "signinBtn")
    cand2 = create_dummy_candidate("Register", "regBtn")

    # Margin is only 0.02 (0.91 vs 0.89) - should be rejected as ambiguous!
    bd1 = ScoreBreakdown(
        text_score=0.9, type_and_role_score=1.0, attributes_score=0.9,
        parent_score=0.9, children_score=0.9, position_score=0.9,
        total_score=0.91
    )
    bd2 = ScoreBreakdown(
        text_score=0.85, type_and_role_score=1.0, attributes_score=0.85,
        parent_score=0.85, children_score=0.85, position_score=0.85,
        total_score=0.89
    )

    scored = [
        ScoredCandidate(candidate=cand1, score_breakdown=bd1),
        ScoredCandidate(candidate=cand2, score_breakdown=bd2)
    ]

    decision = engine.evaluate("auth.btn", "#loginBtn", scored)
    assert decision.decision == DecisionStatus.REJECTED_AMBIGUOUS_MATCH
    assert "Ambiguous match" in decision.reason


def test_decision_approves_strong_match():
    engine = HealingDecisionEngine(Thresholds(minimum_score=0.85, minimum_score_margin=0.10))
    cand1 = create_dummy_candidate("Sign In", "signinBtn", testid="auth-submit")
    cand2 = create_dummy_candidate("Cancel", "cancelBtn")

    # Margin is 0.35 (0.92 vs 0.57)
    bd1 = ScoreBreakdown(
        text_score=0.9, type_and_role_score=1.0, attributes_score=0.95,
        parent_score=0.9, children_score=0.9, position_score=0.9,
        total_score=0.92
    )
    bd2 = ScoreBreakdown(
        text_score=0.4, type_and_role_score=1.0, attributes_score=0.4,
        parent_score=0.4, children_score=0.4, position_score=0.4,
        total_score=0.57
    )

    scored = [
        ScoredCandidate(candidate=cand1, score_breakdown=bd1),
        ScoredCandidate(candidate=cand2, score_breakdown=bd2)
    ]

    decision = engine.evaluate("auth.btn", "#loginBtn", scored)
    assert decision.decision == DecisionStatus.APPROVED
    assert decision.healed_locator in ('[data-testid="auth-submit"]', '#signinBtn')
