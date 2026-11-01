from typing import Any, Optional, TYPE_CHECKING
from selfheal.engine.executor import ExecutionManager

if TYPE_CHECKING:
    from playwright.sync_api import Locator, Page


class SelfHealingLocator:
    """
    Composition wrapper around Playwright's Locator.
    Intercepts user interactions (click, fill, hover, check, etc.) and routes
    failed operations to the deterministic ExecutionManager.
    """

    def __init__(
        self,
        page: "Page",
        selector: str,
        target_key: str,
        executor: ExecutionManager,
        playwright_locator: Optional["Locator"] = None
    ):
        self._page = page
        self._selector = selector
        self._target_key = target_key
        self._executor = executor
        self._locator = playwright_locator or page.locator(selector)

    @property
    def target_key(self) -> str:
        return self._target_key

    @property
    def selector(self) -> str:
        return self._selector

    def click(self, **kwargs: Any) -> Any:
        return self._executor.execute_action(
            page=self._page,
            original_selector=self._selector,
            target_key=self._target_key,
            action_name="click",
            action_fn=lambda loc, **kw: loc.click(**kw),
            **kwargs
        )

    def dblclick(self, **kwargs: Any) -> Any:
        return self._executor.execute_action(
            page=self._page,
            original_selector=self._selector,
            target_key=self._target_key,
            action_name="dblclick",
            action_fn=lambda loc, **kw: loc.dblclick(**kw),
            **kwargs
        )

    def fill(self, value: str, **kwargs: Any) -> Any:
        return self._executor.execute_action(
            page=self._page,
            original_selector=self._selector,
            target_key=self._target_key,
            action_name="fill",
            action_fn=lambda loc, **kw: loc.fill(value, **kw),
            **kwargs
        )

    def clear(self, **kwargs: Any) -> Any:
        return self._executor.execute_action(
            page=self._page,
            original_selector=self._selector,
            target_key=self._target_key,
            action_name="clear",
            action_fn=lambda loc, **kw: loc.clear(**kw),
            **kwargs
        )

    def check(self, **kwargs: Any) -> Any:
        return self._executor.execute_action(
            page=self._page,
            original_selector=self._selector,
            target_key=self._target_key,
            action_name="check",
            action_fn=lambda loc, **kw: loc.check(**kw),
            **kwargs
        )

    def uncheck(self, **kwargs: Any) -> Any:
        return self._executor.execute_action(
            page=self._page,
            original_selector=self._selector,
            target_key=self._target_key,
            action_name="uncheck",
            action_fn=lambda loc, **kw: loc.uncheck(**kw),
            **kwargs
        )

    def hover(self, **kwargs: Any) -> Any:
        return self._executor.execute_action(
            page=self._page,
            original_selector=self._selector,
            target_key=self._target_key,
            action_name="hover",
            action_fn=lambda loc, **kw: loc.hover(**kw),
            **kwargs
        )

    def select_option(self, *args: Any, **kwargs: Any) -> Any:
        return self._executor.execute_action(
            page=self._page,
            original_selector=self._selector,
            target_key=self._target_key,
            action_name="select_option",
            action_fn=lambda loc, **kw: loc.select_option(*args, **kw),
            **kwargs
        )

    def press(self, key: str, **kwargs: Any) -> Any:
        return self._executor.execute_action(
            page=self._page,
            original_selector=self._selector,
            target_key=self._target_key,
            action_name="press",
            action_fn=lambda loc, **kw: loc.press(key, **kw),
            **kwargs
        )

    def inner_text(self, **kwargs: Any) -> str:
        return self._locator.inner_text(**kwargs)

    def text_content(self, **kwargs: Any) -> Optional[str]:
        return self._locator.text_content(**kwargs)

    def is_visible(self, **kwargs: Any) -> bool:
        return self._locator.is_visible(**kwargs)

    def is_enabled(self, **kwargs: Any) -> bool:
        return self._locator.is_enabled(**kwargs)

    def count(self) -> int:
        return self._locator.count()

    def bounding_box(self, **kwargs: Any) -> Any:
        return self._locator.bounding_box(**kwargs)

    def __getattr__(self, name: str) -> Any:
        """Forward any other Playwright locator methods to underlying locator."""
        return getattr(self._locator, name)
