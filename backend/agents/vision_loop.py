from backend.agents.decision_agent import DecisionAgent
from backend.agents.mission_state import MissionState
from backend.agents.replanning_agent import ReplanningAgent
from backend.memory.mission_memory import MissionMemory
from backend.vision.vlm_service import VLMService


class VisionDecisionLoop:
    def __init__(self):
        self.vlm_service = VLMService()
        self.decision_agent = DecisionAgent()
        self.replanning_agent = ReplanningAgent()
        self.memory = MissionMemory()

    def analyze(
        self,
        state: MissionState,
        image_path: str,
        scenario: str = "normal",
    ) -> dict:

        analysis = self.vlm_service.analyze_image(image_path)

        state.add_observation(
            image=image_path,
            analysis=analysis.model_dump(),
        )

        decision = self.decision_agent.decide(analysis)

        state.add_decision(decision)

        self.memory.save_mission(state)

        if decision["requires_replan"]:
            replan_result = self.replanning_agent.replan(
                state,
                scenario=scenario,
            )

            self.memory.save_mission(state)

            return {
                "analysis": analysis.model_dump(),
                "decision": decision,
                "replan": replan_result,
            }

        state.status = "assessment_complete"

        self.memory.save_mission(state)

        return {
            "analysis": analysis.model_dump(),
            "decision": decision,
            "replan": None,
        }