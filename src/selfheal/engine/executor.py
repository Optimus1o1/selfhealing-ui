import time
import json
from typing import Any, Callable, Optional, TYPE_CHECKING
from selfheal.config import SelfHealConfig, HealingPolicy
from selfheal.baseline.fingerprint import ElementFingerprint, BoundingBox
from selfheal.baseline.repository import BaselineRepository
from selfheal.detection.failure_detector import FailureClassifier, FailureType
from selfheal.detection.exceptions import (
    BaselineNotFoundError,
    UnhealableFailureError,
    HealingConfidenceError,
    HealingExecutionError,
)
from selfheal.scanner.dom_scanner import DOMScanner
from selfheal.intelligence.scoring import SimilarityScorer
from selfheal.intelligence.decision_engine import HealingDecisionEngine, DecisionStatus
from selfheal.database.models import HealingEventModel

if TYPE_CHECKING:
    from playwright.sync_api import Page, Locator


class ExecutionManager:
    def __init__(
        self,
        config: SelfHealConfig,
        repository: BaselineRepository,
        run_id: Optional[int] = None
    ):
        self.config = config
        self.repo = repository
        self.run_id = run_id
        self.classifier = FailureClassifier(grace_period_ms=config.framework.grace_period_ms)
        self.scanner = DOMScanner()
        self.scorer = SimilarityScorer(weights=config.weights)
        self.decision_engine = HealingDecisionEngine(thresholds=config.thresholds)

    def execute_action(
        self,
        page: "Page",
        original_selector: str,
        target_key: str,
        action_name: str,
        action_fn: Callable[["Locator"], Any],
        record_baseline_if_missing: bool = True,
        **action_kwargs: Any
    ) -> Any:
        """
        Executes an action safely on a locator.
        If the locator fails, intercepts and attempts deterministic self-healing.
        """
        start_time = time.perf_counter()
        loc = page.locator(original_selector)

        # Snapshot baseline BEFORE interaction in case interaction triggers navigation or unloads DOM
        pre_captured_fp = None
        if record_baseline_if_missing and not self.repo.get_active_fingerprint(target_key):
            pre_captured_fp = self._capture_baseline_snapshot(page, original_selector, target_key)

        # Set default timeout for action to fail fast (e.g. 2500ms) rather than waiting 30s
        action_kwargs.setdefault("timeout", 2500)

        # 1. First, attempt standard execution
        try:
            result = action_fn(loc, **action_kwargs)

            # If interaction succeeded, commit the pre-captured baseline fingerprint
            if pre_captured_fp is not None:
                self.repo.save_fingerprint(pre_captured_fp)

            return result
        except Exception as original_exc:
            pass  # Fall through to failure classification and healing

        # 2. Failure Classification
        classification = self.classifier.classify_failure(page, original_selector)
        if not classification.is_healable:
            # Actionability failure (hidden/disabled/ambiguous) or assertion failure
            self._log_rejected_event(
                target_key=target_key,
                original_locator=original_selector,
                decision="REJECTED_ACTIONABILITY",
                reason=classification.reason,
                latency_ms=(time.perf_counter() - start_time) * 1000
            )
            raise UnhealableFailureError(
                f"Action '{action_name}' failed on '{original_selector}' (key='{target_key}'). "
                f"Classification: {classification.failure_type.value}. Reason: {classification.reason}"
            )

        # 3. Retrieve Baseline Fingerprint
        baseline_fp = self.repo.get_active_fingerprint(target_key)
        if not baseline_fp:
            self._log_rejected_event(
                target_key=target_key,
                original_locator=original_selector,
                decision="REJECTED_NO_BASELINE",
                reason=f"No baseline fingerprint found for target_key '{target_key}'.",
                latency_ms=(time.perf_counter() - start_time) * 1000
            )
            raise BaselineNotFoundError(
                f"Locator '{original_selector}' failed, and no baseline fingerprint exists for target key '{target_key}'."
            )

        # 4. Scan Current DOM for Candidate Elements
        candidates = self.scanner.scan(page, max_candidates=self.config.thresholds.max_candidates)

        # 5. Score Candidates
        ranked = self.scorer.rank_candidates(baseline_fp, candidates)

        # 6. Evaluate Decision
        decision = self.decision_engine.evaluate(
            target_key=target_key,
            original_locator=original_selector,
            ranked_candidates=ranked
        )

        healing_latency = (time.perf_counter() - start_time) * 1000

        # If decision is rejected
        if decision.decision != DecisionStatus.APPROVED or not decision.healed_locator:
            self._log_rejected_event(
                target_key=target_key,
                original_locator=original_selector,
                decision=decision.decision.value,
                reason=decision.reason,
                latency_ms=healing_latency,
                similarity_score=decision.similarity_score,
                score_breakdown=decision.score_breakdown
            )
            raise HealingConfidenceError(
                f"Healing rejected for '{target_key}' ({original_selector}): {decision.reason}"
            )

        # Policy: In OBSERVE mode, log repair but do not retry
        if self.config.framework.policy == HealingPolicy.OBSERVE:
            self._log_healed_event(
                target_key=target_key,
                original_locator=original_selector,
                healed_locator=decision.healed_locator,
                similarity_score=decision.similarity_score or 0.0,
                score_breakdown=decision.score_breakdown,
                retry_success=False,
                status="observed",
                reason=decision.reason,
                latency_ms=healing_latency
            )
            raise HealingExecutionError(
                f"Policy is OBSERVE: potential healed locator identified as '{decision.healed_locator}' "
                f"with score {decision.similarity_score:.4f}, but execution retry is disabled."
            )

        # 7. Safe Retry Once with Healed Locator
        try:
            healed_loc = page.locator(decision.healed_locator)
            retry_result = action_fn(healed_loc, **action_kwargs)

            # Execution succeeded!
            status = "promoted" if self.config.framework.policy == HealingPolicy.AUTOMATIC else "pending_review"

            self._log_healed_event(
                target_key=target_key,
                original_locator=original_selector,
                healed_locator=decision.healed_locator,
                similarity_score=decision.similarity_score or 0.0,
                score_breakdown=decision.score_breakdown,
                retry_success=True,
                status=status,
                reason=decision.reason,
                latency_ms=healing_latency
            )

            # If policy is AUTOMATIC, promote new locator in baseline repository
            if self.config.framework.policy == HealingPolicy.AUTOMATIC:
                self.repo.promote_healed_locator(
                    target_key=target_key,
                    new_locator=decision.healed_locator,
                    similarity_score=decision.similarity_score or 0.0,
                    approved_by="auto_policy"
                )

            return retry_result
        except Exception as retry_err:
            self._log_healed_event(
                target_key=target_key,
                original_locator=original_selector,
                healed_locator=decision.healed_locator,
                similarity_score=decision.similarity_score or 0.0,
                score_breakdown=decision.score_breakdown,
                retry_success=False,
                status="retry_failed",
                reason=f"Retry failed with error: {retry_err}",
                latency_ms=healing_latency
            )
            raise HealingExecutionError(
                f"Healed locator '{decision.healed_locator}' was identified for '{target_key}' "
                f"but action '{action_name}' failed upon retry: {retry_err}"
            )

    def _capture_baseline_snapshot(self, page: "Page", selector: str, target_key: str) -> Optional[ElementFingerprint]:
        """Captures a baseline element fingerprint before an action is executed."""
        try:
            loc = page.locator(selector).first
            if not loc.is_visible():
                return None

            candidates = self.scanner.scan(page, max_candidates=100)
            matched_candidate = None

            # 1. Match by clean ID
            clean_id = selector.lstrip("#") if selector.startswith("#") else ""
            if clean_id:
                for c in candidates:
                    if c.element_id == clean_id:
                        matched_candidate = c
                        break

            # 2. Match by bounding box
            if not matched_candidate:
                bbox = loc.bounding_box()
                if bbox:
                    for c in candidates:
                        if (
                            abs(c.bounding_box.x - bbox["x"]) < 5 and
                            abs(c.bounding_box.y - bbox["y"]) < 5
                        ):
                            matched_candidate = c
                            break

            # 3. Match by name or text
            if not matched_candidate and candidates:
                for c in candidates:
                    if c.attributes.get("name") and f'[name="{c.attributes.get("name")}"]' in selector:
                        matched_candidate = c
                        break

            if matched_candidate:
                return ElementFingerprint(
                    target_key=target_key,
                    version=1,
                    status="active",
                    tag_name=matched_candidate.tag_name,
                    element_id=matched_candidate.element_id,
                    class_list=matched_candidate.class_list,
                    inner_text=matched_candidate.inner_text,
                    aria_role=matched_candidate.aria_role,
                    accessible_name=matched_candidate.accessible_name,
                    input_type=matched_candidate.input_type,
                    attributes=matched_candidate.attributes,
                    parent_tag=matched_candidate.parent_tag,
                    parent_id=matched_candidate.parent_id,
                    parent_classes=matched_candidate.parent_classes,
                    children_count=matched_candidate.children_count,
                    children_tags=matched_candidate.children_tags,
                    bounding_box=matched_candidate.bounding_box,
                    page_url=page.url,
                    original_selector=selector,
                )
        except Exception:
            pass
        return None

    def _log_rejected_event(
        self,
        target_key: str,
        original_locator: str,
        decision: str,
        reason: str,
        latency_ms: float,
        similarity_score: Optional[float] = None,
        score_breakdown: Any = None
    ) -> None:
        breakdown_json = score_breakdown.model_dump_json() if score_breakdown else None
        event = HealingEventModel(
            run_id=self.run_id,
            target_key=target_key,
            original_locator=original_locator,
            healed_locator=None,
            similarity_score=similarity_score,
            score_breakdown_json=breakdown_json,
            decision=decision,
            reason=reason,
            status="rejected",
            retry_success=False,
            latency_ms=round(latency_ms, 2)
        )
        self.repo.record_healing_event(event)

    def _log_healed_event(
        self,
        target_key: str,
        original_locator: str,
        healed_locator: str,
        similarity_score: float,
        score_breakdown: Any,
        retry_success: bool,
        status: str,
        reason: str,
        latency_ms: float
    ) -> None:
        breakdown_json = score_breakdown.model_dump_json() if score_breakdown else None
        event = HealingEventModel(
            run_id=self.run_id,
            target_key=target_key,
            original_locator=original_locator,
            healed_locator=healed_locator,
            similarity_score=similarity_score,
            score_breakdown_json=breakdown_json,
            decision="APPROVED",
            reason=reason,
            status=status,
            retry_success=retry_success,
            latency_ms=round(latency_ms, 2)
        )
        self.repo.record_healing_event(event)
