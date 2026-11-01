from pathlib import Path
from datetime import datetime, timezone
import json
from jinja2 import Environment, FileSystemLoader
from selfheal.baseline.repository import BaselineRepository


class ReportGenerator:
    def __init__(self, repository: BaselineRepository, output_dir: str | Path = "artifacts/reports"):
        self.repo = repository
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        template_dir = Path(__file__).parent / "templates"
        self.jinja_env = Environment(loader=FileSystemLoader(str(template_dir)))

    def generate_json_report(self, run_id: int | None = None, filename: str = "report.json") -> Path:
        events = self.repo.get_healing_events(run_id=run_id)
        stats = self.repo.get_run_statistics()
        data = {
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "run_id": run_id,
            "statistics": stats,
            "healing_events": events,
            "locator_history": self.repo.get_locator_history()
        }
        out_path = self.output_dir / filename
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        return out_path

    def generate_html_report(
        self,
        project_name: str = "SelfHealing UI",
        policy: str = "assisted",
        run_id: int | None = None,
        filename: str = "report.html"
    ) -> Path:
        events = self.repo.get_healing_events(run_id=run_id)
        total_events = len(events)
        approved = [e for e in events if e.get("decision") == "APPROVED"]
        approved_count = len(approved)
        rejected_count = total_events - approved_count

        avg_confidence = round(
            sum(e["similarity_score"] for e in approved if e.get("similarity_score")) / max(1, approved_count) * 100,
            1
        ) if approved_count > 0 else 0.0

        avg_latency = round(
            sum(e.get("latency_ms", 0.0) for e in events) / max(1, total_events),
            1
        ) if total_events > 0 else 0.0

        template = self.jinja_env.get_template("report_template.html")
        html_content = template.render(
            project_name=project_name,
            policy=policy,
            generated_at=datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC"),
            total_events=total_events,
            approved_count=approved_count,
            rejected_count=rejected_count,
            avg_confidence=avg_confidence,
            avg_latency_ms=avg_latency,
            events=events
        )

        out_path = self.output_dir / filename
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(html_content)
        return out_path
