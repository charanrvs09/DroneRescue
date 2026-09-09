from backend.agents.decision_agent import DecisionAgent
from backend.agents.mission_state import MissionState
from backend.vision.vlm_service import VLMService
from drone_simulator.simulator import capture_rgb


class ReplanningAgent:
    """
    Replans the mission when the Vision Agent
    cannot confidently identify the incident.
    """

    MAX_REPLANS = 2

    def __init__(self):
        self.vlm_service = VLMService()
        self.decision_agent = DecisionAgent()

    def replan(
        self,
        state: MissionState,
        scenario: str = "normal",
    ) -> dict:

        # Prevent unlimited autonomous replanning.
        if state.replans >= self.MAX_REPLANS:
            state.status = "human_review_required"

            return {
                "success": False,
                "status": "human_review_required",
                "reason": (
                    "Maximum automatic replans reached. "
                    "Human review is required."
                ),
                "replans": state.replans,
            }

        # Record the replan before taking the new observation.
        state.record_replan()

        # --------------------------------------------------
        # DYNAMIC OBSERVATION
        # --------------------------------------------------

        observation_scenario = scenario

        # Normal demo:
        # unclear -> fire -> confidence improves.
        if scenario == "unclear":
            observation_scenario = "fire"

        # HITL demo:
        # persistent_unclear -> persistent_unclear
        # so confidence remains low.
        elif scenario == "persistent_unclear":
            observation_scenario = "persistent_unclear"

        observation = capture_rgb(
            state.drone_id,
            observation_scenario,
        )

        if not observation["success"]:
            state.status = "observation_failed"

            return {
                "success": False,
                "status": "observation_failed",
                "result": observation,
                "replans": state.replans,
            }

        # --------------------------------------------------
        # VISION RE-ANALYSIS
        # --------------------------------------------------

        image_path = observation["image"]

        analysis = self.vlm_service.analyze_image(
            image_path
        )

        state.add_observation(
            image=image_path,
            analysis=analysis.model_dump(),
        )

        # --------------------------------------------------
        # DECISION AFTER REPLANNING
        # --------------------------------------------------

        decision = self.decision_agent.decide(
            analysis
        )

        state.add_decision(decision)

        if not decision["requires_replan"]:
            state.status = "assessment_complete"

        return {
            "success": True,
            "status": "replanned",
            "observation": observation,
            "analysis": analysis.model_dump(),
            "decision": decision,
            "replans": state.replans,
        }