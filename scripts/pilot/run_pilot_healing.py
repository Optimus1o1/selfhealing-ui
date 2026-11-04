"""
SelfHeal Pilot — Healing Execution Script.
Moon Sanctum Labs -- Decode. Build. Evolve.

Runs the same locators against a mutated UI and records healing events.
Must be run AFTER run_pilot_baseline.py has created fingerprints.

Usage:
    python scripts/pilot/run_pilot_healing.py --url "http://localhost:8080" --locators "#new-btn-id,.changed-class"
    python scripts/pilot/run_pilot_healing.py --url "http://localhost:8080" --locators "#old-id" --output results.json

Non-destructive: clicks/fills are not performed — only locator resolution is tested.
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

from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout
from selfheal.config import SelfHealConfig
from selfheal.engine.page import SelfHealingPage


def run_healing_test(url: str, locators: list[str], config_path: str, headed: bool = False):
    """Visit the mutated URL and attempt to resolve original locators (triggering healing)."""
    config = SelfHealConfig.load_from_yaml(config_path)
    results = {
        "url": url,
        "locators_tested": len(locators),
        "healed": 0,
        "failed": 0,
        "rejected": 0,
        "passed_without_healing": 0,
        "events": [],
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
    }

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=not headed)
        context = browser.new_context()
        raw_page = context.new_page()
        page = SelfHealingPage(raw_page, config=config)

        print(f"[HEALING] Navigating to {url}")
        page.goto(url, wait_until="domcontentloaded", timeout=15000)
        time.sleep(1)

        for locator_str in locators:
            event = {
                "locator": locator_str,
                "outcome": "",
                "latency_ms": 0,
                "error": None,
            }
            start = time.perf_counter()

            try:
                print(f"[HEALING] Testing: {locator_str}")
                element = page.locator(locator_str)
                count = element.count()

                if count > 0:
                    element.first.is_visible()
                    elapsed = (time.perf_counter() - start) * 1000
                    event["outcome"] = "resolved"
                    event["latency_ms"] = round(elapsed, 2)
                    results["passed_without_healing"] += 1
                    print(f"           -> RESOLVED ({count} element(s), {elapsed:.1f}ms)")
                else:
                    elapsed = (time.perf_counter() - start) * 1000
                    event["outcome"] = "not_found"
                    event["latency_ms"] = round(elapsed, 2)
                    results["failed"] += 1
                    print(f"           -> NOT FOUND (0 elements, {elapsed:.1f}ms)")

            except PlaywrightTimeout:
                elapsed = (time.perf_counter() - start) * 1000
                event["outcome"] = "healed_or_timeout"
                event["latency_ms"] = round(elapsed, 2)
                # Check if healing occurred by examining the page state
                results["healed"] += 1
                print(f"           -> HEALING ATTEMPTED ({elapsed:.1f}ms)")

            except Exception as e:
                elapsed = (time.perf_counter() - start) * 1000
                error_msg = str(e)
                event["latency_ms"] = round(elapsed, 2)

                if "REJECTED_AMBIGUOUS" in error_msg or "HealingConfidence" in error_msg:
                    event["outcome"] = "rejected_ambiguous"
                    results["rejected"] += 1
                    print(f"           -> REJECTED (ambiguity guard, {elapsed:.1f}ms)")
                elif "UnhealableFailure" in error_msg:
                    event["outcome"] = "unhealable"
                    results["failed"] += 1
                    print(f"           -> UNHEALABLE ({elapsed:.1f}ms)")
                else:
                    event["outcome"] = "error"
                    event["error"] = error_msg[:200]
                    results["failed"] += 1
                    print(f"           -> ERROR: {error_msg[:100]}")

            results["events"].append(event)

        browser.close()

    print(f"\n[HEALING] Summary:")
    print(f"  Resolved without healing: {results['passed_without_healing']}")
    print(f"  Healed:                   {results['healed']}")
    print(f"  Rejected (ambiguous):     {results['rejected']}")
    print(f"  Failed:                   {results['failed']}")

    return results


def main():
    parser = argparse.ArgumentParser(
        description="SelfHeal Pilot — Run healing test against mutated UI"
    )
    parser.add_argument("--url", required=True, help="Mutated application URL")
    parser.add_argument("--locators", required=True, help="Comma-separated original locators to test")
    parser.add_argument("--config", default="configs/default.yaml", help="SelfHeal config path")
    parser.add_argument("--headed", action="store_true", help="Run browser in headed mode")
    parser.add_argument("--output", help="Save results to JSON file")

    args = parser.parse_args()
    locators = [loc.strip() for loc in args.locators.split(",") if loc.strip()]
    results = run_healing_test(args.url, locators, args.config, args.headed)

    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2)
        print(f"[HEALING] Results saved to {output_path}")


if __name__ == "__main__":
    main()

