from enum import Enum
import time
from typing import Optional, TYPE_CHECKING
from pydantic import BaseModel

if TYPE_CHECKING:
    from playwright.sync_api import Page


class FailureType(str, Enum):
    LOCATOR_NOT_FOUND = "LOCATOR_NOT_FOUND"        # Element missing: ELIGIBLE FOR HEALING
    ELEMENT_HIDDEN = "ELEMENT_HIDDEN"              # Element in DOM but hidden: DO NOT HEAL
    ELEMENT_DISABLED = "ELEMENT_DISABLED"          # Element in DOM but disabled: DO NOT HEAL
    AMBIGUOUS_LOCATOR = "AMBIGUOUS_LOCATOR"        # Multiple elements match: DO NOT HEAL
    INVALID_SELECTOR = "INVALID_SELECTOR"          # Malformed CSS/XPath: DO NOT HEAL
    NETWORK_OR_NAV_ERROR = "NETWORK_OR_NAV"        # Page or network crash: DO NOT HEAL
    ASSERTION_FAILURE = "ASSERTION_FAILURE"        # Assertion mismatch: DO NOT HEAL
    UNKNOWN_ERROR = "UNKNOWN_ERROR"                # Fallback: DO NOT HEAL


class FailureClassification(BaseModel):
    failure_type: FailureType
    is_healable: bool
    reason: str
    element_count: int = 0


class FailureClassifier:
    def __init__(self, grace_period_ms: int = 500):
        self.grace_period_ms = grace_period_ms

    def classify_failure(
        self,
        page: "Page",
        selector: str,
        original_exception: Optional[Exception] = None
    ) -> FailureClassification:
        """
        Distinguishes between genuine actionability defects (hidden, disabled, ambiguous)
        and true locator disappearance (eligible for healing).
        """
        # 1. Check for selector syntax error or assertion error
        if original_exception is not None:
            ex_str = str(original_exception).lower()
            ex_name = original_exception.__class__.__name__

            if "assertionerror" in ex_name.lower():
                return FailureClassification(
                    failure_type=FailureType.ASSERTION_FAILURE,
                    is_healable=False,
                    reason="Test assertion failure; not a locator issue."
                )

            if "is not a valid selector" in ex_str or "syntaxerror" in ex_str:
                return FailureClassification(
                    failure_type=FailureType.INVALID_SELECTOR,
                    is_healable=False,
                    reason="The selector has invalid syntax."
                )

            if "navigation failed" in ex_str or "net::" in ex_str or "target closed" in ex_str:
                return FailureClassification(
                    failure_type=FailureType.NETWORK_OR_NAV_ERROR,
                    is_healable=False,
                    reason="Network or navigation failure."
                )

        # 2. Check DOM presence using Playwright locator count
        try:
            loc = page.locator(selector)
            count = loc.count()
        except Exception as e:
            return FailureClassification(
                failure_type=FailureType.INVALID_SELECTOR,
                is_healable=False,
                reason=f"Failed to query selector: {e}"
            )

        # If zero elements match, wait grace period for dynamic AJAX/SPA hydration
        if count == 0 and self.grace_period_ms > 0:
            time.sleep(self.grace_period_ms / 1000.0)
            try:
                count = loc.count()
            except Exception:
                count = 0

        # Element truly missing -> Eligible for healing!
        if count == 0:
            return FailureClassification(
                failure_type=FailureType.LOCATOR_NOT_FOUND,
                is_healable=True,
                reason="Original locator matches zero elements in the current DOM.",
                element_count=0
            )

        # Multiple elements match -> Ambiguous
        if count > 1:
            return FailureClassification(
                failure_type=FailureType.AMBIGUOUS_LOCATOR,
                is_healable=False,
                reason=f"Original locator matches {count} elements (ambiguous).",
                element_count=count
            )

        # Exactly 1 element matches -> Check actionability
        try:
            first = loc.first
            if not first.is_visible():
                return FailureClassification(
                    failure_type=FailureType.ELEMENT_HIDDEN,
                    is_healable=False,
                    reason="Element exists in DOM but is currently hidden.",
                    element_count=1
                )
            if not first.is_enabled():
                return FailureClassification(
                    failure_type=FailureType.ELEMENT_DISABLED,
                    is_healable=False,
                    reason="Element exists in DOM but is currently disabled.",
                    element_count=1
                )
        except Exception as e:
            # Actionability probe error
            pass

        return FailureClassification(
            failure_type=FailureType.UNKNOWN_ERROR,
            is_healable=False,
            reason="Element exists and appears actionable; failure may be transient or event-driven.",
            element_count=count
        )

