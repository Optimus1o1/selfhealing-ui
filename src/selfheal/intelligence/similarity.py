import math
from typing import Sequence, Union
from rapidfuzz.distance import JaroWinkler, Levenshtein
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


def check_synonym_word(w1: str, w2: str) -> float:
    if w1 == w2:
        return 1.0
    for s in UI_SYNONYM_SETS:
        if w1 in s and w2 in s:
            return 0.95
    return 0.0


def check_ui_synonym(text_a: str, text_b: str) -> float:
    a_norm = text_a.strip().lower()
    b_norm = text_b.strip().lower()
    if not a_norm or not b_norm:
        return 0.0
    if a_norm == b_norm:
        return 1.0
    for syn_set in UI_SYNONYM_SETS:
        if a_norm in syn_set and b_norm in syn_set:
            return 0.95

    # Check multi-word phrase synonym replacement
    t1 = a_norm.split()
    t2 = b_norm.split()
    if len(t1) == len(t2) and len(t1) > 1:
        scores = [check_synonym_word(w1, w2) for w1, w2 in zip(t1, t2)]
        if all(s >= 0.90 for s in scores):
            return sum(scores) / len(scores)

    return 0.0


def compute_text_similarity(baseline_text: str, candidate_text: str, baseline_acc_name: str = "", candidate_acc_name: str = "") -> float:
    """
    Computes text similarity combining visible text, UI synonyms, and accessible name
    using Levenshtein, Jaro-Winkler, and token sort ratio.
    """
    base_t = (baseline_text or "").strip().lower()
    cand_t = (candidate_text or "").strip().lower()
    base_acc = (baseline_acc_name or "").strip().lower()
    cand_acc = (candidate_acc_name or "").strip().lower()

    if not base_t and not cand_t and not base_acc and not cand_acc:
        return 1.0

    def pair_sim(s1: str, s2: str) -> float:
        if not s1 or not s2:
            return 0.0
        if s1 == s2:
            return 1.0
        syn = check_ui_synonym(s1, s2)
        if syn > 0:
            return syn
        jw = JaroWinkler.similarity(s1, s2)
        lev = Levenshtein.normalized_similarity(s1, s2)
        ts = fuzz.token_sort_ratio(s1, s2) / 100.0
        fuzzy = 0.40 * lev + 0.30 * jw + 0.30 * ts

        # Distinguishing keyword mismatch check
        t1, t2 = s1.split(), s2.split()
        if len(t1) > 1 and len(t2) > 1 and t1[-1] != t2[-1]:
            if check_synonym_word(t1[-1], t2[-1]) == 0.0:
                fuzzy = min(fuzzy, 0.70)
        return fuzzy

    scores = []
    if base_t and cand_t:
        scores.append(pair_sim(base_t, cand_t))
    if base_acc and cand_acc:
        scores.append(pair_sim(base_acc, cand_acc))
    if base_t and cand_acc:
        scores.append(pair_sim(base_t, cand_acc))
    if base_acc and cand_t:
        scores.append(pair_sim(base_acc, cand_t))

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
        # Buttons, anchor tags, and submit inputs often serve identical UI actions
        score += 0.25

    # Role match (0.3 max)
    if base.aria_role and cand.aria_role:
        if base.aria_role.lower() == cand.aria_role.lower():
            score += 0.3
    elif not base.aria_role and not cand.aria_role:
        # Both lack explicit role, implicit role is identical
        score += 0.3

    # Input type match (0.2 max)
    if base.tag_name.lower() == "input" or cand.tag_name.lower() == "input":
        if base.input_type and cand.input_type:
            if base.input_type.lower() == cand.input_type.lower():
                score += 0.2
        elif not base.input_type and not cand.input_type:
            score += 0.2
    else:
        # Non-input elements match type inherently
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


def extract_attribute_keys_and_pairs(el: Union[ElementFingerprint, CandidateElement, dict[str, str]]) -> tuple[set[str], set[str]]:
    if isinstance(el, dict):
        keys = {k.lower() for k in el.keys()}
        pairs = {f"{k.lower()}={str(v).lower()}" for k, v in el.items()}
        return keys, pairs

    keys = set()
    pairs = set()
    if getattr(el, "element_id", ""):
        keys.add("id")
        pairs.add(f"id={el.element_id.lower()}")
    if getattr(el, "class_list", []):
        keys.add("class")
        for c in el.class_list:
            if c:
                pairs.add(f"class={c.lower()}")
    for k, v in getattr(el, "attributes", {}).items():
        k_lower = k.lower()
        if k_lower not in ("id", "class"):
            keys.add(k_lower)
            pairs.add(f"{k_lower}={str(v).lower()}")

    return keys, pairs


def compute_attributes_similarity(
    base: Union[ElementFingerprint, dict[str, str]],
    cand: Union[CandidateElement, dict[str, str]]
) -> float:
    """
    Calculates similarity across element attributes, IDs, and classes,
    accounting for attribute evolution and additions during refactoring.
    """
    base_keys, base_pairs = extract_attribute_keys_and_pairs(base)
    cand_keys, cand_pairs = extract_attribute_keys_and_pairs(cand)

    if not base_keys and not cand_keys:
        return 1.0 if (isinstance(base, dict) and isinstance(cand, dict)) else 0.5

    key_jaccard = jaccard_similarity(base_keys, cand_keys)
    pair_jaccard = jaccard_similarity(base_pairs, cand_pairs)
    overlap = len(base_pairs & cand_pairs) / len(base_pairs) if base_pairs else 0.5

    pair_score = 0.5 * pair_jaccard + 0.5 * overlap
    return 0.3 * key_jaccard + 0.7 * pair_score


def compute_parent_similarity(base: ElementFingerprint, cand: CandidateElement) -> float:
    """
    Compares parent container tag, ID, and class overlap.
    """
    tag_match = (base.parent_tag.lower() == cand.parent_tag.lower()) and bool(base.parent_tag)
    tag_score = 1.0 if tag_match else (0.5 if not base.parent_tag and not cand.parent_tag else 0.0)

    if base.parent_id and cand.parent_id:
        id_score = JaroWinkler.similarity(base.parent_id.lower(), cand.parent_id.lower())
    elif not base.parent_id and not cand.parent_id:
        id_score = 1.0 if tag_match else 0.0
    else:
        id_score = 0.0

    if base.parent_classes or cand.parent_classes:
        class_score = jaccard_similarity(set(base.parent_classes), set(cand.parent_classes))
    else:
        class_score = 1.0 if tag_match else 0.0

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
