from backend.safety.safety_governor import SafetyGovernor
from drone_simulator.simulator import (
    capture_rgb,
    capture_thermal,
)


class ResponseAgent:
    """
    Executes operational actions after Safety Governor approval.
    """

    def __init__(self):
        self.safety_governor = SafetyGovernor()

    def execute(
        self,
        drone_id: str,
        decision: dict,
        scenario: str = "normal",
    ) -> dict:
        next_action = decision.get("next_action")

        safety_result = self.safety_governor.validate(
            drone_id,
            next_action,
        )

        if not safety_result["approved"]:
            return {
                "success": False,
                "status": "blocked",
                "safety": safety_result,
            }

        if next_action == "capture_thermal":
            result = capture_thermal(
                drone_id,
                scenario,
            )

            return {
                **result,
                "status": "executed",
                "safety": safety_result,
            }

        if next_action == "capture_rgb":
            result = capture_rgb(
                drone_id,
                scenario,
            )

            return {
                **result,
                "status": "executed",
                "safety": safety_result,
            }

        return {
            "success": True,
            "status": "no_action_required",
            "action": next_action,
            "safety": safety_result,
        }