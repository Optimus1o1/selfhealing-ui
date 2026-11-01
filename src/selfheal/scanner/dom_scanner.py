from pathlib import Path
from typing import Any, TYPE_CHECKING
from pydantic import BaseModel, Field
from selfheal.baseline.fingerprint import BoundingBox

if TYPE_CHECKING:
    from playwright.sync_api import Page


class CandidateElement(BaseModel):
    tag_name: str
    element_id: str = ""
    class_list: list[str] = Field(default_factory=list)
    inner_text: str = ""
    aria_role: str = ""
    accessible_name: str = ""
    input_type: str = ""
    attributes: dict[str, str] = Field(default_factory=dict)
    parent_tag: str = ""
    parent_id: str = ""
    parent_classes: list[str] = Field(default_factory=list)
    children_count: int = 0
    children_tags: list[str] = Field(default_factory=list)
    bounding_box: BoundingBox = Field(default_factory=BoundingBox)
    generated_selector: str = ""


class DOMScanner:
    def __init__(self):
        js_file = Path(__file__).parent / "dom_extractor.js"
        with open(js_file, "r", encoding="utf-8") as f:
            self.extractor_script = f.read()

    def scan(self, page: "Page", max_candidates: int = 100) -> list[CandidateElement]:
        """
        Executes DOM extraction in the browser context and returns candidate elements.
        """
        raw_candidates: list[dict[str, Any]] = page.evaluate(self.extractor_script)
        candidates = []
        for raw in raw_candidates[:max_candidates]:
            box_data = raw.get("bounding_box", {})
            box = BoundingBox(
                x=box_data.get("x", 0.0),
                y=box_data.get("y", 0.0),
                width=box_data.get("width", 0.0),
                height=box_data.get("height", 0.0),
            )
            candidate = CandidateElement(
                tag_name=raw.get("tag_name", ""),
                element_id=raw.get("element_id", ""),
                class_list=raw.get("class_list", []),
                inner_text=raw.get("inner_text", ""),
                aria_role=raw.get("aria_role", ""),
                accessible_name=raw.get("accessible_name", ""),
                input_type=raw.get("input_type", ""),
                attributes=raw.get("attributes", {}),
                parent_tag=raw.get("parent_tag", ""),
                parent_id=raw.get("parent_id", ""),
                parent_classes=raw.get("parent_classes", []),
                children_count=raw.get("children_count", 0),
                children_tags=raw.get("children_tags", []),
                bounding_box=box,
                generated_selector=raw.get("generated_selector", ""),
            )
            candidates.append(candidate)
        return candidates
