from enum import Enum
from typing import Optional
from pydantic import BaseModel
from selfheal.config import Thresholds
from selfheal.baseline.fingerprint import ElementFingerprint
from selfheal.intelligence.scoring import ScoredCandidate, ScoreBreakdown


class DecisionStatus(str, Enum):
    APPROVED = "APPROVED"
    REJECTED_LOW_CONFIDENCE = "REJECTED_LOW_CONFIDENCE"
    REJECTED_AMBIGUOUS_MATCH = "REJECTED_AMBIGUOUS_MATCH"
    REJECTED_NO_CANDIDATES = "REJECTED_NO_CANDIDATES"


class HealingDecision(BaseModel):
    decision: DecisionStatus
    target_key: str
    original_locator: str
    healed_locator: Optional[str] = None
    similarity_score: Optional[float] = None
    reason: str
    score_breakdown: Optional[ScoreBreakdown] = None
    top_candidate: Optional[ScoredCandidate] = None


class HealingDecisionEngine:
    def __init__(self, thresholds: Thresholds):
        self.thresholds = thresholds

    def evaluate(
        self,
        target_key: str,
        original_locator: str,
        ranked_candidates: list[ScoredCandidate]
    ) -> HealingDecision:
        if not ranked_candidates:
            return HealingDecision(
                decision=DecisionStatus.REJECTED_NO_CANDIDATES,
                target_key=target_key,
                original_locator=original_locator,
                reason="No candidate elements discovered on current page DOM."
            )

        top = ranked_candidates[0]

        # 1. Minimum similarity score threshold
        if top.total_score < self.thresholds.minimum_score:
            return HealingDecision(
                decision=DecisionStatus.REJECTED_LOW_CONFIDENCE,
                target_key=target_key,
                original_locator=original_locator,
                similarity_score=top.total_score,
                reason=f"Top candidate score ({top.total_score:.4f}) is below minimum threshold ({self.thresholds.minimum_score:.2f}).",
                score_breakdown=top.score_breakdown,
                top_candidate=top
            )

        # 2. Minimum margin between top candidate and runner-up
        if len(ranked_candidates) > 1:
            runner_up = ranked_candidates[1]
            margin = top.total_score - runner_up.total_score
            if margin < self.thresholds.minimum_score_margin:
                return HealingDecision(
                    decision=DecisionStatus.REJECTED_AMBIGUOUS_MATCH,
                    target_key=target_key,
                    original_locator=original_locator,
                    similarity_score=top.total_score,
                    reason=(
                        f"Ambiguous match: margin between top candidate ({top.total_score:.4f}) and "
                        f"runner-up ({runner_up.total_score:.4f}) is {margin:.4f}, below required margin ({self.thresholds.minimum_score_margin:.2f})."
                    ),
                    score_breakdown=top.score_breakdown,
                    top_candidate=top
                )

        # 3. Choose robust healed selector
        healed_selector = self.synthesize_locator(top)

        return HealingDecision(
            decision=DecisionStatus.APPROVED,
            target_key=target_key,
            original_locator=original_locator,
            healed_locator=healed_selector,
            similarity_score=top.total_score,
            reason=f"Strong match ({top.total_score:.4f}) exceeding threshold and confidence margin.",
            score_breakdown=top.score_breakdown,
            top_candidate=top
        )

    def synthesize_locator(self, candidate: ScoredCandidate) -> str:
        cand = candidate.candidate
        # 1. Prefer generated_selector from DOM extractor if available
        if cand.generated_selector:
            return cand.generated_selector

        # 2. data-testid
        if "data-testid" in cand.attributes:
            return f'[data-testid="{cand.attributes["data-testid"]}"]'

        # 3. Clean ID
        if cand.element_id:
            return f"#{cand.element_id}"

        # 4. Text-based locator
        if cand.inner_text and cand.tag_name in ("button", "a"):
            text_escaped = cand.inner_text.replace('"', '\\"')
            return f'{cand.tag_name}:has-text("{text_escaped}")'

        # 5. Fallback to tag + class
        if cand.class_list:
            return f"{cand.tag_name}.{cand.class_list[0]}"

        return cand.tag_name
