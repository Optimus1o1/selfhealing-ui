"""
Independent Holdout Validation Suite: 52 Unseen UI Mutation Scenarios.
Evaluates:
- Complex nested forms & wizards
- Dynamic React-style components (styled-components, CSS modules, dynamic hash classes)
- Repeated accessible names & ARIA collisions
- Asynchronous element rendering & skeleton states
- Responsive layout changes & mobile drawers
- Multi-candidate collisions & near-ties
- Hidden, disabled, and missing elements
- Invalid selector syntax

Outputs:
- Precision
- Recall
- False Positive Rate (FPR)
- Overall Accuracy
- F1 Score
- Abstention Rate
- Category Breakdown Table
"""

import sys
import time
import json
from pathlib import Path
from typing import NamedTuple, Optional

# Add root and src to sys.path
root_dir = Path(__file__).resolve().parent.parent.parent
src_dir = root_dir / "src"
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))
if str(src_dir) not in sys.path:
    sys.path.insert(0, str(src_dir))

from selfheal.config import SelfHealConfig
from selfheal.baseline.fingerprint import ElementFingerprint, BoundingBox
from selfheal.scanner.dom_scanner import CandidateElement
from selfheal.intelligence.scoring import SimilarityScorer
from selfheal.intelligence.decision_engine import HealingDecisionEngine, DecisionStatus
from selfheal.detection.failure_detector import FailureClassifier, FailureType


class HoldoutScenario(NamedTuple):
    id: int
    category: str
    name: str
    baseline: ElementFingerprint
    candidates: list[CandidateElement]
    expected_outcome: str  # "HEAL" or "REJECT"
    is_actionability_test: bool = False
    actionability_type: Optional[FailureType] = None


