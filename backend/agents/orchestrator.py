from uuid import uuid4

from backend.agents.fleet_agent import FleetAgent
from backend.agents.incident_agent import (
    IncidentAgent,
    IncidentAlert,
)
from backend.agents.knowledge_agent import KnowledgeAgent
from backend.agents.mission_agent import MissionAgent
from backend.agents.mission_executor import MissionExecutor
from backend.agents.mission_state import MissionState
from backend.agents.vision_loop import VisionDecisionLoop
from backend.safety.safety_governor import SafetyGovernor


class EmergencyOrchestrator:
    """
    Coordinates the complete emergency-response workflow.

    AI agents can analyze and recommend actions, but every
    physical drone action is validated by the Safety Governor.

    Low-confidence vision results trigger automatic replanning.

    Persistent uncertainty escalates to human review.

    The orchestrator intentionally stops before mission
    completion when human approval is required.
    """

    def __init__(self):
        self.incident_agent = IncidentAgent()
        self.fleet_agent = FleetAgent()
        self.knowledge_agent = KnowledgeAgent()
        self.mission_agent = MissionAgent()
        self.mission_executor = MissionExecutor()
        self.vision_loop = VisionDecisionLoop()
        self.safety_governor = SafetyGovernor()

    def handle_incident(
        self,
        alert: IncidentAlert,
    ) -> dict:

        # --------------------------------------------------
        # 1. EVALUATE INCIDENT
        # --------------------------------------------------

        incident_result = self.incident_agent.evaluate(
            alert
        )

        if incident_result["decision"] != "dispatch_drone":
            return {
                "success": True,
                "status": "no_dispatch",
                "incident": incident_result,
            }

        # --------------------------------------------------
        # 2. SELECT BEST DRONE
        # --------------------------------------------------

        fleet_result = self.fleet_agent.select_drone(
            alert.incident_type
        )

        if not fleet_result["selected"]:
            return {
                "success": False,
                "status": "no_drone_available",
                "incident": incident_result,
                "fleet": fleet_result,
            }

        drone_id = fleet_result["drone_id"]

        # --------------------------------------------------
        # 3. RETRIEVE OPERATIONAL GUIDANCE
        # --------------------------------------------------

        knowledge_result = (
            self.knowledge_agent.get_guidance(
                alert.incident_type
            )
        )

        # --------------------------------------------------
        # 4. CREATE INITIAL MISSION
        # --------------------------------------------------

        mission = self.mission_agent.create_mission(
            drone_id=drone_id,
            incident_type=alert.incident_type,
            latitude=alert.location["latitude"],
            longitude=alert.location["longitude"],
            guidance=knowledge_result["guidance"],
        )

        # --------------------------------------------------
        # 5. CREATE PERSISTENT MISSION STATE
        # --------------------------------------------------

        mission_id = (
            f"MISSION-{uuid4().hex[:8].upper()}"
        )

        state = MissionState(
            mission_id=mission_id,
            drone_id=drone_id,
            incident_type=alert.incident_type,
            status="mission_started",
        )

        # --------------------------------------------------
        # 6. EXECUTE INITIAL FLIGHT
        #
        # takeoff -> goto -> RGB
        #
        # IMPORTANT:
        # Do NOT execute return_home yet.
        # The mission may need vision analysis,
        # replanning, thermal verification or HITL.
        # --------------------------------------------------

        initial_mission = {
            **mission,
            "steps": mission["steps"][:-1],
        }

        # --------------------------------------------------
        # DEMO OBSERVATION STRATEGY
        #
        # Normal fire:
        #     unclear -> fire after replanning
        #
        # HITL fire:
        #     persistent_unclear -> persistent_unclear
        #     -> low confidence remains
        #     -> human review
        # --------------------------------------------------

        observation_scenario = (
            alert.incident_type
        )

        if alert.incident_type == "fire":
            observation_scenario = "unclear"

            if (
                "persistent uncertainty"
                in alert.description.lower()
            ):
                observation_scenario = (
                    "persistent_unclear"
                )

        for step in initial_mission["steps"]:
            if step["action"] == "capture_rgb":
                step["scenario"] = (
                    observation_scenario
                )

        execution = self.mission_executor.execute(
            initial_mission
        )

        if not execution["success"]:

            state.status = "mission_failed"

            self.vision_loop.memory.save_mission(
                state
            )

            return {
                "success": False,
                "status": "mission_failed",
                "mission_id": mission_id,
                "incident": incident_result,
                "fleet": fleet_result,
                "knowledge": {
                    "sources": [
                        item["source"]
                        for item in knowledge_result[
                            "guidance"
                        ]
                    ]
                },
                "mission": mission,
                "execution": execution,
            }

        # --------------------------------------------------
        # 7. EXTRACT RGB OBSERVATION
        # --------------------------------------------------

        rgb_images = [
            item["result"]
            for item in execution.get(
                "results",
                [],
            )
            if (
                item.get("action")
                == "capture_rgb"
                and item.get("status")
                == "executed"
            )
        ]

        vision_result = None
        thermal_result = None
        replan_result = None

        # --------------------------------------------------
        # 8. ANALYZE AERIAL EVIDENCE
        # --------------------------------------------------

        if rgb_images:

            latest_rgb = rgb_images[-1]

            image_path = latest_rgb.get(
                "image"
            )

            if image_path:

                vision_result = (
                    self.vision_loop.analyze(
                        state=state,
                        image_path=image_path,
                        scenario=observation_scenario,
                    )
                )

                # VisionDecisionLoop automatically
                # invokes ReplanningAgent when confidence
                # is low.
                replan_result = (
                    vision_result.get("replan")
                )

                # Use the newest analysis after
                # successful automatic replanning.
                if (
                    replan_result
                    and replan_result.get(
                        "success"
                    )
                ):
                    vision_result = {
                        **vision_result,
                        "analysis": (
                            replan_result[
                                "analysis"
                            ]
                        ),
                        "decision": (
                            replan_result[
                                "decision"
                            ]
                        ),
                    }

        # --------------------------------------------------
        # 9. HANDLE AI DECISION
        # --------------------------------------------------

        if vision_result:

            decision = vision_result[
                "decision"
            ]

            # --------------------------------------------------
            # AUTOMATIC REPLANNING EXHAUSTED
            # --------------------------------------------------

            if decision["requires_replan"]:

                state.status = (
                    "human_review_required"
                )

                self.vision_loop.memory.save_mission(
                    state
                )

                return {
                    "success": False,
                    "status": (
                        "human_review_required"
                    ),
                    "mission_id": mission_id,
                    "incident": incident_result,
                    "fleet": fleet_result,
                    "knowledge": {
                        "sources": [
                            item["source"]
                            for item in knowledge_result[
                                "guidance"
                            ]
                        ]
                    },
                    "mission": mission,
                    "execution": execution,
                    "vision": vision_result,
                    "replan": replan_result,
                    "memory": {
                        "mission_id": (
                            state.mission_id
                        ),
                        "status": state.status,
                        "replans": state.replans,
                        "observations": len(
                            state.observations
                        ),
                        "decisions": len(
                            state.decisions
                        ),
                    },
                    "hitl": {
                        "required": True,
                        "reason": (
                            "Vision confidence remained "
                            "below the safe autonomous "
                            "decision threshold."
                        ),
                        "paused_before": (
                            "mission_completion"
                        ),
                    },
                }

            # --------------------------------------------------
            # HIGH-CONFIDENCE THERMAL DECISION
            # --------------------------------------------------

            if (
                decision["next_action"]
                == "capture_thermal"
            ):

                # Safety Governor validates the action
                # before it reaches the drone simulator.
                safety = (
                    self.safety_governor.validate(
                        drone_id,
                        "capture_thermal",
                    )
                )

                if not safety["approved"]:

                    state.status = (
                        "safety_blocked"
                    )

                    self.vision_loop.memory.save_mission(
                        state
                    )

                    return {
                        "success": False,
                        "status": (
                            "safety_blocked"
                        ),
                        "mission_id": mission_id,
                        "incident": incident_result,
                        "fleet": fleet_result,
                        "knowledge": {
                            "sources": [
                                item["source"]
                                for item in knowledge_result[
                                    "guidance"
                                ]
                            ]
                        },
                        "mission": mission,
                        "execution": execution,
                        "vision": vision_result,
                        "replan": replan_result,
                        "thermal": {
                            "status": "blocked",
                            "safety": safety,
                        },
                    }

                # Execute thermal inspection.
                thermal_result = (
                    self.mission_executor.execute(
                        {
                            "steps": [
                                {
                                    "step": 4,
                                    "action": (
                                        "capture_thermal"
                                    ),
                                    "drone_id": (
                                        drone_id
                                    ),
                                    "scenario": "fire",
                                }
                            ]
                        }
                    )

                )

                if not thermal_result["success"]:
                    state.status = (
                        "thermal_failed"
                    )

                    self.vision_loop.memory.save_mission(
                        state
                    )

                    return {
                        "success": False,
                        "status": (
                            "thermal_failed"
                        ),
                        "mission_id": mission_id,
                        "incident": incident_result,
                        "fleet": fleet_result,
                        "knowledge": {
                            "sources": [
                                item["source"]
                                for item in knowledge_result[
                                    "guidance"
                                ]
                            ]
                        },
                        "mission": mission,
                        "execution": execution,
                        "vision": vision_result,
                        "replan": replan_result,
                        "thermal": thermal_result,
                    }

        # --------------------------------------------------
        # 10. RETURN DRONE HOME
        # --------------------------------------------------

        return_result = (
            self.mission_executor.execute(
                {
                    "steps": [
                        {
                            "step": 5,
                            "action": "return_home",
                            "drone_id": drone_id,
                        }
                    ]
                }
            )
        )

        if not return_result["success"]:

            state.status = "return_failed"

        else:

            state.status = "mission_completed"

        # --------------------------------------------------
        # 11. PERSIST FINAL MISSION STATE
        # --------------------------------------------------

        self.vision_loop.memory.save_mission(
            state
        )

        # --------------------------------------------------
        # 12. FINAL RESPONSE
        # --------------------------------------------------

        return {
            "success": return_result["success"],
            "status": state.status,
            "mission_id": mission_id,
            "incident": incident_result,
            "fleet": fleet_result,
            "knowledge": {
                "sources": [
                    item["source"]
                    for item in knowledge_result[
                        "guidance"
                    ]
                ]
            },
            "mission": mission,
            "execution": execution,
            "vision": vision_result,
            "replan": replan_result,
            "thermal": thermal_result,
            "return_home": return_result,
            "memory": {
                "mission_id": state.mission_id,
                "status": state.status,
                "replans": state.replans,
                "observations": len(
                    state.observations
                ),
                "decisions": len(
                    state.decisions
                ),
            },
        }