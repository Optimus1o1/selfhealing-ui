from enum import Enum
from pathlib import Path
from typing import Optional
from pydantic import BaseModel, Field
import yaml


class HealingPolicy(str, Enum):
    OBSERVE = "observe"
    ASSISTED = "assisted"
    AUTOMATIC = "automatic"


class SimilarityWeights(BaseModel):
    text: float = Field(0.30, ge=0.0, le=1.0)
    type_and_role: float = Field(0.20, ge=0.0, le=1.0)
    attributes: float = Field(0.20, ge=0.0, le=1.0)
    parent_context: float = Field(0.15, ge=0.0, le=1.0)
    children_structure: float = Field(0.10, ge=0.0, le=1.0)
    position: float = Field(0.05, ge=0.0, le=1.0)

    def normalized_weights(self) -> dict[str, float]:
        raw = {
            "text": self.text,
            "type_and_role": self.type_and_role,
            "attributes": self.attributes,
            "parent_context": self.parent_context,
            "children_structure": self.children_structure,
            "position": self.position,
        }
        total = sum(raw.values())
        if total == 0:
            return raw
        return {k: v / total for k, v in raw.items()}


class Thresholds(BaseModel):
    minimum_score: float = Field(0.85, ge=0.0, le=1.0)
    minimum_score_margin: float = Field(0.10, ge=0.0, le=1.0)
    max_candidates: int = Field(100, ge=1, le=1000)


class FrameworkSettings(BaseModel):
    project_name: str = "SelfHealing UI"
    policy: HealingPolicy = HealingPolicy.ASSISTED
    database_path: str = "artifacts/selfheal.db"
    screenshot_dir: str = "artifacts/screenshots"
    report_dir: str = "artifacts/reports"
    record_screenshots: bool = False
    grace_period_ms: int = 500
    retry_limit: int = 1


class SelfHealConfig(BaseModel):
    framework: FrameworkSettings = Field(default_factory=FrameworkSettings)
    thresholds: Thresholds = Field(default_factory=Thresholds)
    weights: SimilarityWeights = Field(default_factory=SimilarityWeights)

    @classmethod
    def load_from_yaml(cls, path: str | Path) -> "SelfHealConfig":
        file_path = Path(path)
        if not file_path.is_file():
            return cls()
        with open(file_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
        return cls(**data)