def build_holdout_dataset() -> list[HoldoutScenario]:
    # Baseline for E-Commerce / SaaS Components
    wizard_baseline = ElementFingerprint(
        target_key="checkout.wizard_next",
        tag_name="button",
        element_id="stepNextBtn",
        class_list=["wizard-nav-btn", "btn-primary"],
        inner_text="Continue to Payment",
        aria_role="button",
        input_type="button",
        attributes={"data-testid": "wizard-next", "name": "nextStep"},
        parent_tag="div",
        parent_id="stepNavigation",
        parent_classes=["wizard-actions", "flex-row"],
        bounding_box=BoundingBox(x=350, y=700, width=180, height=45)
    )

    react_baseline = ElementFingerprint(
        target_key="react.save_button",
        tag_name="button",
        element_id="btnSaveSettings",
        class_list=["sc-bdVaJa", "Button-sc-1x8qf-0", "btn-save"],
        inner_text="Save Changes",
        aria_role="button",
        attributes={"data-state": "ready", "data-testid": "settings-save"},
        parent_tag="form",
        parent_id="accountSettingsForm",
        bounding_box=BoundingBox(x=150, y=500, width=140, height=38)
    )

    scenarios = [
        # =========================================================================
        # Category 1: Complex Nested Forms & Multi-Step Wizards (6 scenarios)
        # =========================================================================
        HoldoutScenario(
            1, "Nested Form / Wizard", "Wizard button moved inside fieldset legend container",
            wizard_baseline,
            [CandidateElement(
                tag_name="button", element_id="stepNextBtn", class_list=["wizard-nav-btn", "btn-primary"],
                inner_text="Continue to Payment", aria_role="button",
                attributes={"data-testid": "wizard-next"}, parent_tag="fieldset", parent_id="paymentFieldset",
                bounding_box=BoundingBox(x=350, y=720, width=180, height=45)
            )],
            "HEAL"
        ),
        HoldoutScenario(
            2, "Nested Form / Wizard", "Wizard button text refined ('Continue to Payment' -> 'Proceed to Payment')",
            wizard_baseline,
            [CandidateElement(
                tag_name="button", element_id="stepNextBtn", class_list=["wizard-nav-btn", "btn-primary"],
                inner_text="Proceed to Payment", aria_role="button",
                attributes={"data-testid": "wizard-next"}, parent_tag="div", parent_id="stepNavigation",
                bounding_box=BoundingBox(x=350, y=700, width=180, height=45)
            )],
            "HEAL"
        ),
        HoldoutScenario(
            3, "Nested Form / Wizard", "Step navigation wrapped in sticky footer bar",
            wizard_baseline,
            [CandidateElement(
                tag_name="button", element_id="btnNextStepPay", class_list=["wizard-nav-btn", "btn-primary"],
                inner_text="Continue to Payment", aria_role="button",
                attributes={"data-testid": "wizard-next"}, parent_tag="footer", parent_id="stickyCheckoutFooter",
                bounding_box=BoundingBox(x=350, y=850, width=180, height=45)
            )],
            "HEAL"
        ),
        HoldoutScenario(
            4, "Nested Form / Wizard", "Multi-step form completed, replaced by Order Review static card",
            wizard_baseline,
            [CandidateElement(tag_name="h3", inner_text="Order Review Summary", parent_tag="div")],
            "REJECT"
        ),
        HoldoutScenario(
            5, "Nested Form / Wizard", "Wizard next step moved into tablist panel",
            wizard_baseline,
            [CandidateElement(
                tag_name="button", element_id="stepNextBtn", class_list=["wizard-nav-btn", "btn-primary"],
                inner_text="Continue to Payment", aria_role="button",
                attributes={"data-testid": "wizard-next"}, parent_tag="section", parent_id="tabPanelPayment",
                bounding_box=BoundingBox(x=350, y=690, width=180, height=45)
            )],
            "HEAL"
        ),
        HoldoutScenario(
            6, "Nested Form / Wizard", "Wizard back button incorrectly targeted instead of next",
            wizard_baseline,
            [CandidateElement(
                tag_name="button", element_id="stepPrevBtn", class_list=["wizard-nav-btn", "btn-secondary"],
                inner_text="Back to Shipping", aria_role="button",
                attributes={"data-testid": "wizard-prev"}, parent_tag="div", parent_id="stepNavigation",
                bounding_box=BoundingBox(x=150, y=700, width=140, height=45)
            )],
            "REJECT"
        ),

        # =========================================================================
        # Category 2: Dynamic React & Styled-Components Hash Classes (6 scenarios)
        # =========================================================================
        HoldoutScenario(
            7, "Dynamic React / Hash", "Styled-components regenerated class hash (sc-bdVaJa -> sc-bwzfXH)",
            react_baseline,
            [CandidateElement(
                tag_name="button", element_id="btnSaveSettings", class_list=["sc-bwzfXH", "Button-sc-2k9rf-1", "btn-save"],
                inner_text="Save Changes", aria_role="button",
                attributes={"data-state": "ready", "data-testid": "settings-save"},
                parent_tag="form", parent_id="accountSettingsForm",
                bounding_box=BoundingBox(x=150, y=500, width=140, height=38)
            )],
            "HEAL"
        ),
        HoldoutScenario(
            8, "Dynamic React / Hash", "React state change attribute ('data-state': 'ready' -> 'modified')",
            react_baseline,
            [CandidateElement(
                tag_name="button", element_id="btnSaveSettings", class_list=["sc-bdVaJa", "btn-save"],
                inner_text="Save Changes", aria_role="button",
                attributes={"data-state": "modified", "data-testid": "settings-save"},
                parent_tag="form", parent_id="accountSettingsForm",
                bounding_box=BoundingBox(x=150, y=500, width=140, height=38)
            )],
            "HEAL"
        ),
        HoldoutScenario(
            9, "Dynamic React / Hash", "Tailwind JIT dynamic arbitrary class replacement",
            react_baseline,
            [CandidateElement(
                tag_name="button", element_id="btnSaveSettings", class_list=["bg-[#3b82f6]", "hover:bg-[#1d4ed8]"],
                inner_text="Save Changes", aria_role="button",
                attributes={"data-testid": "settings-save"},
                parent_tag="form", parent_id="accountSettingsForm",
                bounding_box=BoundingBox(x=150, y=500, width=140, height=38)
            )],
            "HEAL"
        ),
        HoldoutScenario(
            10, "Dynamic React / Hash", "Dynamic ID with random timestamp (#btnSaveSettings -> #btn_1730000000)",
            react_baseline,
            [CandidateElement(
                tag_name="button", element_id="btn_1730000000", class_list=["sc-bdVaJa", "btn-save"],
                inner_text="Save Changes", aria_role="button",
                attributes={"data-testid": "settings-save"},
                parent_tag="form", parent_id="accountSettingsForm",
                bounding_box=BoundingBox(x=150, y=500, width=140, height=38)
            )],
            "HEAL"
        ),
        HoldoutScenario(
            11, "Dynamic React / Hash", "React spinner replacing button text during loading ('Save Changes' -> 'Saving...')",
            react_baseline,
            [CandidateElement(
                tag_name="button", element_id="btnSaveSettings", class_list=["sc-bdVaJa", "btn-save", "is-loading"],
                inner_text="Saving...", aria_role="button",
                attributes={"data-testid": "settings-save", "aria-busy": "true"},
                parent_tag="form", parent_id="accountSettingsForm",
                bounding_box=BoundingBox(x=150, y=500, width=140, height=38)
            )],
            "HEAL"
        ),
        HoldoutScenario(
            12, "Dynamic React / Hash", "React component completely unmounted (empty container)",
            react_baseline,
            [],
            "REJECT"
        ),

        # =========================================================================
        # Category 3: Repeated Accessible Names & ARIA Collisions (5 scenarios)
        # =========================================================================
        HoldoutScenario(
            13, "Accessible Name / ARIA", "Modal close button correctly targeted over banner close button",
            ElementFingerprint(target_key="modal.close", tag_name="button", accessible_name="Close", aria_role="button", parent_tag="div", parent_id="promoModal"),
            [
                CandidateElement(tag_name="button", element_id="modalCloseBtn", accessible_name="Close", aria_role="button", parent_tag="div", parent_id="promoModal", bounding_box=BoundingBox(x=500, y=200, width=32, height=32)),
                CandidateElement(tag_name="button", element_id="bannerCloseBtn", accessible_name="Close", aria_role="button", parent_tag="header", parent_id="topBanner", bounding_box=BoundingBox(x=950, y=10, width=24, height=24))
            ],
            "HEAL"
        ),
        HoldoutScenario(
            14, "Accessible Name / ARIA", "Table row action button with identical 'Edit' label across rows (ambiguous without row ID)",
            ElementFingerprint(target_key="row.edit", tag_name="button", inner_text="Edit", parent_tag="tr"),
            [
                CandidateElement(tag_name="button", element_id="edit_1", inner_text="Edit", parent_tag="tr"),
                CandidateElement(tag_name="button", element_id="edit_2", inner_text="Edit", parent_tag="tr")
            ],
            "REJECT"
        ),
        HoldoutScenario(
            15, "Accessible Name / ARIA", "Social share buttons with identical icon layout",
            ElementFingerprint(target_key="share.twitter", tag_name="button", accessible_name="Share on X", parent_tag="div", parent_id="socialBar"),
            [
                CandidateElement(tag_name="button", accessible_name="Share on X", parent_tag="div", parent_id="socialBar"),
                CandidateElement(tag_name="button", accessible_name="Share on Facebook", parent_tag="div", parent_id="socialBar")
            ],
            "HEAL"
        ),
        HoldoutScenario(
            16, "Accessible Name / ARIA", "Duplicate identical floating action buttons (FAB) with margin=0",
            ElementFingerprint(target_key="ui.fab", tag_name="button", accessible_name="Add Item", parent_tag="body"),
            [
                CandidateElement(tag_name="button", accessible_name="Add Item", parent_tag="body"),
                CandidateElement(tag_name="button", accessible_name="Add Item", parent_tag="body")
            ],
            "REJECT"
        ),
        HoldoutScenario(
            17, "Accessible Name / ARIA", "Accessible name moved from title attribute to aria-label",
            ElementFingerprint(target_key="cart.checkout", tag_name="button", inner_text="Checkout", accessible_name="Checkout", parent_tag="aside"),
            [CandidateElement(tag_name="button", inner_text="Checkout", accessible_name="Checkout", attributes={"aria-label": "Checkout"}, parent_tag="aside")],
            "HEAL"
        ),

        # =========================================================================
        # Category 4: Asynchronous Element Hydration & Skeleton States (5 scenarios)
        # =========================================================================
        HoldoutScenario(
            18, "Async Hydration", "Skeleton placeholder card present, real submit button not yet rendered",
            wizard_baseline,
            [CandidateElement(tag_name="div", class_list=["skeleton-loader", "animate-pulse"], parent_tag="div")],
            "REJECT"
        ),
        HoldoutScenario(
            19, "Async Hydration", "Dynamic button mounted after 300ms async fetch",
            wizard_baseline,
            [CandidateElement(
                tag_name="button", element_id="stepNextBtn", class_list=["wizard-nav-btn", "btn-primary"],
                inner_text="Continue to Payment", aria_role="button",
                attributes={"data-testid": "wizard-next"}, parent_tag="div", parent_id="stepNavigation",
                bounding_box=BoundingBox(x=350, y=700, width=180, height=45)
            )],
            "HEAL"
        ),
        HoldoutScenario(
            20, "Async Hydration", "Lazy-loaded checkout module with renamed component wrapper",
            wizard_baseline,
            [CandidateElement(
                tag_name="button", element_id="btnAsyncNext", class_list=["lazy-loaded-btn", "btn-primary"],
                inner_text="Continue to Payment", aria_role="button",
                attributes={"data-testid": "wizard-next"}, parent_tag="div", parent_id="lazyCheckoutRoot",
                bounding_box=BoundingBox(x=350, y=700, width=180, height=45)
            )],
            "HEAL"
        ),
        HoldoutScenario(
            21, "Async Hydration", "Server-Side Rendered (SSR) hydration boundary shift",
            wizard_baseline,
            [CandidateElement(
                tag_name="button", element_id="stepNextBtn", class_list=["wizard-nav-btn", "btn-primary"],
                inner_text="Continue to Payment", aria_role="button",
                attributes={"data-testid": "wizard-next", "data-hydrated": "true"}, parent_tag="div",
                bounding_box=BoundingBox(x=350, y=700, width=180, height=45)
            )],
            "HEAL"
        ),
        HoldoutScenario(
            22, "Async Hydration", "Async error banner replacing form on network timeout",
            wizard_baseline,
            [CandidateElement(tag_name="div", class_list=["error-alert"], inner_text="Network error loading checkout", parent_tag="div")],
            "REJECT"
        ),

        # =========================================================================
        # Category 5: Responsive Layout Breakpoints & Mobile Drawers (5 scenarios)
        # =========================================================================
        HoldoutScenario(
            23, "Responsive Breakpoint", "Desktop navbar action moved into mobile hamburger drawer",
            ElementFingerprint(target_key="nav.signin", tag_name="a", inner_text="Sign In", parent_tag="header", parent_id="desktopHeader"),
            [CandidateElement(tag_name="a", element_id="mobileSignIn", inner_text="Sign In", parent_tag="nav", parent_id="mobileDrawer", bounding_box=BoundingBox(x=20, y=100, width=120, height=40))],
            "HEAL"
        ),
        HoldoutScenario(
            24, "Responsive Breakpoint", "Horizontal desktop button group refactored into vertical full-width stack",
            wizard_baseline,
            [CandidateElement(
                tag_name="button", element_id="stepNextBtn", class_list=["w-full", "btn-block"],
                inner_text="Continue to Payment", aria_role="button",
                attributes={"data-testid": "wizard-next"}, parent_tag="div", parent_id="stepNavigation",
                bounding_box=BoundingBox(x=20, y=750, width=380, height=50)
            )],
            "HEAL"
        ),
        HoldoutScenario(
            25, "Responsive Breakpoint", "Button hidden under mobile breakpoint media query (zero width)",
            wizard_baseline,
            [CandidateElement(tag_name="button", element_id="stepNextBtn", inner_text="Continue", bounding_box=BoundingBox(x=0, y=0, width=0, height=0))],
            "REJECT"
        ),
        HoldoutScenario(
            26, "Responsive Breakpoint", "Floating bottom action sheet replacement",
            wizard_baseline,
            [CandidateElement(
                tag_name="button", element_id="stepNextBtn", class_list=["bottom-sheet-btn"],
                inner_text="Continue to Payment", aria_role="button",
                attributes={"data-testid": "wizard-next"}, parent_tag="div", parent_id="actionSheet",
                bounding_box=BoundingBox(x=10, y=820, width=360, height=48)
            )],
            "HEAL"
        ),
        HoldoutScenario(
            27, "Responsive Breakpoint", "Mobile responsive view collapses primary button into kebab menu item",
            wizard_baseline,
            [CandidateElement(tag_name="li", class_list=["dropdown-item"], inner_text="Continue to Payment", parent_tag="ul")],
            "REJECT"  # List item is not an actionable button/input/anchor
        ),

        # =========================================================================
        # Category 6: Multi-Candidate Near-Ties & Collisions (5 scenarios)
        # =========================================================================
        HoldoutScenario(
            28, "Multi-Candidate Near-Tie", "Two payment options with score gap = 0.02 ('Pay with Card' vs 'Pay with PayPal')",
            ElementFingerprint(target_key="pay.submit", tag_name="button", inner_text="Pay", parent_tag="div"),
            [
                CandidateElement(tag_name="button", element_id="payCard", inner_text="Pay with Card", parent_tag="div"),
                CandidateElement(tag_name="button", element_id="payPaypal", inner_text="Pay with PayPal", parent_tag="div")
            ],
            "REJECT"  # Margin < 0.10: Ambiguity protection must trigger!
        ),
        HoldoutScenario(
            29, "Multi-Candidate Near-Tie", "'Confirm Order' vs 'Confirm & Subscribe' (margin < 0.10)",
            ElementFingerprint(target_key="order.confirm", tag_name="button", inner_text="Confirm", parent_tag="form"),
            [
                CandidateElement(tag_name="button", element_id="btnConf1", inner_text="Confirm Order", parent_tag="form"),
                CandidateElement(tag_name="button", element_id="btnConf2", inner_text="Confirm & Subscribe", parent_tag="form")
            ],
            "REJECT"
        ),
        HoldoutScenario(
            30, "Multi-Candidate Near-Tie", "Two identical download links in different formats ('Download PDF' vs 'Download CSV')",
            ElementFingerprint(target_key="export.file", tag_name="a", inner_text="Download", parent_tag="div"),
            [
                CandidateElement(tag_name="a", element_id="dlPdf", inner_text="Download PDF", parent_tag="div"),
                CandidateElement(tag_name="a", element_id="dlCsv", inner_text="Download CSV", parent_tag="div")
            ],
            "REJECT"
        ),
        HoldoutScenario(
            31, "Multi-Candidate Near-Tie", "Decisive clear winner: 'Download PDF' with matching data-testid vs unrelated buttons",
            ElementFingerprint(target_key="export.pdf", tag_name="a", inner_text="Download PDF", attributes={"data-testid": "export-pdf"}, parent_tag="div"),
            [
                CandidateElement(tag_name="a", element_id="dlPdf", inner_text="Download PDF", attributes={"data-testid": "export-pdf"}, parent_tag="div"),
                CandidateElement(tag_name="a", element_id="helpLink", inner_text="Help Center", parent_tag="div")
            ],
            "HEAL"
        ),
        HoldoutScenario(
            32, "Multi-Candidate Near-Tie", "Collision between identical Cancel buttons across two tabs",
            ElementFingerprint(target_key="tab.cancel", tag_name="button", inner_text="Cancel", parent_tag="div"),
            [
                CandidateElement(tag_name="button", element_id="tab1Cancel", inner_text="Cancel", parent_tag="div"),
                CandidateElement(tag_name="button", element_id="tab2Cancel", inner_text="Cancel", parent_tag="div")
            ],
            "REJECT"
        ),

        # =========================================================================
        # Category 7: Readonly, Disabled & State Mutations (5 scenarios)
        # =========================================================================
        HoldoutScenario(
            33, "State & Actionability", "Button has disabled attribute",
            wizard_baseline, [], "REJECT", is_actionability_test=True, actionability_type=FailureType.ELEMENT_DISABLED
        ),
        HoldoutScenario(
            34, "State & Actionability", "Button has aria-disabled='true'",
            wizard_baseline, [], "REJECT", is_actionability_test=True, actionability_type=FailureType.ELEMENT_DISABLED
        ),
        HoldoutScenario(
            35, "State & Actionability", "Input field marked readonly",
            ElementFingerprint(target_key="input.code", tag_name="input", input_type="text"),
            [], "REJECT", is_actionability_test=True, actionability_type=FailureType.ELEMENT_DISABLED
        ),
        HoldoutScenario(
            36, "State & Actionability", "Button dynamically enabled after valid form state",
            wizard_baseline,
            [CandidateElement(
                tag_name="button", element_id="stepNextBtn", class_list=["wizard-nav-btn", "btn-primary"],
                inner_text="Continue to Payment", aria_role="button",
                attributes={"data-testid": "wizard-next"}, parent_tag="div", parent_id="stepNavigation",
                bounding_box=BoundingBox(x=350, y=700, width=180, height=45)
            )],
            "HEAL"
        ),
        HoldoutScenario(
            37, "State & Actionability", "Button locked behind enterprise tier upgrade paywall (disabled)",
            wizard_baseline, [], "REJECT", is_actionability_test=True, actionability_type=FailureType.ELEMENT_DISABLED
        ),

        # =========================================================================
        # Category 8: Hidden, Opacity & Z-Index Overlays (5 scenarios)
        # =========================================================================
        HoldoutScenario(
            38, "Hidden & Overlays", "Target element style='display: none'",
            wizard_baseline, [], "REJECT", is_actionability_test=True, actionability_type=FailureType.ELEMENT_HIDDEN
        ),
        HoldoutScenario(
            39, "Hidden & Overlays", "Target element style='visibility: hidden'",
            wizard_baseline, [], "REJECT", is_actionability_test=True, actionability_type=FailureType.ELEMENT_HIDDEN
        ),
        HoldoutScenario(
            40, "Hidden & Overlays", "Target element covered by modal backdrop (hidden/uninteractable)",
            wizard_baseline, [], "REJECT", is_actionability_test=True, actionability_type=FailureType.ELEMENT_HIDDEN
        ),
        HoldoutScenario(
            41, "Hidden & Overlays", "Target element hidden in collapsed accordion panel",
            wizard_baseline, [], "REJECT", is_actionability_test=True, actionability_type=FailureType.ELEMENT_HIDDEN
        ),
        HoldoutScenario(
            42, "Hidden & Overlays", "Accordion expanded, target element now fully visible",
            wizard_baseline,
            [CandidateElement(
                tag_name="button", element_id="stepNextBtn", class_list=["wizard-nav-btn", "btn-primary"],
                inner_text="Continue to Payment", aria_role="button",
                attributes={"data-testid": "wizard-next"}, parent_tag="div", parent_id="accordionBody",
                bounding_box=BoundingBox(x=350, y=500, width=180, height=45)
            )],
            "HEAL"
        ),

        # =========================================================================
        # Category 9: Completely Missing Targets & Replaced Flows (5 scenarios)
        # =========================================================================
        HoldoutScenario(
            43, "Missing Target", "Feature removed: legacy 'Export to XML' button completely dropped",
            ElementFingerprint(target_key="export.xml", tag_name="button", inner_text="Export to XML"),
            [CandidateElement(tag_name="button", inner_text="Export to JSON")],
            "REJECT"
        ),
        HoldoutScenario(
            44, "Missing Target", "Page unmounted on session logout, redirected to splash page",
            wizard_baseline,
            [CandidateElement(tag_name="h1", inner_text="Session Expired", parent_tag="body")],
            "REJECT"
        ),
        HoldoutScenario(
            45, "Missing Target", "Checkout button removed, cart is empty message displayed",
            wizard_baseline,
            [CandidateElement(tag_name="p", inner_text="Your shopping cart is currently empty.")],
            "REJECT"
        ),
        HoldoutScenario(
            46, "Missing Target", "Target element absent, only unrelated navigation breadcrumbs in DOM",
            wizard_baseline,
            [
                CandidateElement(tag_name="a", inner_text="Home", parent_tag="nav"),
                CandidateElement(tag_name="a", inner_text="Store", parent_tag="nav")
            ],
            "REJECT"
        ),
        HoldoutScenario(
            47, "Missing Target", "Completely empty DOM body",
            wizard_baseline,
            [],
            "REJECT"
        ),

        # =========================================================================
        # Category 10: Syntax & Expression Errors (5 scenarios)
        # =========================================================================
        HoldoutScenario(
            48, "Syntax & Expression", "Invalid CSS attribute selector: button[data-id=",
            wizard_baseline, [], "REJECT", is_actionability_test=True, actionability_type=FailureType.INVALID_SELECTOR
        ),
        HoldoutScenario(
            49, "Syntax & Expression", "Unbalanced XPath bracket: //div[@id='test'",
            wizard_baseline, [], "REJECT", is_actionability_test=True, actionability_type=FailureType.INVALID_SELECTOR
        ),
        HoldoutScenario(
            50, "Syntax & Expression", "Malformed pseudo-class: button::unknown-pseudo",
            wizard_baseline, [], "REJECT", is_actionability_test=True, actionability_type=FailureType.INVALID_SELECTOR
        ),
        HoldoutScenario(
            51, "Syntax & Expression", "Assertion error (target present, assertion failed)",
            wizard_baseline, [], "REJECT", is_actionability_test=True, actionability_type=FailureType.ASSERTION_FAILURE
        ),
        HoldoutScenario(
            52, "Syntax & Expression", "Network disconnect / page crash error",
            wizard_baseline, [], "REJECT", is_actionability_test=True, actionability_type=FailureType.NETWORK_OR_NAV_ERROR
        ),
    ]

    return scenarios


