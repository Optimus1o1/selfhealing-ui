from typing import Optional, Any
import json
from datetime import datetime, timezone
from selfheal.database.connection import DatabaseManager
from selfheal.baseline.fingerprint import ElementFingerprint
from selfheal.database.models import TestRunModel, HealingEventModel, LocatorHistoryModel


class BaselineRepository:
    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager

    def save_fingerprint(self, fingerprint: ElementFingerprint) -> int:
        with self.db.session() as conn:
            # Check existing active version for target_key
            cur = conn.execute(
                "SELECT id, version FROM element_fingerprints WHERE target_key = ? AND status = 'active' ORDER BY version DESC LIMIT 1",
                (fingerprint.target_key,)
            )
            existing = cur.fetchone()
            if existing:
                # If there's an existing active version, determine next version
                next_version = existing["version"] + 1
            else:
                next_version = 1

            fingerprint.version = next_version
            data = fingerprint.to_db_row()
            columns = ", ".join(data.keys())
            placeholders = ", ".join(["?"] * len(data))
            sql = f"INSERT INTO element_fingerprints ({columns}) VALUES ({placeholders})"
            cursor = conn.execute(sql, list(data.values()))
            return cursor.lastrowid

    def get_active_fingerprint(self, target_key: str) -> Optional[ElementFingerprint]:
        with self.db.session() as conn:
            cur = conn.execute(
                """
                SELECT * FROM element_fingerprints 
                WHERE target_key = ? AND status = 'active' 
                ORDER BY version DESC LIMIT 1
                """,
                (target_key,)
            )
            row = cur.fetchone()
            if row:
                return ElementFingerprint.from_db_row(dict(row))
            return None

    def get_all_active_fingerprints(self) -> list[ElementFingerprint]:
        with self.db.session() as conn:
            cur = conn.execute(
                "SELECT * FROM element_fingerprints WHERE status = 'active' ORDER BY target_key ASC"
            )
            return [ElementFingerprint.from_db_row(dict(r)) for r in cur.fetchall()]

    def promote_healed_locator(self, target_key: str, new_locator: str, similarity_score: float, approved_by: str = "system") -> None:
        with self.db.session() as conn:
            # Archive old active version
            cur = conn.execute(
                "SELECT * FROM element_fingerprints WHERE target_key = ? AND status = 'active' ORDER BY version DESC LIMIT 1",
                (target_key,)
            )
            old_row = cur.fetchone()
            old_locator = old_row["original_selector"] if old_row else "unknown"

            if old_row:
                conn.execute(
                    "UPDATE element_fingerprints SET status = 'archived' WHERE id = ?",
                    (old_row["id"],)
                )
                # Clone as new active version with updated selector
                new_fp = dict(old_row)
                new_fp.pop("id", None)
                new_fp["version"] = old_row["version"] + 1
                new_fp["status"] = "active"
                new_fp["original_selector"] = new_locator
                new_fp["created_at"] = datetime.now(timezone.utc).isoformat()
                new_fp["updated_at"] = datetime.now(timezone.utc).isoformat()

                cols = ", ".join(new_fp.keys())
                vals = ", ".join(["?"] * len(new_fp))
                conn.execute(f"INSERT INTO element_fingerprints ({cols}) VALUES ({vals})", list(new_fp.values()))

            # Record in locator_history
            conn.execute(
                """
                INSERT INTO locator_history (target_key, old_locator, new_locator, similarity_score, change_type, approved_by)
                VALUES (?, ?, ?, ?, 'HEALED_PROMOTED', ?)
                """,
                (target_key, old_locator, new_locator, similarity_score, approved_by)
            )

            # Update healing_events status
            conn.execute(
                "UPDATE healing_events SET status = 'promoted' WHERE target_key = ? AND status = 'pending_review'",
                (target_key,)
            )

    def reject_healing_event(self, event_id: int) -> None:
        with self.db.session() as conn:
            conn.execute(
                "UPDATE healing_events SET status = 'rejected' WHERE id = ?",
                (event_id,)
            )

    def create_test_run(self, project_name: str, policy: str) -> int:
        import uuid
        run_uuid = str(uuid.uuid4())
        with self.db.session() as conn:
            cur = conn.execute(
                """
                INSERT INTO test_runs (run_uuid, project_name, policy, status)
                VALUES (?, ?, ?, 'RUNNING')
                """,
                (run_uuid, project_name, policy)
            )
            return cur.lastrowid

    def finish_test_run(self, run_id: int, total_steps: int, passed: int, failed: int, healed: int, status: str = "COMPLETED") -> None:
        with self.db.session() as conn:
            conn.execute(
                """
                UPDATE test_runs 
                SET completed_at = CURRENT_TIMESTAMP, total_steps = ?, passed_count = ?, failed_count = ?, healed_count = ?, status = ?
                WHERE id = ?
                """,
                (total_steps, passed, failed, healed, status, run_id)
            )

    def record_healing_event(self, event: HealingEventModel) -> int:
        with self.db.session() as conn:
            cur = conn.execute(
                """
                INSERT INTO healing_events (
                    run_id, target_key, original_locator, healed_locator,
                    similarity_score, score_breakdown_json, decision, reason,
                    status, retry_success, latency_ms
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    event.run_id,
                    event.target_key,
                    event.original_locator,
                    event.healed_locator,
                    event.similarity_score,
                    event.score_breakdown_json,
                    event.decision,
                    event.reason,
                    event.status,
                    1 if event.retry_success else 0,
                    event.latency_ms,
                )
            )
            return cur.lastrowid

    def get_healing_events(self, run_id: Optional[int] = None) -> list[dict[str, Any]]:
        with self.db.session() as conn:
            if run_id:
                cur = conn.execute(
                    "SELECT * FROM healing_events WHERE run_id = ? ORDER BY created_at DESC",
                    (run_id,)
                )
            else:
                cur = conn.execute(
                    "SELECT * FROM healing_events ORDER BY created_at DESC"
                )
            return [dict(r) for r in cur.fetchall()]

    def get_locator_history(self, target_key: Optional[str] = None) -> list[dict[str, Any]]:
        with self.db.session() as conn:
            if target_key:
                cur = conn.execute(
                    "SELECT * FROM locator_history WHERE target_key = ? ORDER BY promoted_at DESC",
                    (target_key,)
                )
            else:
                cur = conn.execute(
                    "SELECT * FROM locator_history ORDER BY promoted_at DESC"
                )
            return [dict(r) for r in cur.fetchall()]

    def get_run_statistics(self) -> dict[str, Any]:
        with self.db.session() as conn:
            cur = conn.execute("SELECT COUNT(*) as total_runs, SUM(total_steps) as total_steps, SUM(passed_count) as total_passed, SUM(failed_count) as total_failed, SUM(healed_count) as total_healed FROM test_runs")
            stats = dict(cur.fetchone() or {})
            cur_events = conn.execute("SELECT COUNT(*) as total_healing_events, AVG(similarity_score) as avg_score, AVG(latency_ms) as avg_latency FROM healing_events WHERE decision = 'APPROVED'")
            ev_stats = dict(cur_events.fetchone() or {})
            stats.update(ev_stats)
            return stats

    def get_test_runs(self) -> list[dict[str, Any]]:
        with self.db.session() as conn:
            cur = conn.execute("SELECT * FROM test_runs ORDER BY started_at DESC")
            return [dict(r) for r in cur.fetchall()]

    def get_fingerprint_versions(self, target_key: str) -> list[ElementFingerprint]:
        with self.db.session() as conn:
            cur = conn.execute(
                "SELECT * FROM element_fingerprints WHERE target_key = ? ORDER BY version ASC",
                (target_key,)
            )
            return [ElementFingerprint.from_db_row(dict(r)) for r in cur.fetchall()]

    def get_healing_event_by_id(self, event_id: int) -> Optional[dict[str, Any]]:
        with self.db.session() as conn:
            cur = conn.execute("SELECT * FROM healing_events WHERE id = ?", (event_id,))
            row = cur.fetchone()
            return dict(row) if row else None

    def get_all_target_keys(self) -> list[str]:
        with self.db.session() as conn:
            cur = conn.execute("SELECT DISTINCT target_key FROM element_fingerprints ORDER BY target_key ASC")
            return [r["target_key"] for r in cur.fetchall()]

    def get_locator_stability_stats(self) -> list[dict[str, Any]]:
        with self.db.session() as conn:
            cur = conn.execute("""
                SELECT 
                    ef.target_key,
                    MIN(ef.original_selector) as initial_selector,
                    MAX(ef.version) as total_versions,
                    MAX(ef.created_at) as last_updated,
                    (SELECT original_selector FROM element_fingerprints WHERE target_key = ef.target_key AND status = 'active' ORDER BY version DESC LIMIT 1) as active_selector,
                    (SELECT COUNT(*) FROM healing_events WHERE target_key = ef.target_key) as times_intercepted,
                    (SELECT COUNT(*) FROM healing_events WHERE target_key = ef.target_key AND decision = 'APPROVED') as times_approved,
                    (SELECT COUNT(*) FROM healing_events WHERE target_key = ef.target_key AND decision != 'APPROVED') as times_rejected
                FROM element_fingerprints ef
                GROUP BY ef.target_key
                ORDER BY ef.target_key ASC
            """)
            return [dict(r) for r in cur.fetchall()]

    def get_latency_percentiles(self) -> dict[str, float]:
        with self.db.session() as conn:
            cur = conn.execute("SELECT latency_ms FROM healing_events WHERE latency_ms > 0 ORDER BY latency_ms ASC")
            lats = [r["latency_ms"] for r in cur.fetchall()]
            if not lats:
                return {"count": 0, "mean": 0.0, "p50": 0.0, "p90": 0.0, "p95": 0.0, "min": 0.0, "max": 0.0}

            n = len(lats)
            def percentile(p: float) -> float:
                idx = int(p * (n - 1))
                return lats[idx]

            return {
                "count": n,
                "mean": round(sum(lats) / n, 2),
                "p50": round(percentile(0.50), 2),
                "p90": round(percentile(0.90), 2),
                "p95": round(percentile(0.95), 2),
                "min": round(lats[0], 2),
                "max": round(lats[-1], 2),
            }


