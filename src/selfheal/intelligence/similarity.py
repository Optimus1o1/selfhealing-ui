import math
from typing import Sequence
from rapidfuzz.distance import JaroWinkler
from rapidfuzz import fuzz
from selfheal.baseline.fingerprint import ElementFingerprint, BoundingBox
from selfheal.scanner.dom_scanner import CandidateElement


# Common UI Semantic Equivalence Sets (Deterministic UI ontology)
UI_SYNONYM_SETS = [
    {"login", "sign in", "log in", "signin", "authenticate"},
    {"register", "sign up", "signup", "create account", "join"},
    {"submit", "confirm", "send", "save", "apply", "commit", "done", "continue", "proceed", "next"},
    {"cancel", "dismiss", "close", "abort", "exit"},
    {"search", "find", "query", "lookup"},
    {"delete", "remove", "trash", "discard", "destroy"},
    {"edit", "modify", "update", "change"},
    {"add", "new", "create", "insert"},
    {"back", "prev", "previous", "return"},
    {"ok", "accept", "agree", "yes"},
]


def check_ui_synonym(text_a: str, text_b: str) -> float:
    a_norm = text_a.strip().lower()
    b_norm = text_b.strip().lower()
    if not a_norm or not b_norm:
        return 0.0
    if a_norm == b_norm:
        return 1.0
    for syn_set in UI_SYNONYM_SETS:
        if a_norm in syn_set and b_norm in syn_set:
            return 0.92
    return 0.0


def compute_text_similarity(baseline_text: str, candidate_text: str, baseline_acc_name: str = "", candidate_acc_name: str = "") -> float:
    """
    Computes text similarity combining visible text, UI synonyms, and accessible name
    using Jaro-Winkler and token sort ratio.
    """
    base_t = (baseline_text or "").strip().lower()
    cand_t = (candidate_text or "").strip().lower()

    # Also factor in accessible name if available
    base_acc = (baseline_acc_name or "").strip().lower()
    cand_acc = (candidate_acc_name or "").strip().lower()

    if not base_t and not cand_t and not base_acc and not cand_acc:
        return 1.0

    scores = []
    if base_t and cand_t:
        syn_score = check_ui_synonym(base_t, cand_t)
        jw = JaroWinkler.similarity(base_t, cand_t)
        ts = fuzz.token_sort_ratio(base_t, cand_t) / 100.0
        fuzzy_score = 0.6 * jw + 0.4 * ts
        scores.append(max(syn_score, fuzzy_score))

    if base_acc and cand_acc:
        syn_acc = check_ui_synonym(base_acc, cand_acc)
        jw_acc = JaroWinkler.similarity(base_acc, cand_acc)
        scores.append(max(syn_acc, jw_acc))

    # Cross-match if text was moved to aria-label or vice-versa
    if base_t and cand_acc:
        syn_cross1 = check_ui_synonym(base_t, cand_acc)
        scores.append(max(syn_cross1, JaroWinkler.similarity(base_t, cand_acc)))
    if base_acc and cand_t:
        syn_cross2 = check_ui_synonym(base_acc, cand_t)
        scores.append(max(syn_cross2, JaroWinkler.similarity(base_acc, cand_t)))

    return max(scores) if scores else 0.0


def compute_type_and_role_similarity(base: ElementFingerprint, cand: CandidateElement) -> float:
    """
    Computes similarity based on HTML tag, input type, and ARIA role.
    """
    score = 0.0
    # Tag match (0.5 max)
    if base.tag_name.lower() == cand.tag_name.lower():
        score += 0.5
    elif {base.tag_name.lower(), cand.tag_name.lower()} <= {"button", "a", "input"}:
        # Buttons and anchor tags or submit inputs often serve identical UI actions
        score += 0.25

    # Role match (0.3 max)
    if base.aria_role and cand.aria_role:
        if base.aria_role.lower() == cand.aria_role.lower():
            score += 0.3
    elif not base.aria_role and not cand.aria_role:
        # Both lack explicit role, implicit role is identical
        score += 0.3

    # Input type match (0.2 max)
    if base.input_type and cand.input_type:
        if base.input_type.lower() == cand.input_type.lower():
            score += 0.2
    elif not base.input_type and not cand.input_type:
        score += 0.2

    return min(1.0, score)


def jaccard_similarity(set_a: set, set_b: set) -> float:
    if not set_a and not set_b:
        return 1.0
    if not set_a or not set_b:
        return 0.0
    intersection = len(set_a & set_b)
    union = len(set_a | set_b)
    return intersection / union if union > 0 else 0.0


def compute_attributes_similarity(base_attrs: dict[str, str], cand_attrs: dict[str, str]) -> float:
    """
    Calculates similarity across attribute names and key-value pairs,
    accounting for new attributes added during refactoring (overlap coefficient).
    """
    base_pairs = {f"{k}={v}" for k, v in base_attrs.items()}
    cand_pairs = {f"{k}={v}" for k, v in cand_attrs.items()}

    if not base_pairs and not cand_pairs:
        return 1.0

    key_jaccard = jaccard_similarity(set(base_attrs.keys()), set(cand_attrs.keys()))
    pair_jaccard = jaccard_similarity(base_pairs, cand_pairs)

    # Overlap coefficient: measures preservation of baseline attributes in candidate
    overlap = len(base_pairs & cand_pairs) / len(base_pairs) if base_pairs else 1.0

    pair_score = 0.5 * pair_jaccard + 0.5 * overlap
    return 0.3 * key_jaccard + 0.7 * pair_score


def compute_parent_similarity(base: ElementFingerprint, cand: CandidateElement) -> float:
    """
    Compares parent container tag, ID, and class overlap.
    """
    tag_score = 1.0 if base.parent_tag.lower() == cand.parent_tag.lower() else 0.0

    id_score = 0.5  # Neutral default if either side lacks an ID
    if base.parent_id and cand.parent_id:
        id_score = JaroWinkler.similarity(base.parent_id.lower(), cand.parent_id.lower())

    class_score = jaccard_similarity(set(base.parent_classes), set(cand.parent_classes))

    return 0.4 * tag_score + 0.3 * id_score + 0.3 * class_score


def compute_children_similarity(base: ElementFingerprint, cand: CandidateElement) -> float:
    """
    Compares children tag distribution and count.
    """
    if base.children_count == 0 and cand.children_count == 0:
        return 1.0

    count_diff = abs(base.children_count - cand.children_count)
    max_count = max(base.children_count, cand.children_count, 1)
    count_score = max(0.0, 1.0 - (count_diff / max_count))

    tag_score = jaccard_similarity(set(base.children_tags), set(cand.children_tags))

    return 0.5 * count_score + 0.5 * tag_score


def compute_position_similarity(base_box: BoundingBox, cand_box: BoundingBox, viewport_diag: float = 1920.0) -> float:
    """
    Calculates geometric proximity of bounding box centers normalized to viewport diagonal.
    """
    bx, by = base_box.center
    cx, cy = cand_box.center

    dist = math.sqrt((bx - cx) ** 2 + (by - cy) ** 2)
    normalized_dist = min(dist / viewport_diag, 1.0)
    return max(0.0, 1.0 - normalized_dist)
