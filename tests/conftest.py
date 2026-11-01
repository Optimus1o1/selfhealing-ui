import sys
from pathlib import Path
import pytest

# Ensure src/ is on python path
src_dir = Path(__file__).parent.parent / "src"
if str(src_dir) not in sys.path:
    sys.path.insert(0, str(src_dir))

from selfheal.pytest_plugin import (
    selfheal_config,
    selfheal_db,
    selfheal_repo,
    healed_page,
)
from selfheal.database.connection import DatabaseManager
from demo_app.app import DemoServer


@pytest.fixture(autouse=True)
def clean_test_db(selfheal_db: DatabaseManager):
    """Ensure every test runs against a clean SQLite database."""
    with selfheal_db.get_connection() as conn:
        conn.execute("DELETE FROM healing_events")
        conn.execute("DELETE FROM element_fingerprints")
        conn.execute("DELETE FROM test_runs")
    yield


@pytest.fixture(scope="session")
def demo_server() -> DemoServer:
    server = DemoServer(host="127.0.0.1", port=8899)
    server.start()
    yield server
    server.stop()


