import pytest
from selfheal.intelligence.similarity import (
    compute_text_similarity,
    compute_type_and_role_similarity,
    compute_attributes_similarity,
    compute_parent_similarity,
    compute_children_similarity,
    compute_position_similarity,
)
from selfheal.baseline.fingerprint import ElementFingerprint, BoundingBox
from selfheal.scanner.dom_scanner import CandidateElement
from selfheal.config import SimilarityWeights
from selfheal.intelligence.scoring import SimilarityScorer


def test_text_similarity_exact_and_variants():
    # Exact match
    assert compute_text_similarity("Login", "Login") == 1.0

    # Semantic/rephrased variant: "Login" vs "Sign In"
    score_variant = compute_text_similarity("Login", "Sign In")
    assert 0.0 <= score_variant <= 1.0

    # Accessible name cross-match
    acc_score = compute_text_similarity("", "Submit", baseline_acc_name="Submit", candidate_acc_name="")
    assert acc_score == 1.0


def test_type_and_role_similarity():
    base = ElementFingerprint(target_key="btn", tag_name="button", aria_role="button", input_type="submit")
    cand = CandidateElement(tag_name="button", aria_role="button", input_type="submit")
    assert compute_type_and_role_similarity(base, cand) == 1.0

    # Button vs Input[type=submit]
    cand_input = CandidateElement(tag_name="input", input_type="submit")
    score = compute_type_and_role_similarity(base, cand_input)
    assert score > 0.4


def test_attributes_similarity():
    base_attrs = {"name": "submitBtn", "data-testid": "login-action", "type": "submit"}
    cand_attrs = {"name": "submitBtn", "data-testid": "login-action", "type": "submit"}
    assert compute_attributes_similarity(base_attrs, cand_attrs) == 1.0

    cand_modified = {"name": "submitBtn", "type": "submit"}
    score = compute_attributes_similarity(base_attrs, cand_modified)
    assert 0.5 < score < 1.0


def test_position_similarity():
    box1 = BoundingBox(x=100.0, y=200.0, width=120.0, height=40.0)
    box2 = BoundingBox(x=105.0, y=205.0, width=120.0, height=40.0)
    score = compute_position_similarity(box1, box2, viewport_diag=1920.0)
    assert score > 0.95


def test_weighted_scoring_aggregation():
    weights = SimilarityWeights(
        text=0.30,
        type_and_role=0.20,
        attributes=0.20,
        parent_context=0.15,
        children_structure=0.10,
        position=0.05
    )
    scorer = SimilarityScorer(weights)

    base = ElementFingerprint(
        target_key="login.submit",
        tag_name="button",
        inner_text="Login",
        aria_role="button",
        input_type="submit",
        attributes={"name": "login", "data-testid": "auth-submit"},
        parent_tag="form",
        parent_id="loginForm",
        bounding_box=BoundingBox(x=200, y=400, width=100, height=40)
    )

    cand = CandidateElement(
        tag_name="button",
        inner_text="Login",
        aria_role="button",
        input_type="submit",
        attributes={"name": "login", "data-testid": "auth-submit"},
        parent_tag="form",
        parent_id="loginForm",
        bounding_box=BoundingBox(x=200, y=400, width=100, height=40)
    )

    scored = scorer.score_candidate(base, cand)
    assert scored.total_score >= 0.95
