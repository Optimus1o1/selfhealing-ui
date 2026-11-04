"""
SelfHeal Pilot — Baseline Creation Script.
Moon Sanctum Labs -- Decode. Build. Evolve.

Creates a fingerprint baseline for a given URL by visiting the page
and interacting with specified locators using SelfHealingPage.

Usage:
    python scripts/pilot/run_pilot_baseline.py --url "http://localhost:8080" --locators "#btn1,#btn2,.nav-link"
    python scripts/pilot/run_pilot_baseline.py --url "http://localhost:8080" --discover

Non-destructive: only reads DOM elements and stores fingerprints locally.
"""

import argparse
import json
import sys
import time
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
if str(PROJECT_ROOT / "src") not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT / "src"))

from playwright.sync_api import sync_playwright
from selfheal.config import SelfHealConfig
from selfheal.engine.page import SelfHealingPage


def create_baseline(url: str, locators: list[str], config_path: str, headed: bool = False):
    """Visit a URL and interact with locators to create baseline fingerprints."""
    config = SelfHealConfig.load_from_yaml(config_path)
    results = {
        "url": url,
        "locators_requested": len(locators),
        "baselines_created": 0,
        "errors": [],
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
    }

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=not headed)
        context = browser.new_context()
        raw_page = context.new_page()
        page = SelfHealingPage(raw_page, config=config)

        print(f"[BASELINE] Navigating to {url}")
        page.goto(url, wait_until="domcontentloaded", timeout=15000)
        time.sleep(1)  # Allow dynamic content to render

        for locator_str in locators:
            try:
                print(f"[BASELINE] Fingerprinting: {locator_str}")
                element = page.locator(locator_str)
                # Trigger a non-destructive action to register the fingerprint
                count = element.count()
                if count > 0:
                    # Just evaluate to register — don't click
                    element.first.is_visible()
                    results["baselines_created"] += 1
                    print(f"           -> OK ({count} element(s) found)")
                else:
                    results["errors"].append({"locator": locator_str, "error": "No elements found"})
                    print(f"           -> SKIP (0 elements)")
            except Exception as e:
                results["errors"].append({"locator": locator_str, "error": str(e)})
                print(f"           -> ERROR: {e}")

        browser.close()

    print(f"\n[BASELINE] Complete: {results['baselines_created']}/{results['locators_requested']} baselines created")
    if results["errors"]:
        print(f"[BASELINE] {len(results['errors'])} error(s) encountered")

    return results


def main():
    parser = argparse.ArgumentParser(
        description="SelfHeal Pilot — Create baseline fingerprints for a URL"
    )
    parser.add_argument("--url", required=True, help="Application URL to baseline")
    parser.add_argument(
        "--locators",
        help="Comma-separated CSS selectors to fingerprint (e.g., '#btn1,.nav-link')",
    )
    parser.add_argument(
        "--config",
        default="configs/default.yaml",
        help="Path to SelfHeal config YAML (default: configs/default.yaml)",
    )
    parser.add_argument("--headed", action="store_true", help="Run browser in headed mode")
    parser.add_argument("--output", help="Save results to JSON file")

    args = parser.parse_args()

    if not args.locators:
        print("Error: --locators is required. Provide comma-separated CSS selectors.")
        print("Example: --locators \"#submit-btn,.product-card,button[type=submit]\"")
        sys.exit(1)

    locators = [loc.strip() for loc in args.locators.split(",") if loc.strip()]
    results = create_baseline(args.url, locators, args.config, args.headed)

    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2)
        print(f"[BASELINE] Results saved to {output_path}")


if __name__ == "__main__":
    main()

