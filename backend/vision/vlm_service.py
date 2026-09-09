from pathlib import Path

from pydantic import BaseModel, Field


class VisionAnalysis(BaseModel):
    incident_type: str
    confidence: float = Field(ge=0.0, le=1.0)
    severity: str
    summary: str
    evidence: list[str]
    recommended_action: str


class VLMService:
    """
    Vision analysis service.

    Uses a deterministic demo fallback so DroneRescue
    can operate without external VLM API credits.
    """

    def __init__(
        self,
        model: str = "demo-vision-v1",
    ):
        self.model = model

    def analyze_image(
        self,
        image_path: str,
    ) -> VisionAnalysis:

        path = Path(image_path)

        if not path.exists():
            raise FileNotFoundError(
                f"Image not found: {image_path}"
            )

        if path.suffix.lower() not in {
            ".png",
            ".jpg",
            ".jpeg",
            ".webp",
        }:
            raise ValueError(
                f"Unsupported image format: {path.suffix}"
            )

        filename = path.name.lower()

        # --------------------------------------------------
        # HIGH-CONFIDENCE FIRE DETECTION
        # --------------------------------------------------

        if "fire" in filename:
            return VisionAnalysis(
                incident_type="fire",
                confidence=0.94,
                severity="high",
                summary=(
                    "A fire incident is visible in the "
                    "drone imagery with flames and smoke."
                ),
                evidence=[
                    "Visible flames",
                    "Smoke plume detected",
                    "Structure appears affected",
                ],
                recommended_action=(
                    "Escalate emergency response and "
                    "perform thermal inspection."
                ),
            )

        # --------------------------------------------------
        # CHEMICAL LEAK DETECTION
        # --------------------------------------------------

        if "chemical_leak" in filename:
            return VisionAnalysis(
                incident_type="chemical_leak",
                confidence=0.91,
                severity="high",
                summary=(
                    "A possible hazardous chemical release "
                    "is visible near the incident area."
                ),
                evidence=[
                    "Visible vapor or spill pattern",
                    "Potential hazardous release detected",
                    "Affected area requires isolation",
                ],
                recommended_action=(
                    "Maintain safe distance and perform "
                    "remote inspection."
                ),
            )

        # --------------------------------------------------
        # INTRUSION DETECTION
        # --------------------------------------------------

        if "intrusion" in filename:
            return VisionAnalysis(
                incident_type="intrusion",
                confidence=0.89,
                severity="medium",
                summary=(
                    "A possible unauthorized person or vehicle "
                    "is visible in the monitored area."
                ),
                evidence=[
                    "Person or vehicle detected",
                    "Movement detected in restricted area",
                    "Potential unauthorized access",
                ],
                recommended_action=(
                    "Continue aerial monitoring and "
                    "track the detected subject."
                ),
            )

        # --------------------------------------------------
        # ACCIDENT DETECTION
        # --------------------------------------------------

        if "accident" in filename:
            return VisionAnalysis(
                incident_type="accident",
                confidence=0.92,
                severity="high",
                summary=(
                    "A possible accident scene with a vehicle "
                    "or person requiring assistance is visible."
                ),
                evidence=[
                    "Vehicle or person detected",
                    "Possible accident scene",
                    "Emergency assistance may be required",
                ],
                recommended_action=(
                    "Perform scene assessment and "
                    "maintain aerial observation."
                ),
            )

        # --------------------------------------------------
        # STRUCTURAL DAMAGE DETECTION
        # --------------------------------------------------

        if "structural_damage" in filename:
            return VisionAnalysis(
                incident_type="structural_damage",
                confidence=0.90,
                severity="high",
                summary=(
                    "Visible structural damage is present "
                    "in the inspected area."
                ),
                evidence=[
                    "Damaged structural elements detected",
                    "Possible instability observed",
                    "Affected structure requires inspection",
                ],
                recommended_action=(
                    "Perform detailed structural inspection "
                    "using RGB and thermal imagery."
                ),
            )

        # --------------------------------------------------
        # FLOODING DETECTION
        # --------------------------------------------------

        if "flooding" in filename:
            return VisionAnalysis(
                incident_type="flooding",
                confidence=0.93,
                severity="high",
                summary=(
                    "Flooding is visible across the "
                    "affected area."
                ),
                evidence=[
                    "Standing water detected",
                    "Flooded area identified",
                    "Access routes may be affected",
                ],
                recommended_action=(
                    "Map the affected area and monitor "
                    "safe access routes."
                ),
            )

        # --------------------------------------------------
        # PERSISTENT UNCERTAINTY
        # --------------------------------------------------
        # Used to demonstrate bounded autonomy.
        # The image remains ambiguous even after
        # automatic replanning, eventually requiring
        # human review.

        if "persistent_unclear" in filename:
            return VisionAnalysis(
                incident_type="unknown",
                confidence=0.35,
                severity="unknown",
                summary=(
                    "Repeated aerial observations remain "
                    "ambiguous and do not provide enough "
                    "evidence for autonomous action."
                ),
                evidence=[
                    "Image remains indistinct",
                    "No reliable emergency signature detected",
                    "Repeated observation did not improve confidence",
                ],
                recommended_action=(
                    "Human operator review is required "
                    "before continuing the mission."
                ),
            )

        # --------------------------------------------------
        # LOW-CONFIDENCE OBSERVATION
        # --------------------------------------------------

        if "unclear" in filename:
            return VisionAnalysis(
                incident_type="unknown",
                confidence=0.35,
                severity="unknown",
                summary=(
                    "The aerial image is ambiguous and "
                    "does not provide enough evidence "
                    "to identify an emergency."
                ),
                evidence=[
                    "Image contains an indistinct structure",
                    "No clear emergency signature detected",
                ],
                recommended_action=(
                    "Reposition the drone and capture "
                    "another RGB image."
                ),
            )

        # --------------------------------------------------
        # DEFAULT OBSERVATION
        # --------------------------------------------------

        return VisionAnalysis(
            incident_type="unknown",
            confidence=0.35,
            severity="low",
            summary=(
                "No specific emergency incident could "
                "be confidently identified."
            ),
            evidence=[
                "No known emergency pattern detected",
            ],
            recommended_action=(
                "Capture another image from a better "
                "observation position."
            ),
        )