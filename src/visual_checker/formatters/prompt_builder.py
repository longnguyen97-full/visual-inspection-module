from typing import List
from ..schemas.report import DefectRegion

class PromptBuilder:
    """Builds structured natural language summaries optimized for LLM Agent consumption."""

    @staticmethod
    def build_summary(
        has_defect: bool,
        ssim_score: float,
        diff_ratio: float,
        defects: List[DefectRegion]
    ) -> str:
        if not has_defect or len(defects) == 0:
            return f"[VISUAL INSPECTION PASS] No visual regression detected. SSIM Score: {ssim_score:.4f}. UI matches baseline perfectly."

        lines = [
            f"[VISUAL BUG DETECTED] Visual regression found with SSIM Index = {ssim_score:.4f} and {diff_ratio*100:.2f}% pixel discrepancy.",
            f"Total affected regions: {len(defects)}."
        ]

        for d in defects:
            b = d.bbox
            lines.append(
                f"- Region #{d.id} [{d.severity.upper()} in {d.region_type}]: "
                f"Coordinates (x={b.x}, y={b.y}, width={b.width}px, height={b.height}px, area={d.area}px). "
                f"Action required: Inspect CSS/DOM styles affecting elements inside this bounding box."
            )

        return "\n".join(lines)
