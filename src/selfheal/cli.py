import click
import subprocess
import sys
from pathlib import Path
from selfheal.config import SelfHealConfig
from selfheal.database.connection import DatabaseManager
from selfheal.baseline.repository import BaselineRepository
from selfheal.reporting.report_generator import ReportGenerator


@click.group()
def cli():
    """Self-Healing UI Automation Framework CLI (Moon Sanctum Labs)."""
    pass


@cli.command()
@click.option("--tests", default="tests/healing", help="Path to test directory or file.")
@click.option("--headed", is_flag=True, help="Run browser in headed mode.")
def test(tests: str, headed: bool):
    """Run Playwright tests with self-healing enabled."""
    click.echo(f"[*] Running tests with SelfHeal engine in: {tests}")
    cmd = [sys.executable, "-m", "pytest", tests, "-v"]
    if headed:
        cmd.append("--headed")
    result = subprocess.run(cmd)
    sys.exit(result.returncode)


@cli.command()
@click.option("--format", "fmt", type=click.Choice(["html", "json", "all"]), default="all")
def report(fmt: str):
    """Generate post-run audit and healing reports."""
    config = SelfHealConfig.load_from_yaml("configs/default.yaml")
    db_mgr = DatabaseManager(config.framework.database_path)
    repo = BaselineRepository(db_mgr)
    gen = ReportGenerator(repo, output_dir=config.framework.report_dir)

    if fmt in ("json", "all"):
        json_path = gen.generate_json_report()
        click.echo(f"[+] JSON report generated: {json_path}")
    if fmt in ("html", "all"):
        html_path = gen.generate_html_report(project_name=config.framework.project_name)
        click.echo(f"[+] HTML report generated: {html_path}")


@cli.command()
@click.option("--port", default=8501, help="Port to serve Streamlit dashboard.")
def dashboard(port: int):
    """Launch the interactive Streamlit Audit Dashboard."""
    app_path = Path(__file__).parent / "dashboard" / "app.py"
    click.echo(f"[*] Launching SelfHeal Dashboard on port {port}...")
    subprocess.run([sys.executable, "-m", "streamlit", "run", str(app_path), "--server.port", str(port)])


@cli.command()
def baselines():
    """List all active element fingerprints in the repository."""
    config = SelfHealConfig.load_from_yaml("configs/default.yaml")
    db_mgr = DatabaseManager(config.framework.database_path)
    repo = BaselineRepository(db_mgr)
    fps = repo.get_all_active_fingerprints()
    if not fps:
        click.echo("[-] No active element fingerprints found.")
        return
    click.echo(f"[+] Found {len(fps)} active baseline fingerprint(s):")
    for fp in fps:
        click.echo(f"  - {fp.target_key} (v{fp.version}) [{fp.tag_name}]: '{fp.inner_text}' -> {fp.original_selector}")


@cli.command()
def reset_db():
    """Reset the SQLite database for a clean test run."""
    config = SelfHealConfig.load_from_yaml("configs/default.yaml")
    db_path = Path(config.framework.database_path)
    if db_path.exists():
        db_path.unlink()
        click.echo(f"[+] Deleted database: {db_path}")
    db_mgr = DatabaseManager(db_path)
    click.echo("[+] Database re-initialized successfully.")


if __name__ == "__main__":
    cli()
