import pytest
from typing import Generator
from playwright.sync_api import Page
from selfheal.config import SelfHealConfig
from selfheal.database.connection import DatabaseManager
from selfheal.baseline.repository import BaselineRepository
from selfheal.engine.page import SelfHealingPage


@pytest.fixture(scope="session")
def selfheal_config() -> SelfHealConfig:
    return SelfHealConfig.load_from_yaml("configs/default.yaml")


@pytest.fixture(scope="session")
def selfheal_db(selfheal_config: SelfHealConfig) -> DatabaseManager:
    return DatabaseManager(selfheal_config.framework.database_path)


@pytest.fixture(scope="session")
def selfheal_repo(selfheal_db: DatabaseManager) -> BaselineRepository:
    return BaselineRepository(selfheal_db)


@pytest.fixture(scope="function")
def healed_page(
    page: Page,
    selfheal_config: SelfHealConfig,
    selfheal_db: DatabaseManager
) -> Generator[SelfHealingPage, None, None]:
    """
    Pytest fixture supplying a SelfHealingPage instance wrapping Playwright's page.
    Automatically manages database connection and execution manager.
    """
    repo = BaselineRepository(selfheal_db)
    run_id = repo.create_test_run(
        project_name=selfheal_config.framework.project_name,
        policy=selfheal_config.framework.policy.value
    )
    sh_page = SelfHealingPage(
        page=page,
        config=selfheal_config,
        db_manager=selfheal_db,
        run_id=run_id
    )

    yield sh_page

    # Conclude test run summary
    events = repo.get_healing_events(run_id=run_id)
    healed_count = sum(1 for e in events if e.get("decision") == "APPROVED" and e.get("retry_success"))
    failed_count = sum(1 for e in events if e.get("decision") != "APPROVED" or not e.get("retry_success"))
    repo.finish_test_run(
        run_id=run_id,
        total_steps=len(events),
        passed=healed_count,
        failed=failed_count,
        healed=healed_count,
        status="COMPLETED"
    )