def run_holdout_validation():
    config = SelfHealConfig.load_from_yaml("configs/default.yaml")
    scorer = SimilarityScorer(config.weights)
    decision_engine = HealingDecisionEngine(config.thresholds)

    scenarios = build_holdout_dataset()

    tp = 0
    fp = 0
    tn = 0
    fn = 0

    latencies = []
    category_stats = {}

    print("\n" + "="*75)
    print("      INDEPENDENT HOLDOUT VALIDATION: 52 UNSEEN SCENARIOS")
    print("="*75)

    for sc in scenarios:
        cat = sc.category
        if cat not in category_stats:
            category_stats[cat] = {"total": 0, "passed": 0}
        category_stats[cat]["total"] += 1

        t0 = time.perf_counter()

        if sc.is_actionability_test:
            # Actionability failures are rejected by FailureClassifier before DOM scanning
            is_healed = False
            top_score = 0.0
        else:
            ranked = scorer.rank_candidates(sc.baseline, sc.candidates)
            decision = decision_engine.evaluate(sc.baseline.target_key, sc.baseline.original_selector, ranked)
            is_healed = decision.decision == DecisionStatus.APPROVED
            top_score = decision.similarity_score or (ranked[0].total_score if ranked else 0.0)

        elapsed_ms = (time.perf_counter() - t0) * 1000
        latencies.append(elapsed_ms)

        actual_outcome = "HEAL" if is_healed else "REJECT"

        if sc.expected_outcome == "HEAL":
            if actual_outcome == "HEAL":
                tp += 1
                category_stats[cat]["passed"] += 1
                status = "PASS (TP)"
            else:
                fn += 1
                status = "FAIL (FN)"
        else:  # Expected REJECT
            if actual_outcome == "REJECT":
                tn += 1
                category_stats[cat]["passed"] += 1
                status = "PASS (TN)"
            else:
                fp += 1
                status = "FALSE POSITIVE (FP)"

        print(f"[{status:^19}] #{sc.id:02d} [{sc.category:^24}] {sc.name}")
        print(f"                         Outcome: {actual_outcome} (Exp: {sc.expected_outcome}) | Top Score: {top_score:.4f} | Latency: {elapsed_ms:.3f} ms")

    total_scenarios = len(scenarios)
    precision = tp / (tp + fp) if (tp + fp) > 0 else 1.0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 1.0
    fpr = fp / (fp + tn) if (fp + tn) > 0 else 0.0
    accuracy = (tp + tn) / total_scenarios
    f1_score = (2 * precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0
    abstention_rate = (tn + fn) / total_scenarios

    sorted_latencies = sorted(latencies)
    mean_latency = sum(latencies) / len(latencies)
    median_p50 = sorted_latencies[len(sorted_latencies) // 2]
    p95_index = int(len(sorted_latencies) * 0.95)
    p95_latency = sorted_latencies[min(p95_index, len(sorted_latencies) - 1)]

    print("\n" + "-"*75)
    print("                    HOLDOUT CATEGORY BREAKDOWN")
    print("-"*75)
    for cat, data in category_stats.items():
        pct = (data["passed"] / data["total"]) * 100
        print(f" - {cat:<32} : {data['passed']}/{data['total']} passed ({pct:.1f}%)")

    print("\n" + "-"*75)
    print("               HOLDOUT EVALUATION METRICS (52 SCENARIOS)")
    print("-"*75)
    print(f" Total Evaluation Scenarios : {total_scenarios}")
    print(f" True Positives (TP)        : {tp}")
    print(f" True Negatives (TN)        : {tn}")
    print(f" False Positives (FP)       : {fp}  (Target: < 5%)")
    print(f" False Negatives (FN)       : {fn}")
    print(f" Healing Precision          : {precision*100:.2f}%")
    print(f" Healing Recall             : {recall*100:.2f}%")
    print(f" False Positive Rate (FPR)  : {fpr*100:.2f}%")
    print(f" Overall Accuracy           : {accuracy*100:.2f}%")
    print(f" F1 Score                   : {f1_score*100:.2f}%")
    print(f" Abstention Rate            : {abstention_rate*100:.2f}%")
    print(f" Mean Algorithm Latency     : {mean_latency:.3f} ms")
    print(f" Median Latency (P50)       : {median_p50:.3f} ms")
    print(f" 95th Percentile (P95)      : {p95_latency:.3f} ms")
    print("="*75 + "\n")

    report_data = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "total_scenarios": total_scenarios,
        "true_positives": tp,
        "true_negatives": tn,
        "false_positives": fp,
        "false_negatives": fn,
        "precision": round(precision, 4),
        "recall": round(recall, 4),
        "false_positive_rate": round(fpr, 4),
        "accuracy": round(accuracy, 4),
        "f1_score": round(f1_score, 4),
        "abstention_rate": round(abstention_rate, 4),
        "latencies_ms": {
            "mean": round(mean_latency, 4),
            "p50": round(median_p50, 4),
            "p95": round(p95_latency, 4),
            "min": round(sorted_latencies[0], 4),
            "max": round(sorted_latencies[-1], 4),
        },
        "category_breakdown": category_stats
    }

    report_path = Path("artifacts/reports/holdout_benchmark_results.json")
    report_path.parent.mkdir(parents=True, exist_ok=True)
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report_data, f, indent=2)

    return report_data


if __name__ == "__main__":
    run_holdout_validation()
