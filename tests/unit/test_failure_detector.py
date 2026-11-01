import pytest
from unittest.mock import MagicMock
from selfheal.detection.failure_detector import FailureClassifier, FailureType


def test_classify_assertion_error():
    classifier = FailureClassifier(grace_period_ms=0)
    page_mock = MagicMock()
    classification = classifier.classify_failure(page_mock, "#btn", AssertionError("Assertion failed"))
    assert classification.failure_type == FailureType.ASSERTION_FAILURE
    assert not classification.is_healable


def test_classify_invalid_syntax_error():
    classifier = FailureClassifier(grace_period_ms=0)
    page_mock = MagicMock()
    page_mock.locator.side_effect = Exception("is not a valid selector")
    classification = classifier.classify_failure(page_mock, "///invalid:::selector")
    assert classification.failure_type == FailureType.INVALID_SELECTOR
    assert not classification.is_healable


def test_classify_missing_locator():
    classifier = FailureClassifier(grace_period_ms=0)
    page_mock = MagicMock()
    locator_mock = MagicMock()
    locator_mock.count.return_value = 0
    page_mock.locator.return_value = locator_mock

    classification = classifier.classify_failure(page_mock, "#missingBtn")
    assert classification.failure_type == FailureType.LOCATOR_NOT_FOUND
    assert classification.is_healable


def test_classify_ambiguous_locator():
    classifier = FailureClassifier(grace_period_ms=0)
    page_mock = MagicMock()
    locator_mock = MagicMock()
    locator_mock.count.return_value = 3
    page_mock.locator.return_value = locator_mock

    classification = classifier.classify_failure(page_mock, ".duplicateBtn")
    assert classification.failure_type == FailureType.AMBIGUOUS_LOCATOR
    assert not classification.is_healable


def test_classify_hidden_element():
    classifier = FailureClassifier(grace_period_ms=0)
    page_mock = MagicMock()
    locator_mock = MagicMock()
    locator_mock.count.return_value = 1
    first_el = MagicMock()
    first_el.is_visible.return_value = False
    first_el.is_enabled.return_value = True
    locator_mock.first = first_el
    page_mock.locator.return_value = locator_mock

    classification = classifier.classify_failure(page_mock, "#hiddenBtn")
    assert classification.failure_type == FailureType.ELEMENT_HIDDEN
    assert not classification.is_healable


def test_classify_disabled_element():
    classifier = FailureClassifier(grace_period_ms=0)
    page_mock = MagicMock()
    locator_mock = MagicMock()
    locator_mock.count.return_value = 1
    first_el = MagicMock()
    first_el.is_visible.return_value = True
    first_el.is_enabled.return_value = False
    locator_mock.first = first_el
    page_mock.locator.return_value = locator_mock

    classification = classifier.classify_failure(page_mock, "#disabledBtn")
    assert classification.failure_type == FailureType.ELEMENT_DISABLED
    assert not classification.is_healable
