from typing import Optional, Any
from pydantic import BaseModel, Field
import json


class BoundingBox(BaseModel):
    x: float = 0.0
    y: float = 0.0
    width: float = 0.0
    height: float = 0.0

    @property
    def center(self) -> tuple[float, float]:
        return (self.x + self.width / 2.0, self.y + self.height / 2.0)


class ElementFingerprint(BaseModel):
    target_key: str
    version: int = 1
    status: str = "active"  # active, pending_review, rejected, archived
    tag_name: str = ""
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
    page_url: str = ""
    original_selector: str = ""
    screenshot_path: Optional[str] = None

    @classmethod
    def sanitize_attributes(cls, raw_attrs: dict[str, Any]) -> dict[str, str]:
        """
        Sanitize attributes to protect user privacy.
        Never store raw password values, auth tokens, or private credentials.
        """
        sanitized = {}
        sensitive_keys = {
            "value", "password", "token", "secret", "auth", "session",
            "credential", "credit_card", "cvv", "apikey", "api_key"
        }
        for k, v in raw_attrs.items():
            k_lower = k.lower()
            if any(s in k_lower for s in sensitive_keys) and k_lower != "type":
                continue
            if v is not None:
                sanitized[k] = str(v).strip()
        return sanitized

    def to_db_row(self) -> dict[str, Any]:
        # Redact inner_text for password inputs as safety defense-in-depth
        safe_inner_text = "" if self.input_type == "password" else self.inner_text
        return {
            "target_key": self.target_key,
            "version": self.version,
            "status": self.status,
            "tag_name": self.tag_name,
            "element_id": self.element_id,
            "class_list": json.dumps(self.class_list),
            "inner_text": safe_inner_text,
            "aria_role": self.aria_role,
            "accessible_name": self.accessible_name,
            "input_type": self.input_type,
            "attributes_json": json.dumps(self.attributes),
            "parent_tag": self.parent_tag,
            "parent_id": self.parent_id,
            "parent_classes": json.dumps(self.parent_classes),
            "children_count": self.children_count,
            "children_tags": json.dumps(self.children_tags),
            "bounding_box_x": self.bounding_box.x,
            "bounding_box_y": self.bounding_box.y,
            "bounding_box_width": self.bounding_box.width,
            "bounding_box_height": self.bounding_box.height,
            "page_url": self.page_url,
            "original_selector": self.original_selector,
            "screenshot_path": self.screenshot_path,
        }

    @classmethod
    def from_db_row(cls, row: dict[str, Any]) -> "ElementFingerprint":
        return cls(
            target_key=row["target_key"],
            version=row.get("version", 1),
            status=row.get("status", "active"),
            tag_name=row.get("tag_name") or "",
            element_id=row.get("element_id") or "",
            class_list=json.loads(row.get("class_list") or "[]"),
            inner_text=row.get("inner_text") or "",
            aria_role=row.get("aria_role") or "",
            accessible_name=row.get("accessible_name") or "",
            input_type=row.get("input_type") or "",
            attributes=json.loads(row.get("attributes_json") or "{}"),
            parent_tag=row.get("parent_tag") or "",
            parent_id=row.get("parent_id") or "",
            parent_classes=json.loads(row.get("parent_classes") or "[]"),
            children_count=row.get("children_count") or 0,
            children_tags=json.loads(row.get("children_tags") or "[]"),
            bounding_box=BoundingBox(
                x=row.get("bounding_box_x") or 0.0,
                y=row.get("bounding_box_y") or 0.0,
                width=row.get("bounding_box_width") or 0.0,
                height=row.get("bounding_box_height") or 0.0,
            ),
            page_url=row.get("page_url") or "",
            original_selector=row.get("original_selector") or "",
            screenshot_path=row.get("screenshot_path"),
        )

