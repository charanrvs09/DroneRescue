from backend.safety.safety_governor import SafetyGovernor

from drone_simulator.simulator import (
    capture_rgb,
    capture_thermal,
    goto,
    return_home,
    takeoff,
)


class MissionExecutor:
    """
    Executes mission steps only after they pass
    through the deterministic Safety Governor.
    """

    def __init__(self):
        self.safety_governor = SafetyGovernor()

    def execute(self, mission: dict) -> dict:
        results = []

        for step in mission["steps"]:
            action = step["action"]
            drone_id = step["drone_id"]

            # Pass destination coordinates to the Safety Governor
            # when validating a goto action.
            safety = self.safety_governor.validate(
                drone_id=drone_id,
                action=action,
                latitude=step.get("latitude"),
                longitude=step.get("longitude"),
            )

            if not safety["approved"]:
                results.append(
                    {
                        "step": step["step"],
                        "action": action,
                        "status": "blocked",
                        "safety": safety,
                    }
                )

                return {
                    "success": False,
                    "status": "mission_blocked",
                    "results": results,
                }

            if action == "takeoff":
                result = takeoff(drone_id)

            elif action == "goto":
                result = goto(
                    drone_id,
                    step["latitude"],
                    step["longitude"],
                )

            elif action == "capture_rgb":
                result = capture_rgb(
                    drone_id,
                    step.get("scenario", "normal"),
                )

            elif action == "capture_thermal":
                result = capture_thermal(
                    drone_id,
                    step.get("scenario", "normal"),
                )

            elif action == "return_home":
                result = return_home(drone_id)

            else:
                result = {
                    "success": False,
                    "error": f"Unknown action: {action}",
                }

            results.append(
                {
                    "step": step["step"],
                    "action": action,
                    "status": (
                        "executed"
                        if result["success"]
                        else "failed"
                    ),
                    "result": result,
                }
            )

            if not result["success"]:
                return {
                    "success": False,
                    "status": "mission_failed",
                    "results": results,
                }

        return {
            "success": True,
            "status": "mission_completed",
            "results": results,
        }