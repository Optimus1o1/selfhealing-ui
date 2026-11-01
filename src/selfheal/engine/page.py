from typing import Any, Optional, Union
from playwright.sync_api import Page, Locator
from selfheal.config import SelfHealConfig
from selfheal.database.connection import DatabaseManager
from selfheal.baseline.repository import BaselineRepository
from selfheal.engine.executor import ExecutionManager
from selfheal.engine.locator import SelfHealingLocator


class SelfHealingPage:
    """
    Composition wrapper around Playwright's Page object.
    Provides self-healing locators and intercepts interaction failures.
    """

    def __init__(
        self,
        page: Page,
        config: Optional[SelfHealConfig] = None,
        db_manager: Optional[DatabaseManager] = None,
        run_id: Optional[int] = None
    ):
        self._page = page
        self._config = config or SelfHealConfig()
        self._db_manager = db_manager or DatabaseManager(self._config.framework.database_path)
        self._repo = BaselineRepository(self._db_manager)
        self._run_id = run_id
        self._executor = ExecutionManager(
            config=self._config,
            repository=self._repo,
            run_id=self._run_id
        )

    @property
    def raw_page(self) -> Page:
        return self._page

    @property
    def repository(self) -> BaselineRepository:
        return self._repo

    @property
    def executor(self) -> ExecutionManager:
        return self._executor

    def healed_locator(self, selector: str, key: Optional[str] = None) -> SelfHealingLocator:
        """
        Creates a SelfHealingLocator bound to a stable target_key.
        If key is not provided, defaults to the selector itself.
        """
        target_key = key or selector
        return SelfHealingLocator(
            page=self._page,
            selector=selector,
            target_key=target_key,
            executor=self._executor
        )

    def bind(self, locator_or_selector: Union[str, Locator, SelfHealingLocator], key: str) -> SelfHealingLocator:
        """
        Binds any selector or Playwright Locator to an explicit stable target key.
        Example:
            button = page.locator("#loginBtn")
            page.bind(button, key="login.submit_button").click()
        """
        if isinstance(locator_or_selector, SelfHealingLocator):
            return SelfHealingLocator(
                page=self._page,
                selector=locator_or_selector.selector,
                target_key=key,
                executor=self._executor,
                playwright_locator=locator_or_selector._locator
            )
        elif isinstance(locator_or_selector, str):
            return SelfHealingLocator(
                page=self._page,
                selector=locator_or_selector,
                target_key=key,
                executor=self._executor
            )
        else:
            # Playwright Locator instance - extract string representation if possible
            selector_str = str(locator_or_selector)
            return SelfHealingLocator(
                page=self._page,
                selector=selector_str,
                target_key=key,
                executor=self._executor,
                playwright_locator=locator_or_selector
            )

    def locator(self, selector: str, key: Optional[str] = None, **kwargs: Any) -> SelfHealingLocator:
        """Drop-in replacement for page.locator returning a SelfHealingLocator."""
        target_key = key or selector
        raw_loc = self._page.locator(selector, **kwargs)
        return SelfHealingLocator(
            page=self._page,
            selector=selector,
            target_key=target_key,
            executor=self._executor,
            playwright_locator=raw_loc
        )

    # Convenience shortcuts that route through self-healing
    def click(self, selector: str, key: Optional[str] = None, **kwargs: Any) -> Any:
        return self.healed_locator(selector, key=key).click(**kwargs)

    def fill(self, selector: str, value: str, key: Optional[str] = None, **kwargs: Any) -> Any:
        return self.healed_locator(selector, key=key).fill(value, **kwargs)

    def hover(self, selector: str, key: Optional[str] = None, **kwargs: Any) -> Any:
        return self.healed_locator(selector, key=key).hover(**kwargs)

    def check(self, selector: str, key: Optional[str] = None, **kwargs: Any) -> Any:
        return self.healed_locator(selector, key=key).check(**kwargs)

    def uncheck(self, selector: str, key: Optional[str] = None, **kwargs: Any) -> Any:
        return self.healed_locator(selector, key=key).uncheck(**kwargs)

    # Standard Page delegations
    def goto(self, url: str, **kwargs: Any) -> Any:
        return self._page.goto(url, **kwargs)

    def wait_for_selector(self, selector: str, **kwargs: Any) -> Any:
        return self._page.wait_for_selector(selector, **kwargs)

    def wait_for_load_state(self, state: Optional[str] = None, **kwargs: Any) -> Any:
        return self._page.wait_for_load_state(state, **kwargs)

    def evaluate(self, expression: str, arg: Optional[Any] = None) -> Any:
        return self._page.evaluate(expression, arg)

    def screenshot(self, **kwargs: Any) -> bytes:
        return self._page.screenshot(**kwargs)

    def close(self) -> None:
        self._page.close()

    def __getattr__(self, name: str) -> Any:
        return getattr(self._page, name)
