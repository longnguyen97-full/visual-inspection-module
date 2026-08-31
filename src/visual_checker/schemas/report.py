from typing import List, Optional
from pydantic import BaseModel, Field

class BoundingBox(BaseModel):
    x: int = Field(..., description="Top-left X coordinate")
    y: int = Field(..., description="Top-left Y coordinate")
    width: int = Field(..., description="Bounding box width")
    height: int = Field(..., description="Bounding box height")

    @property
    def area(self) -> int:
        return self.width * self.height

class DefectRegion(BaseModel):
    id: int
    bbox: BoundingBox
    area: int
    severity: str = Field(..., description="'critical', 'warning', or 'minor'")
    region_type: str = Field(default="general", description="'header', 'body', 'card', 'footer', etc.")

class VisualInspectionResult(BaseModel):
    has_defect: bool
    ssim_score: float
    diff_pixel_ratio: float
    defect_count: int
    defects: List[DefectRegion] = []
    agent_prompt_summary: str
    execution_time_ms: float
