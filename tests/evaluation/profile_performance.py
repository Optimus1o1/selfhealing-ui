"""
Multi-Tier Performance Profiling Suite (500+ Iterations).
Measures:
1. Pure Algorithm Latency (Scoring across 50 Candidates)
2. Decision Engine Latency (Threshold evaluation & ambiguity protection)
3. DOM Extraction Latency (In-Browser JavaScript evaluation via page.evaluate)
4. Normal Execution Overhead (Playwright native click vs SelfHealingLocator click)
5. Complete Browser-Based Healing Latency (Timeout -> Classification -> Scan -> Score -> Decision -> Retry)
6. Configurable Fast Healing Latency (Optimized 1000ms action timeout strategy)
7. Rejected Healing Latency (Actionability failure short-circuit)

Calculates Mean, Min, Max, Median (P50), 90th Percentile (P90), and 95th Percentile (P95).
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

from selfheal.config import SelfHealConfig, FrameworkSettings
from selfheal.database.connection import DatabaseManager
from selfheal.baseline.repository import BaselineRepository
from selfheal.baseline.fingerprint import ElementFingerprint, BoundingBox
from selfheal.scanner.dom_scanner import DOMScanner, CandidateElement
from selfheal.intelligence.scoring import SimilarityScorer
from selfheal.intelligence.decision_engine import HealingDecisionEngine
from selfheal.detection.exceptions import UnhealableFailureError
from selfheal.engine.page import SelfHealingPage
from demo_app.app import DemoServer


def calculate_percentiles(times: list[float]) -> dict[str, float]:
    sorted_times = sorted(times)
    n = len(sorted_times)
    if n == 0:
        return {"mean_ms": 0.0, "median_p50_ms": 0.0, "p90_ms": 0.0, "p95_ms": 0.0, "min_ms": 0.0, "max_ms": 0.0}
    mean_val = sum(sorted_times) / n
    p50_val = sorted_times[n // 2]
    p90_val = sorted_times[min(int(n * 0.90), n - 1)]
    p95_val = sorted_times[min(int(n * 0.95), n - 1)]
    return {
        "mean_ms": round(mean_val, 3),
        "median_p50_ms": round(p50_val, 3),
        "p90_ms": round(p90_val, 3),
        "p95_ms": round(p95_val, 3),
        "min_ms": round(sorted_times[0], 3),
        "max_ms": round(sorted_times[-1], 3)
    }


def run_profiler(micro_iterations: int = 500, browser_iterations: int = 15):
    print("\n" + "="*80)
    print("      SELF-HEALING FRAMEWORK MULTI-TIER PERFORMANCE PROFILER (500+ RUNS)")
    print("="*80)

    config = SelfHealConfig.load_from_yaml("configs/default.yaml")
    scorer = SimilarityScorer(config.weights)
    decision_engine = HealingDecisionEngine(config.thresholds)

    # -------------------------------------------------------------
    # TIER 1: Pure Algorithm Latency (500 Iterations + 50 Warm-Up)
    # -------------------------------------------------------------
    base = ElementFingerprint(
        target_key="auth.submit", tag_name="button", element_id="loginBtn",
        class_list=["btn", "btn-primary"], inner_text="Login",
        aria_role="button", input_type="submit", attributes={"name": "submit", "data-testid": "auth-submit"},
        parent_tag="form", parent_id="loginForm", bounding_box=BoundingBox(x=200, y=400, width=120, height=40)
    )

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

    # Warm-up (50 runs)
    for _ in range(50):
        _ = scorer.rank_candidates(base, candidates)

    algo_times = []
    decision_times = []
    for _ in range(micro_iterations):
        t0 = time.perf_counter()
        ranked = scorer.rank_candidates(base, candidates)
        t_algo = (time.perf_counter() - t0) * 1000
        algo_times.append(t_algo)

        t1 = time.perf_counter()
        _ = decision_engine.evaluate(base.target_key, "#loginBtn", ranked)
        t_dec = (time.perf_counter() - t1) * 1000
        decision_times.append(t_dec)

    algo_stats = calculate_percentiles(algo_times)
    dec_stats = calculate_percentiles(decision_times)

    print("\n[1] PURE ALGORITHM SCORING LATENCY (50 Candidates Scoring, 500 Iterations)")
    print(f"    • Mean    : {algo_stats['mean_ms']} ms")
    print(f"    • P50     : {algo_stats['median_p50_ms']} ms")
    print(f"    • P90     : {algo_stats['p90_ms']} ms")
    print(f"    • P95     : {algo_stats['p95_ms']} ms")
    print(f"    • Min/Max : {algo_stats['min_ms']} / {algo_stats['max_ms']} ms")

    print("\n[2] DECISION ENGINE EVALUATION LATENCY (Threshold & Ambiguity Checks, 500 Iterations)")
    print(f"    • Mean    : {dec_stats['mean_ms']} ms")
    print(f"    • P50     : {dec_stats['median_p50_ms']} ms")
    print(f"    • P90     : {dec_stats['p90_ms']} ms")
    print(f"    • P95     : {dec_stats['p95_ms']} ms")

    # -------------------------------------------------------------
    # TIER 2: Live Browser Profiling
    # -------------------------------------------------------------
    server = DemoServer(host="127.0.0.1", port=8899)
    server.start()

    dom_times = []
    normal_overhead_times = []
    healing_cycle_times = []
    fast_healing_times = []
    rejected_healing_times = []

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            scanner = DOMScanner()
            db_mgr = DatabaseManager("artifacts/profile.db")
            repo = BaselineRepository(db_mgr)

            page.goto("http://127.0.0.1:8899/v1")

            # DOM Scanner profiling (500 evaluations with 20 warm-up)
            for _ in range(20):
                _ = scanner.scan(page, max_candidates=100)

            for _ in range(micro_iterations):
                t0 = time.perf_counter()
                _ = scanner.scan(page, max_candidates=100)
                dom_times.append((time.perf_counter() - t0) * 1000)

            # Normal Execution Overhead profiling (Present element fill/click)
            sh_page = SelfHealingPage(page, config=config, db_manager=db_mgr)
            for _ in range(50):
                page.goto("http://127.0.0.1:8899/v1")
                t0 = time.perf_counter()
                sh_page.healed_locator("#username", key="input.username").fill("benchmark_user")
                normal_overhead_times.append((time.perf_counter() - t0) * 1000)

            # Complete End-to-End Browser Healing Latency (Default: 2500ms timeout)
            # Record baseline first on V1
            page.goto("http://127.0.0.1:8899/v1")
            sh_page = SelfHealingPage(page, config=config, db_manager=db_mgr)
            sh_page.healed_locator("#loginBtn", key="perf.button").click()

            for _ in range(browser_iterations):
                page.goto("http://127.0.0.1:8899/v2")
                t0 = time.perf_counter()
                sh_page.healed_locator("#loginBtn", key="perf.button").click()
                healing_cycle_times.append((time.perf_counter() - t0) * 1000)

            # Fast Configurable Healing Latency (Configured: 1000ms action timeout)
            fast_config = SelfHealConfig.load_from_yaml("configs/default.yaml")
            fast_config.framework.action_timeout_ms = 1000
            fast_sh_page = SelfHealingPage(page, config=fast_config, db_manager=db_mgr)

            for _ in range(browser_iterations):
                page.goto("http://127.0.0.1:8899/v2")
                t0 = time.perf_counter()
                fast_sh_page.healed_locator("#loginBtn", key="perf.button").click()
                fast_healing_times.append((time.perf_counter() - t0) * 1000)

            # Rejected Actionability Latency (Unhealable: Hidden or Disabled target)
            for _ in range(browser_iterations):
                page.goto("http://127.0.0.1:8899/v2")
                t0 = time.perf_counter()
                try:
                    # Target an element classified as unhealable
                    sh_page.healed_locator("#disabledBtn", key="disabled.target").click(timeout=800)
                except UnhealableFailureError:
                    rejected_healing_times.append((time.perf_counter() - t0) * 1000)
                except Exception:
                    rejected_healing_times.append((time.perf_counter() - t0) * 1000)

            browser.close()
    finally:
        server.stop()

    dom_stats = calculate_percentiles(dom_times)
    print("\n[3] LIVE BROWSER DOM EXTRACTION LATENCY (page.evaluate, 500 Iterations)")
    print(f"    • Mean    : {dom_stats['mean_ms']} ms")
    print(f"    • P50     : {dom_stats['median_p50_ms']} ms")
    print(f"    • P90     : {dom_stats['p90_ms']} ms")
    print(f"    • P95     : {dom_stats['p95_ms']} ms")
    print(f"    • Min/Max : {dom_stats['min_ms']} / {dom_stats['max_ms']} ms")

    normal_stats = calculate_percentiles(normal_overhead_times)
    print("\n[4] NORMAL EXECUTION OVERHEAD (Present element interaction without healing)")
    print(f"    • Mean    : {normal_stats['mean_ms']} ms")
    print(f"    • P50     : {normal_stats['median_p50_ms']} ms")
    print(f"    • P90     : {normal_stats['p90_ms']} ms")
    print(f"    • P95     : {normal_stats['p95_ms']} ms")

    healing_stats = calculate_percentiles(healing_cycle_times)
    print("\n[5] COMPLETE BROWSER HEALING LATENCY (Standard 2500ms Timeout Strategy)")
    print("    (Action Timeout [2500ms] + Grace Period [500ms] + Scan + Score + Decision + Retried Click)")
    print(f"    • Mean    : {healing_stats['mean_ms']} ms")
    print(f"    • P50     : {healing_stats['median_p50_ms']} ms")
    print(f"    • P90     : {healing_stats['p90_ms']} ms")
    print(f"    • P95     : {healing_stats['p95_ms']} ms")

    fast_stats = calculate_percentiles(fast_healing_times)
    print("\n[6] CONFIGURABLE FAST HEALING LATENCY (Optimized 1000ms Timeout Strategy)")
    print("    (Action Timeout [1000ms] + Grace Period [500ms] + Scan + Score + Decision + Retried Click)")
    print(f"    • Mean    : {fast_stats['mean_ms']} ms")
    print(f"    • P50     : {fast_stats['median_p50_ms']} ms")
    print(f"    • P90     : {fast_stats['p90_ms']} ms")
    print(f"    • P95     : {fast_stats['p95_ms']} ms")

    rejected_stats = calculate_percentiles(rejected_healing_times)
    print("\n[7] REJECTED HEALING LATENCY (Early Classification Short-Circuit)")
    print(f"    • Mean    : {rejected_stats['mean_ms']} ms")
    print(f"    • P50     : {rejected_stats['median_p50_ms']} ms")
    print(f"    • P90     : {rejected_stats['p90_ms']} ms")
    print(f"    • P95     : {rejected_stats['p95_ms']} ms")

    print("\n" + "="*80)
    print("                    PERFORMANCE BENCHMARK SUMMARY TABLE")
    print("="*80)
    print(f"{'Component':<35} | {'Mean (ms)':<10} | {'P50 (ms)':<10} | {'P90 (ms)':<10} | {'P95 (ms)':<10}")
    print("-"*80)
    print(f"{'Pure Algorithm Scoring':<35} | {algo_stats['mean_ms']:<10} | {algo_stats['median_p50_ms']:<10} | {algo_stats['p90_ms']:<10} | {algo_stats['p95_ms']:<10}")
    print(f"{'Decision Engine':<35} | {dec_stats['mean_ms']:<10} | {dec_stats['median_p50_ms']:<10} | {dec_stats['p90_ms']:<10} | {dec_stats['p95_ms']:<10}")
    print(f"{'DOM Extraction (in-browser)':<35} | {dom_stats['mean_ms']:<10} | {dom_stats['median_p50_ms']:<10} | {dom_stats['p90_ms']:<10} | {dom_stats['p95_ms']:<10}")
    print(f"{'Normal Execution Overhead':<35} | {normal_stats['mean_ms']:<10} | {normal_stats['median_p50_ms']:<10} | {normal_stats['p90_ms']:<10} | {normal_stats['p95_ms']:<10}")
    print(f"{'Standard Healing (2500ms timeout)':<35} | {healing_stats['mean_ms']:<10} | {healing_stats['median_p50_ms']:<10} | {healing_stats['p90_ms']:<10} | {healing_stats['p95_ms']:<10}")
    print(f"{'Fast Healing (1000ms timeout)':<35} | {fast_stats['mean_ms']:<10} | {fast_stats['median_p50_ms']:<10} | {fast_stats['p90_ms']:<10} | {fast_stats['p95_ms']:<10}")
    print(f"{'Rejected Healing (Actionability)':<35} | {rejected_stats['mean_ms']:<10} | {rejected_stats['median_p50_ms']:<10} | {rejected_stats['p90_ms']:<10} | {rejected_stats['p95_ms']:<10}")
    print("="*80 + "\n")

    profile_results = {
        "pure_algorithm_scoring": algo_stats,
        "decision_engine": dec_stats,
        "dom_extraction": dom_stats,
        "normal_execution_overhead": normal_stats,
        "standard_healing_2500ms": healing_stats,
        "fast_healing_1000ms": fast_stats,
        "rejected_healing": rejected_stats,
        "analysis": {
            "timeout_dominance_percentage": round((2500 / healing_stats['mean_ms']) * 100, 2) if healing_stats['mean_ms'] > 0 else 0,
            "grace_period_dominance_percentage": round((500 / healing_stats['mean_ms']) * 100, 2) if healing_stats['mean_ms'] > 0 else 0,
            "pure_computation_overhead_ms": round(algo_stats['mean_ms'] + dec_stats['mean_ms'] + dom_stats['mean_ms'], 3)
        }
    }

    out_file = Path("artifacts/reports/performance_profile.json")
    out_file.parent.mkdir(parents=True, exist_ok=True)
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(profile_results, f, indent=2)

    print(f"Results successfully saved to {out_file}")
    return profile_results


if __name__ == "__main__":
    run_profiler()
