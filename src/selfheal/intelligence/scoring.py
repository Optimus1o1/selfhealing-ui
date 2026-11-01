from typing import Any
from pydantic import BaseModel
from selfheal.config import SimilarityWeights
from selfheal.baseline.fingerprint import ElementFingerprint
from selfheal.scanner.dom_scanner import CandidateElement
from selfheal.intelligence.similarity import (
    compute_text_similarity,
    compute_type_and_role_similarity,
    compute_attributes_similarity,
    compute_parent_similarity,
    compute_children_similarity,
    compute_position_similarity,
)


class ScoreBreakdown(BaseModel):
    text_score: float
    type_and_role_score: float
    attributes_score: float
    parent_score: float
    children_score: float
    position_score: float
    total_score: float


class ScoredCandidate(BaseModel):
    candidate: CandidateElement
    score_breakdown: ScoreBreakdown

    @property
    def total_score(self) -> float:
        return self.score_breakdown.total_score


class SimilarityScorer:
    def __init__(self, weights: SimilarityWeights):
        self.weights = weights.normalized_weights()

    def score_candidate(self, base: ElementFingerprint, cand: CandidateElement) -> ScoredCandidate:
        text_s = compute_text_similarity(base.inner_text, cand.inner_text, base.accessible_name, cand.accessible_name)
        type_s = compute_type_and_role_similarity(base, cand)
        attr_s = compute_attributes_similarity(base.attributes, cand.attributes)
        parent_s = compute_parent_similarity(base, cand)
        child_s = compute_children_similarity(base, cand)
        pos_s = compute_position_similarity(base.bounding_box, cand.bounding_box)

        total = (
            text_s * self.weights["text"] +
            type_s * self.weights["type_and_role"] +
            attr_s * self.weights["attributes"] +
            parent_s * self.weights["parent_context"] +
            child_s * self.weights["children_structure"] +
            pos_s * self.weights["position"]
        )

        breakdown = ScoreBreakdown(
            text_score=round(text_s, 4),
            type_and_role_score=round(type_s, 4),
            attributes_score=round(attr_s, 4),
            parent_score=round(parent_s, 4),
            children_score=round(child_s, 4),
            position_score=round(pos_s, 4),
            total_score=round(total, 4),
        )

        return ScoredCandidate(candidate=cand, score_breakdown=breakdown)

    def rank_candidates(self, base: ElementFingerprint, candidates: list[CandidateElement]) -> list[ScoredCandidate]:
        scored = [self.score_candidate(base, c) for c in candidates]
        scored.sort(key=lambda sc: sc.total_score, reverse=True)
        return scored
