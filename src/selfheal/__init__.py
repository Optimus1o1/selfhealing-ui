"""
Self-Healing UI Automation Framework for Playwright.
Deterministic locator recovery using historical DOM fingerprints,
failure classification, and weighted similarity analysis.
"""

from selfheal.engine.page import SelfHealingPage
from selfheal.engine.locator import SelfHealingLocator
from selfheal.config import SelfHealConfig

__version__ = "1.0.0"
__all__ = ["SelfHealingPage", "SelfHealingLocator", "SelfHealConfig"]

