from backend.vision.vlm_service import VisionAnalysis


class DecisionAgent:
    """
    Converts vision analysis into the next operational action.
    """

    def decide(self, analysis: VisionAnalysis) -> dict:

        # Low-confidence observations always trigger
        # another observation before emergency action.
        if analysis.confidence < 0.60:
            return {
                "decision": "recapture",
                "reason": (
                    "Vision confidence is too low for "
                    "safe emergency action."
                ),
                "next_action": "capture_rgb",
                "requires_replan": True,
            }

        # Fire requires thermal verification.
        if analysis.incident_type == "fire":
            return {
                "decision": "thermal_inspection",
                "reason": (
                    "High-confidence fire detection requires "
                    "thermal verification."
                ),
                "next_action": "capture_thermal",
                "requires_replan": False,
            }

        # Chemical leaks require remote inspection.
        if analysis.incident_type == "chemical_leak":
            return {
                "decision": "remote_hazard_inspection",
                "reason": (
                    "Potential chemical release detected. "
                    "Maintain safe distance and perform remote inspection."
                ),
                "next_action": "capture_rgb",
                "requires_replan": False,
            }

        # Intrusions require continued aerial surveillance.
        if analysis.incident_type == "intrusion":
            return {
                "decision": "aerial_surveillance",
                "reason": (
                    "Potential unauthorized activity detected. "
                    "Continue aerial monitoring."
                ),
                "next_action": "monitor",
                "requires_replan": False,
            }

        # Accidents require scene assessment.
        if analysis.incident_type == "accident":
            return {
                "decision": "scene_assessment",
                "reason": (
                    "Accident scene detected. "
                    "Perform aerial assessment for situational awareness."
                ),
                "next_action": "capture_rgb",
                "requires_replan": False,
            }

        # Structural damage requires detailed inspection.
        if analysis.incident_type == "structural_damage":
            return {
                "decision": "structural_inspection",
                "reason": (
                    "Structural damage detected. "
                    "Perform detailed aerial inspection."
                ),
                "next_action": "capture_rgb",
                "requires_replan": False,
            }

        # Flooding requires mapping and monitoring.
        if analysis.incident_type == "flooding":
            return {
                "decision": "flood_mapping",
                "reason": (
                    "Flooding detected. "
                    "Map the affected area and monitor access routes."
                ),
                "next_action": "capture_rgb",
                "requires_replan": False,
            }

        # Unknown high-confidence observations.
        return {
            "decision": "continue_monitoring",
            "reason": (
                "No specialized emergency action is available "
                "for the detected incident."
            ),
            "next_action": "monitor",
            "requires_replan": False,
        }
