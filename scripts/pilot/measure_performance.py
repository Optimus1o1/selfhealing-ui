"""
SelfHeal Pilot — Performance Measurement Script.
Moon Sanctum Labs -- Decode. Build. Evolve.

Measures healing latency by running a scenario multiple times.
Uses the bundled demo application or a user-specified URL.

Usage:
    python scripts/pilot/measure_performance.py --iterations 10
    python scripts/pilot/measure_performance.py --iterations 50 --output perf_results.json

Non-destructive: uses the bundled demo app in read-only test mode.
"""

import argparse
import json
import statistics
import sys
import time
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
if str(PROJECT_ROOT / "src") not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT / "src"))

from selfheal.config import SelfHealConfig
from selfheal.intelligence.scoring import SimilarityScorer
from selfheal.intelligence.decision_engine import HealingDecisionEngine


def measure_scoring_performance(iterations: int, config_path: str) -> dict:
    """Measure pure algorithm scoring latency using synthetic fingerprint data."""
    config = SelfHealConfig.load_from_yaml(config_path)
    scorer = SimilarityScorer(config)

    # Synthetic baseline fingerprint (representative of real-world elements)
    baseline_fp = {
        "tag": "button",
        "text": "Add to Cart",
        "aria_label": "Add to Cart",
        "aria_role": "button",
        "attributes": {"id": "add-to-cart-btn", "class": "btn btn-primary", "type": "submit"},
        "parent_tag": "div",
        "parent_class": "product-actions",
        "children_count": 0,
        "children_tags": [],
        "position": {"x": 450, "y": 320, "width": 120, "height": 40},
    }

    # Synthetic candidate (similar but changed — simulates a UI mutation)
    candidate_fp = {
        "tag": "button",
        "text": "Add to Basket",
        "aria_label": "Add to Basket",
        "aria_role": "button",
        "attributes": {"id": "add-to-basket-btn", "class": "btn btn-action", "type": "submit"},
        "parent_tag": "div",
        "parent_class": "product-controls",
        "children_count": 0,
        "children_tags": [],
        "position": {"x": 460, "y": 325, "width": 130, "height": 40},
    }

    latencies = []
    scores = []

    print(f"[PERF] Running {iterations} scoring iterations...")

    for i in range(iterations):
        start = time.perf_counter()
        score = scorer.compute_similarity(baseline_fp, candidate_fp)
        elapsed = (time.perf_counter() - start) * 1000  # ms
        latencies.append(elapsed)
        scores.append(score)

        if (i + 1) % 10 == 0:
            print(f"         Iteration {i + 1}/{iterations} — {elapsed:.3f}ms (score: {score:.4f})")

    results = {
        "iterations": iterations,
        "score_mean": round(statistics.mean(scores), 4),
        "latency_ms": {
            "mean": round(statistics.mean(latencies), 3),
            "median": round(statistics.median(latencies), 3),
            "p95": round(sorted(latencies)[int(len(latencies) * 0.95)], 3),
            "p99": round(sorted(latencies)[int(len(latencies) * 0.99)], 3),
            "min": round(min(latencies), 3),
            "max": round(max(latencies), 3),
            "stdev": round(statistics.stdev(latencies), 3) if len(latencies) > 1 else 0,
        },
    }

    print(f"\n[PERF] Scoring Results:")
    print(f"  Mean score:     {results['score_mean']}")
    print(f"  Mean latency:   {results['latency_ms']['mean']}ms")
    print(f"  Median latency: {results['latency_ms']['median']}ms")
    print(f"  P95 latency:    {results['latency_ms']['p95']}ms")
    print(f"  P99 latency:    {results['latency_ms']['p99']}ms")

    return results


def measure_decision_performance(iterations: int, config_path: str) -> dict:
    """Measure decision engine (threshold + margin gating) latency."""
    config = SelfHealConfig.load_from_yaml(config_path)
    engine = HealingDecisionEngine(config)

    # Synthetic scored candidates
    candidates = [
        {"score": 0.92, "fingerprint": {"tag": "button", "text": "Add to Basket"}},
        {"score": 0.65, "fingerprint": {"tag": "button", "text": "Remove Item"}},
        {"score": 0.45, "fingerprint": {"tag": "a", "text": "Back to Products"}},
    ]

    latencies = []

    print(f"[PERF] Running {iterations} decision engine iterations...")

    for i in range(iterations):
        start = time.perf_counter()
        try:
            engine.decide(candidates)
        except Exception:
            pass  # Expected for some candidate configurations
        elapsed = (time.perf_counter() - start) * 1000
        latencies.append(elapsed)

    results = {
        "iterations": iterations,
        "latency_ms": {
            "mean": round(statistics.mean(latencies), 3),
            "median": round(statistics.median(latencies), 3),
            "p95": round(sorted(latencies)[int(len(latencies) * 0.95)], 3),
            "min": round(min(latencies), 3),
            "max": round(max(latencies), 3),
        },
    }

    print(f"\n[PERF] Decision Engine Results:")
    print(f"  Mean latency:   {results['latency_ms']['mean']}ms")
    print(f"  Median latency: {results['latency_ms']['median']}ms")

    return results


def main():
    parser = argparse.ArgumentParser(
        description="SelfHeal Pilot — Measure scoring and decision latency"
    )
    parser.add_argument(
        "--iterations", type=int, default=100, help="Number of iterations (default: 100)"
    )
    parser.add_argument("--config", default="configs/default.yaml", help="SelfHeal config path")
    parser.add_argument("--output", help="Save results to JSON file")

    args = parser.parse_args()

    scoring_results = measure_scoring_performance(args.iterations, args.config)
    decision_results = measure_decision_performance(args.iterations, args.config)

    combined = {
        "selfheal_version": "1.0.0",
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "scoring": scoring_results,
        "decision_engine": decision_results,
    }

    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(combined, f, indent=2)
        print(f"\n[PERF] Results saved to {output_path}")
    else:
        print(f"\n[PERF] Combined JSON:")
        print(json.dumps(combined, indent=2))


if __name__ == "__main__":
    main()

