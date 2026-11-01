class SelfHealException(Exception):
    """Base exception for all selfheal framework errors."""
    pass


class BaselineNotFoundError(SelfHealException):
    """Raised when no baseline fingerprint is recorded for the given target key."""
    pass


class UnhealableFailureError(SelfHealException):
    """Raised when a failure is not eligible for healing (e.g., hidden/disabled element, assertion)."""
    pass


class HealingConfidenceError(SelfHealException):
    """Raised when candidate similarity is below threshold or margin is ambiguous."""
    pass


class HealingExecutionError(SelfHealException):
    """Raised when retrying the healed locator fails."""
    pass

