import sqlite3
from pathlib import Path
from typing import Generator
from contextlib import contextmanager


class DatabaseManager:
    def __init__(self, db_path: str | Path = "artifacts/selfheal.db"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.init_db()

    def get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(
            self.db_path,
            timeout=10.0,
            check_same_thread=False
        )
        conn.row_factory = sqlite3.Row
        # Enable Write-Ahead Logging (WAL) for high concurrency
        conn.execute("PRAGMA journal_mode = WAL;")
        conn.execute("PRAGMA busy_timeout = 5000;")
        conn.execute("PRAGMA foreign_keys = ON;")
        return conn

    @contextmanager
    def session(self) -> Generator[sqlite3.Connection, None, None]:
        conn = self.get_connection()
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def init_db(self) -> None:
        schema_path = Path(__file__).parent / "schema.sql"
        if not schema_path.is_file():
            return
        with open(schema_path, "r", encoding="utf-8") as f:
            ddl = f.read()

        with self.session() as conn:
            conn.executescript(ddl)
