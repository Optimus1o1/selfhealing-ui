import pytest
from unittest.mock import MagicMock
from selfheal.engine.locator import SelfHealingLocator
from selfheal.engine.executor import ExecutionManager
from selfheal.detection.exceptions import HealingExecutionError, UnhealableFailureError
from selfheal.config import SelfHealConfig
from selfheal.intelligence.decision_engine import HealingDecision, DecisionStatus


def test_locator_chaining_first_last_nth():
    page_mock = MagicMock()
    executor_mock = MagicMock()
    raw_loc = MagicMock()

    sh_loc = SelfHealingLocator(
        page=page_mock,
        selector="button.btn",
        target_key="form.buttons",
        executor=executor_mock,
        playwright_locator=raw_loc
    )

    first_loc = sh_loc.first
    assert isinstance(first_loc, SelfHealingLocator)
    assert first_loc.target_key == "form.buttons.first"
    assert "nth=0" in first_loc.selector

    last_loc = sh_loc.last
    assert isinstance(last_loc, SelfHealingLocator)
    assert last_loc.target_key == "form.buttons.last"
    assert "nth=-1" in last_loc.selector

    nth_loc = sh_loc.nth(3)
    assert isinstance(nth_loc, SelfHealingLocator)
    assert nth_loc.target_key == "form.buttons[3]"
    assert "nth=3" in nth_loc.selector


def test_execute_action_rejects_ambiguous_healed_retry():
    page_mock = MagicMock()
    repo_mock = MagicMock()
    config = SelfHealConfig()
    executor = ExecutionManager(config=config, repository=repo_mock)

    # Mock classification to be healable
    executor.classifier.classify_failure = MagicMock()
    executor.classifier.classify_failure.return_value.is_healable = True

    # Mock baseline
    repo_mock.get_active_fingerprint.return_value = MagicMock()

    # Mock scanner and scorer
    executor.scanner.scan = MagicMock(return_value=[MagicMock()])
    executor.scorer.rank_candidates = MagicMock(return_value=[MagicMock()])

    # Mock decision approved
    executor.decision_engine.evaluate = MagicMock(return_value=HealingDecision(
        decision=DecisionStatus.APPROVED,
        target_key="test.key",
        original_locator="#oldBtn",
        healed_locator=".ambiguous-healed-btn",
        similarity_score=0.92,
        reason="Good match"
    ))

    # Mock live page resolving to 0 elements for old locator, 2 elements for healed locator
    old_loc_mock = MagicMock()
    old_loc_mock.count.return_value = 0
    healed_loc_mock = MagicMock()
    healed_loc_mock.count.return_value = 2

    page_mock.locator.side_effect = lambda sel: old_loc_mock if sel == "#oldBtn" else healed_loc_mock

    def failing_action_fn(loc, **kw):
        if loc == old_loc_mock:
            raise Exception("Element not found")
        return "ok"

    # The executor must reject the retry because healed count is 2 (not unique)!
    with pytest.raises(HealingExecutionError) as exc_info:
        executor.execute_action(
            page=page_mock,
            original_selector="#oldBtn",
            target_key="test.key",
            action_name="click",
            action_fn=failing_action_fn,
            record_baseline_if_missing=False
        )

    assert "resolved to 2 elements" in str(exc_info.value)
