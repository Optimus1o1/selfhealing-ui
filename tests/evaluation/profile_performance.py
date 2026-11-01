"""
Multi-Tier Performance Profiling Suite.
Measures:
1. Pure Algorithm Latency (Similarity Scoring + Decision Engine)
2. DOM Extraction Latency (In-Browser JavaScript evaluation via page.evaluate)
3. Normal Execution Overhead (Playwright native click vs SelfHealingLocator click)
4. Full Browser-Based Healing Latency (Timeout -> Classification -> Scan -> Score -> Decision -> Retry)
Calculates Mean, Min, Max, Median (P50), and 95th Percentile (P95).
"""

import sys
import time
import json
from pathlib import Path
from playwright.sync_api import sync_playwright

# Add root and src to sys.path
root_dir = Path(__file__).resolve().parent.parent.parent
src_dir = root_dir / "src"
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))
if str(src_dir) not in sys.path:
    sys.path.insert(0, str(src_dir))

from selfheal.config import SelfHealConfig
from selfheal.database.connection import DatabaseManager
from selfheal.baseline.repository import BaselineRepository
from selfheal.baseline.fingerprint import ElementFingerprint, BoundingBox
from selfheal.scanner.dom_scanner import DOMScanner, CandidateElement
from selfheal.intelligence.scoring import SimilarityScorer
from selfheal.intelligence.decision_engine import HealingDecisionEngine
from selfheal.engine.page import SelfHealingPage
from demo_app.app import DemoServer


