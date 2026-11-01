"""
Evaluation and Benchmarking Suite for Self-Healing UI Automation.
Evaluates Precision, Recall, False Positive Rate (FPR), and Execution Overhead.
"""

import sys
from pathlib import Path

# Add src to sys.path
src_dir = Path(__file__).resolve().parent.parent.parent / "src"
if str(src_dir) not in sys.path:
    sys.path.insert(0, str(src_dir))

import time
from typing import NamedTuple
from selfheal.config import SelfHealConfig
from selfheal.baseline.fingerprint import ElementFingerprint, BoundingBox
from selfheal.scanner.dom_scanner import CandidateElement
from selfheal.intelligence.scoring import SimilarityScorer
from selfheal.intelligence.decision_engine import HealingDecisionEngine, DecisionStatus


class BenchmarkScenario(NamedTuple):
    name: str
    baseline: ElementFingerprint
    candidates: list[CandidateElement]
    expected_outcome: str  # "HEAL" or "REJECT"
    expected_element_id: str = ""


def run_benchmark():
    config = SelfHealConfig.load_from_yaml("configs/default.yaml")
    scorer = SimilarityScorer(config.weights)
    decision_engine = HealingDecisionEngine(config.thresholds)

    # Standard baseline
    base = ElementFingerprint(
        target_key="auth.submit",
        tag_name="button",
        element_id="loginBtn",
        class_list=["btn", "btn-primary"],
        inner_text="Login",
        aria_role="button",
        input_type="submit",
        attributes={"name": "submit", "data-testid": "auth-submit"},
        parent_tag="form",
        parent_id="loginForm",
        bounding_box=BoundingBox(x=200, y=400, width=120, height=40)
    )

    scenarios = [
        # 1. ID Renamed
        BenchmarkScenario(
            name="ID Renamed (#loginBtn -> #signinBtn)",
            baseline=base,
            candidates=[
                CandidateElement(
                    tag_name="button", element_id="signinBtn", class_list=["btn", "btn-primary"],
                    inner_text="Login", aria_role="button", input_type="submit",
                    attributes={"name": "submit", "data-testid": "auth-submit"},
                    parent_tag="form", parent_id="loginForm",
                    bounding_box=BoundingBox(x=200, y=400, width=120, height=40)
                )
            ],
            expected_outcome="HEAL",
            expected_element_id="signinBtn"
        ),
        # 2. Text Rephrased (Login -> Sign In)
        BenchmarkScenario(
            name="Button Text Rephrased ('Login' -> 'Sign In')",
            baseline=base,
            candidates=[
                CandidateElement(
                    tag_name="button", element_id="loginBtn", class_list=["btn", "btn-primary"],
                    inner_text="Sign In", aria_role="button", input_type="submit",
                    attributes={"name": "submit", "data-testid": "auth-submit"},
                    parent_tag="form", parent_id="loginForm",
                    bounding_box=BoundingBox(x=200, y=400, width=120, height=40)
                )
            ],
            expected_outcome="HEAL",
            expected_element_id="loginBtn"
        ),
        # 3. Class Restyled
        BenchmarkScenario(
            name="Classes Changed (Tailwind to Bootstrap)",
            baseline=base,
            candidates=[
                CandidateElement(
                    tag_name="button", element_id="loginBtn", class_list=["bg-blue-600", "px-4"],
                    inner_text="Login", aria_role="button", input_type="submit",
                    attributes={"name": "submit", "data-testid": "auth-submit"},
                    parent_tag="form", parent_id="loginForm",
                    bounding_box=BoundingBox(x=200, y=400, width=120, height=40)
                )
            ],
            expected_outcome="HEAL",
            expected_element_id="loginBtn"
        ),
        # 4. Container Restructured
        BenchmarkScenario(
            name="Parent Container Restructured",
            baseline=base,
            candidates=[
                CandidateElement(
                    tag_name="button", element_id="loginBtn", class_list=["btn", "btn-primary"],
                    inner_text="Login", aria_role="button", input_type="submit",
                    attributes={"name": "submit", "data-testid": "auth-submit"},
                    parent_tag="div", parent_id="newContainer",
                    bounding_box=BoundingBox(x=220, y=420, width=120, height=40)
                )
            ],
            expected_outcome="HEAL",
            expected_element_id="loginBtn"
        ),
        # 5. Position Shifted (Responsive Layout)
        BenchmarkScenario(
            name="Position Shifted by 150px",
            baseline=base,
            candidates=[
                CandidateElement(
                    tag_name="button", element_id="loginBtn", class_list=["btn", "btn-primary"],
                    inner_text="Login", aria_role="button", input_type="submit",
                    attributes={"name": "submit", "data-testid": "auth-submit"},
                    parent_tag="form", parent_id="loginForm",
                    bounding_box=BoundingBox(x=350, y=550, width=120, height=40)
                )
            ],
            expected_outcome="HEAL",
            expected_element_id="loginBtn"
        ),
        # 6. Target Removed Completely
        BenchmarkScenario(
            name="Target Element Removed (Only Unrelated Footer Links)",
            baseline=base,
            candidates=[
                CandidateElement(
                    tag_name="a", element_id="privacyLink", class_list=["footer-link"],
                    inner_text="Privacy Policy", aria_role="link",
                    bounding_box=BoundingBox(x=10, y=900, width=100, height=20)
                )
            ],
            expected_outcome="REJECT"
        ),
        # 7. Ambiguous Tie (Two similar buttons, e.g. Login vs Register without clear winner)
        BenchmarkScenario(
            name="Ambiguous Candidates Margin Check",
            baseline=base,
            candidates=[
                CandidateElement(
                    tag_name="button", element_id="btnA", class_list=["btn", "btn-primary"],
                    inner_text="Login", aria_role="button", input_type="submit",
                    attributes={"name": "submit", "data-testid": "auth-submit"},
                    parent_tag="form", parent_id="loginForm",
                    bounding_box=BoundingBox(x=200, y=400, width=120, height=40)
                ),
                CandidateElement(
                    tag_name="button", element_id="btnB", class_list=["btn", "btn-primary"],
                    inner_text="Login", aria_role="button", input_type="submit",
                    attributes={"name": "submit", "data-testid": "auth-submit"},
                    parent_tag="form", parent_id="loginForm",
                    bounding_box=BoundingBox(x=202, y=402, width=120, height=40)
                )
            ],
            expected_outcome="REJECT"  # Margin is ~0.0, must reject as ambiguous!
        ),
        # 8. Unrelated Action Button ("Cancel")
        BenchmarkScenario(
            name="Unrelated Action Button ('Cancel')",
            baseline=base,
            candidates=[
                CandidateElement(
                    tag_name="button", element_id="cancelBtn", class_list=["btn-danger"],
                    inner_text="Cancel", aria_role="button",
                    bounding_box=BoundingBox(x=50, y=400, width=80, height=40)
                )
            ],
            expected_outcome="REJECT"
        ),
    ]

    tp = 0  # Expected HEAL, Got HEAL
    fp = 0  # Expected REJECT, Got HEAL
    tn = 0  # Expected REJECT, Got REJECT
    fn = 0  # Expected HEAL, Got REJECT
    latencies = []

    print("\n" + "="*70)
    print("      SELF-HEALING FRAMEWORK BENCHMARK & EVALUATION")
    print("="*70)

    for sc in scenarios:
        t0 = time.perf_counter()
        ranked = scorer.rank_candidates(sc.baseline, sc.candidates)
        decision = decision_engine.evaluate(sc.baseline.target_key, sc.baseline.original_selector, ranked)
        elapsed_ms = (time.perf_counter() - t0) * 1000
        latencies.append(elapsed_ms)

        is_healed = decision.decision == DecisionStatus.APPROVED
        actual_outcome = "HEAL" if is_healed else "REJECT"

        if sc.expected_outcome == "HEAL":
            if actual_outcome == "HEAL":
                tp += 1
                status_icon = "PASS (TP)"
            else:
                fn += 1
                status_icon = "FAIL (FN)"
        else:  # Expected REJECT
            if actual_outcome == "REJECT":
                tn += 1
                status_icon = "PASS (TN)"
            else:
                fp += 1
                status_icon = "FALSE POSITIVE (FP)"

        top_score = decision.similarity_score or (ranked[0].total_score if ranked else 0.0)
        print(f"[{status_icon}] {sc.name}")
        print(f"       Outcome: {actual_outcome} (Expected: {sc.expected_outcome}) | Top Score: {top_score:.4f} | Latency: {elapsed_ms:.2f} ms")

    precision = tp / (tp + fp) if (tp + fp) > 0 else 1.0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 1.0
    fpr = fp / (fp + tn) if (fp + tn) > 0 else 0.0
    accuracy = (tp + tn) / len(scenarios)
    avg_latency = sum(latencies) / len(latencies)

    print("\n" + "-"*70)
    print("                    EVALUATION METRICS")
    print("-"*70)
    print(f" Total Evaluation Scenarios : {len(scenarios)}")
    print(f" True Positives (TP)        : {tp}")
    print(f" True Negatives (TN)        : {tn}")
    print(f" False Positives (FP)       : {fp}  (Target: < 5%)")
    print(f" False Negatives (FN)       : {fn}")
    print(f" Healing Precision          : {precision*100:.2f}%")
    print(f" Healing Recall             : {recall*100:.2f}%")
    print(f" False Positive Rate (FPR)  : {fpr*100:.2f}%")
    print(f" Overall Accuracy           : {accuracy*100:.2f}%")
    print(f" Average Algorithm Latency  : {avg_latency:.2f} ms")
    print("="*70 + "\n")

    return {
        "precision": precision,
        "recall": recall,
        "fpr": fpr,
        "accuracy": accuracy,
        "avg_latency": avg_latency
    }


if __name__ == "__main__":
    run_benchmark()