def calculate_percentiles(times: list[float]) -> dict[str, float]:
    sorted_times = sorted(times)
    n = len(sorted_times)
    mean_val = sum(sorted_times) / n
    p50_val = sorted_times[n // 2]
    p95_val = sorted_times[min(int(n * 0.95), n - 1)]
    return {
        "mean_ms": round(mean_val, 3),
        "median_p50_ms": round(p50_val, 3),
        "p95_ms": round(p95_val, 3),
        "min_ms": round(sorted_times[0], 3),
        "max_ms": round(sorted_times[-1], 3)
    }


def run_profiler(iterations: int = 30):
    print("\n" + "="*75)
    print("      SELF-HEALING FRAMEWORK MULTI-TIER PERFORMANCE PROFILER")
    print("="*75)

    config = SelfHealConfig.load_from_yaml("configs/default.yaml")
    scorer = SimilarityScorer(config.weights)
    decision_engine = HealingDecisionEngine(config.thresholds)

    # -------------------------------------------------------------
    # TIER 1: Pure Algorithm Latency (Scoring + Decision Engine)
    # -------------------------------------------------------------
    base = ElementFingerprint(
        target_key="auth.submit", tag_name="button", element_id="loginBtn",
        class_list=["btn", "btn-primary"], inner_text="Login",
        aria_role="button", input_type="submit", attributes={"name": "submit", "data-testid": "auth-submit"},
        parent_tag="form", parent_id="loginForm", bounding_box=BoundingBox(x=200, y=400, width=120, height=40)
    )

    # Synthetic candidate pool of 50 elements
    candidates = [
        CandidateElement(
            tag_name="button", element_id=f"btn_{i}",
            class_list=["btn", "btn-primary" if i == 0 else "btn-secondary"],
            inner_text="Sign In" if i == 0 else f"Action {i}",
            aria_role="button", input_type="submit" if i == 0 else "",
            attributes={"data-testid": "auth-submit"} if i == 0 else {},
            parent_tag="form", parent_id="loginForm",
            bounding_box=BoundingBox(x=200 + i, y=400, width=120, height=40)
        )
        for i in range(50)
    ]

    algo_times = []
    for _ in range(iterations * 2):
        t0 = time.perf_counter()
        ranked = scorer.rank_candidates(base, candidates)
        _ = decision_engine.evaluate(base.target_key, "#loginBtn", ranked)
        algo_times.append((time.perf_counter() - t0) * 1000)

    algo_stats = calculate_percentiles(algo_times)
    print("\n[1] PURE ALGORITHM LATENCY (50 Candidates Scoring + Decision Engine)")
    print(f"    • Mean    : {algo_stats['mean_ms']} ms")
    print(f"    • P50     : {algo_stats['median_p50_ms']} ms")
    print(f"    • P95     : {algo_stats['p95_ms']} ms")
    print(f"    • Min/Max : {algo_stats['min_ms']} / {algo_stats['max_ms']} ms")

    # -------------------------------------------------------------
    # TIER 2: Live Browser DOM Extraction Latency
    # -------------------------------------------------------------
    server = DemoServer(host="127.0.0.1", port=8899)
    server.start()

    dom_times = []
    normal_overhead_times = []
    healing_cycle_times = []

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            scanner = DOMScanner()
            db_mgr = DatabaseManager("artifacts/profile.db")
            repo = BaselineRepository(db_mgr)

            page.goto("http://127.0.0.1:8899/v1")

            # DOM Scanner profiling
            for _ in range(iterations):
                t0 = time.perf_counter()
                _ = scanner.scan(page, max_candidates=100)
                dom_times.append((time.perf_counter() - t0) * 1000)

            # Normal Execution Overhead profiling (Native click vs SelfHealingLocator click)
            for _ in range(iterations):
                page.goto("http://127.0.0.1:8899/v1")
                sh_page = SelfHealingPage(page, config=config, db_manager=db_mgr)
                t0 = time.perf_counter()
                # Fast click on present element without healing
                sh_page.healed_locator("#username", key="input.username").fill("benchmark_user")
                normal_overhead_times.append((time.perf_counter() - t0) * 1000)

            # Complete End-to-End Browser Healing Latency
            # Record baseline first on V1
            page.goto("http://127.0.0.1:8899/v1")
            sh_page = SelfHealingPage(page, config=config, db_manager=db_mgr)
            sh_page.healed_locator("#loginBtn", key="perf.button").click()

            # Now measure healing on V2 (locator #loginBtn is missing, heals to #signinBtn)
            for _ in range(iterations):
                page.goto("http://127.0.0.1:8899/v2")
                t0 = time.perf_counter()
                sh_page.healed_locator("#loginBtn", key="perf.button").click()
                healing_cycle_times.append((time.perf_counter() - t0) * 1000)

            browser.close()
    finally:
        server.stop()

    dom_stats = calculate_percentiles(dom_times)
    print("\n[2] LIVE BROWSER DOM EXTRACTION LATENCY (page.evaluate)")
    print(f"    • Mean    : {dom_stats['mean_ms']} ms")
    print(f"    • P50     : {dom_stats['median_p50_ms']} ms")
    print(f"    • P95     : {dom_stats['p95_ms']} ms")
    print(f"    • Min/Max : {dom_stats['min_ms']} / {dom_stats['max_ms']} ms")

    normal_stats = calculate_percentiles(normal_overhead_times)
    print("\n[3] NORMAL EXECUTION OVERHEAD (SelfHealingLocator fill/click on present element)")
    print(f"    • Mean    : {normal_stats['mean_ms']} ms")
    print(f"    • P50     : {normal_stats['median_p50_ms']} ms")
    print(f"    • P95     : {normal_stats['p95_ms']} ms")

    healing_stats = calculate_percentiles(healing_cycle_times)
    print("\n[4] COMPLETE BROWSER-BASED HEALING LATENCY")
    print("    (Initial Failure + Grace Period + DOM Scan + Similarity + Decision + Retried Click)")
    print(f"    • Mean    : {healing_stats['mean_ms']} ms")
    print(f"    • P50     : {healing_stats['median_p50_ms']} ms")
    print(f"    • P95     : {healing_stats['p95_ms']} ms")
    print(f"    • Min/Max : {healing_stats['min_ms']} / {healing_stats['max_ms']} ms")

    print("\n" + "="*75)
    print("                    PERFORMANCE SUMMARY TABLE")
    print("="*75)
    print(f"{'Component':<35} | {'Mean (ms)':<10} | {'P50 (ms)':<10} | {'P95 (ms)':<10}")
    print("-"*75)
    print(f"{'Pure Algorithm Engine':<35} | {algo_stats['mean_ms']:<10} | {algo_stats['median_p50_ms']:<10} | {algo_stats['p95_ms']:<10}")
    print(f"{'DOM Extraction (in-browser)':<35} | {dom_stats['mean_ms']:<10} | {dom_stats['median_p50_ms']:<10} | {dom_stats['p95_ms']:<10}")
    print(f"{'Normal Execution Overhead':<35} | {normal_stats['mean_ms']:<10} | {normal_stats['median_p50_ms']:<10} | {normal_stats['p95_ms']:<10}")
    print(f"{'Full Browser Healing Cycle':<35} | {healing_stats['mean_ms']:<10} | {healing_stats['median_p50_ms']:<10} | {healing_stats['p95_ms']:<10}")
    print("="*75 + "\n")

    profile_results = {
        "pure_algorithm": algo_stats,
        "dom_extraction": dom_stats,
        "normal_execution_overhead": normal_stats,
        "full_browser_healing_cycle": healing_stats
    }

    out_file = Path("artifacts/reports/performance_profile.json")
    out_file.parent.mkdir(parents=True, exist_ok=True)
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(profile_results, f, indent=2)

    return profile_results


if __name__ == "__main__":
    run_profiler()
