from backend.agents.human_approval import HumanApprovalAgent
from backend.agents.incident_agent import IncidentAlert
from backend.agents.mission_executor import MissionExecutor
from backend.agents.mission_state import MissionState
from backend.agents.orchestrator import EmergencyOrchestrator
from backend.memory.mission_memory import MissionMemory

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from drone_simulator.fleet import get_all_drones
from drone_simulator.simulator import (
    capture_rgb,
    capture_thermal,
    get_drone_status,
    goto,
    return_home,
    takeoff,
)


router = APIRouter(
    prefix="/drones",
    tags=["Drones"],
)

mission_memory = MissionMemory()

human_approval_agent = HumanApprovalAgent()

mission_executor = MissionExecutor()


# --------------------------------------------------
# HUMAN-IN-THE-LOOP STATE
# --------------------------------------------------

pending_approvals = {}

pending_missions = {}


class GotoRequest(BaseModel):
    latitude: float
    longitude: float


class ApprovalDecision(BaseModel):
    approved: bool
    operator: str = "human_operator"


# --------------------------------------------------
# MISSION MEMORY HELPERS
# --------------------------------------------------

def persist_mission_status(
    mission_id: str,
    status: str,
    operator: str | None = None,
    decision_type: str | None = None,
) -> None:
    """
    Update an existing mission in persistent SQLite memory.

    Existing observations and AI decisions are preserved.
    Human approval/rejection is appended to the decision history.
    """

    existing = mission_memory.get_mission(
        mission_id
    )

    if existing is None:
        return

    observations = existing.get(
        "observations",
        [],
    )

    decisions = existing.get(
        "decisions",
        [],
    )

    if decision_type:
        human_decision = {
            "decision": decision_type,
            "operator": (
                operator or "human_operator"
            ),
        }

        decisions = [
            *decisions,
            human_decision,
        ]

    state = MissionState(
        mission_id=existing["mission_id"],
        drone_id=existing["drone_id"],
        incident_type=existing[
            "incident_type"
        ],
        status=status,
        replans=existing.get(
            "replans",
            0,
        ),
        observations=observations,
        decisions=decisions,
    )

    mission_memory.save_mission(state)


# --------------------------------------------------
# DRONE LIST
# --------------------------------------------------

@router.get("")
def list_drones():
    return {
        "drones": [
            drone.model_dump()
            for drone in get_all_drones()
        ]
    }


# --------------------------------------------------
# MISSION HISTORY
# --------------------------------------------------

@router.get("/missions")
def list_missions():
    return {
        "missions": mission_memory.get_all_missions()
    }


@router.get("/missions/{mission_id}")
def get_mission_history(
    mission_id: str,
):
    mission = mission_memory.get_mission(
        mission_id
    )

    if mission is None:
        raise HTTPException(
            status_code=404,
            detail=(
                f"Mission {mission_id} not found"
            ),
        )

    return mission


# --------------------------------------------------
# HUMAN-IN-THE-LOOP
# --------------------------------------------------

@router.get("/approvals")
def list_pending_approvals():
    """
    Return actions waiting for human authorization.
    """

    return {
        "approvals": list(
            pending_approvals.values()
        )
    }


@router.get("/approvals/{mission_id}")
def get_approval(
    mission_id: str,
):
    approval = pending_approvals.get(
        mission_id
    )

    if approval is None:
        raise HTTPException(
            status_code=404,
            detail=(
                f"No pending approval found "
                f"for mission {mission_id}"
            ),
        )

    return approval


@router.post(
    "/approvals/{mission_id}/resolve"
)
def resolve_approval(
    mission_id: str,
    decision: ApprovalDecision,
):
    """
    Approve or reject a pending high-risk action.

    APPROVE:
        Continue the mission through the Safety Governor.
        Fire missions perform thermal verification and
        then return home.

    REJECT:
        Stop mission continuation and safely return home.

    Every physical action uses MissionExecutor,
    which means the Safety Governor remains in the loop.
    """

    approval = pending_approvals.get(
        mission_id
    )

    if approval is None:
        raise HTTPException(
            status_code=404,
            detail=(
                f"No pending approval found "
                f"for mission {mission_id}"
            ),
        )

    mission_context = pending_missions.get(
        mission_id
    )

    if mission_context is None:
        raise HTTPException(
            status_code=404,
            detail=(
                f"Mission context for {mission_id} "
                f"is no longer available"
            ),
        )

    # --------------------------------------------------
    # RECORD HUMAN DECISION
    # --------------------------------------------------

    human_result = (
        human_approval_agent.resolve(
            approval_request=approval,
            approved=decision.approved,
            operator=decision.operator,
        )
    )

    drone_id = mission_context[
        "drone_id"
    ]

    incident_type = mission_context[
        "incident_type"
    ]

    # --------------------------------------------------
    # HUMAN REJECTED
    # --------------------------------------------------

    if not decision.approved:

        safe_return = (
            mission_executor.execute(
                {
                    "steps": [
                        {
                            "step": 1,
                            "action": "return_home",
                            "drone_id": drone_id,
                        }
                    ]
                }
            )
        )

        persist_mission_status(
            mission_id=mission_id,
            status=(
                "human_rejected_safe_return"
            ),
            operator=decision.operator,
            decision_type="human_rejected",
        )

        pending_approvals.pop(
            mission_id,
            None,
        )

        pending_missions.pop(
            mission_id,
            None,
        )

        return {
            **human_result,
            "mission_status": (
                "human_rejected_safe_return"
            ),
            "execution": safe_return,
            "message": (
                "Human operator rejected mission "
                "continuation. Drone was instructed "
                "to return home safely."
            ),
        }

    # --------------------------------------------------
    # HUMAN APPROVED
    # --------------------------------------------------

    continuation_steps = []

    # Fire missions receive thermal verification.
    if incident_type == "fire":

        continuation_steps.append(
            {
                "step": 1,
                "action": "capture_thermal",
                "drone_id": drone_id,
                "scenario": "fire",
            }
        )

    # Always return home after authorized action.
    continuation_steps.append(
        {
            "step": len(
                continuation_steps
            ) + 1,
            "action": "return_home",
            "drone_id": drone_id,
        }
    )

    continuation_result = (
        mission_executor.execute(
            {
                "steps": continuation_steps
            }
        )
    )

    # --------------------------------------------------
    # APPROVED CONTINUATION FAILED
    # --------------------------------------------------

    if not continuation_result[
        "success"
    ]:

        fallback_return = (
            mission_executor.execute(
                {
                    "steps": [
                        {
                            "step": 1,
                            "action": "return_home",
                            "drone_id": drone_id,
                        }
                    ]
                }
            )
        )

        persist_mission_status(
            mission_id=mission_id,
            status="continuation_failed",
            operator=decision.operator,
            decision_type=(
                "human_approved_continuation_failed"
            ),
        )

        pending_approvals.pop(
            mission_id,
            None,
        )

        pending_missions.pop(
            mission_id,
            None,
        )

        return {
            **human_result,
            "mission_status": (
                "continuation_failed"
            ),
            "execution": continuation_result,
            "fallback_return": fallback_return,
            "message": (
                "Human approval was granted, but "
                "the continuation action failed. "
                "A Safety Governor-controlled "
                "return-home attempt was made."
            ),
        }

    # --------------------------------------------------
    # APPROVED MISSION COMPLETED
    # --------------------------------------------------

    persist_mission_status(
        mission_id=mission_id,
        status="mission_completed",
        operator=decision.operator,
        decision_type=(
            "human_approved_continuation"
        ),
    )

    pending_approvals.pop(
        mission_id,
        None,
    )

    pending_missions.pop(
        mission_id,
        None,
    )

    return {
        **human_result,
        "mission_status": (
            "human_approved_mission_completed"
        ),
        "execution": continuation_result,
        "message": (
            "Human operator approved continuation. "
            "The drone completed the authorized "
            "verification and returned home."
        ),
    }


# --------------------------------------------------
# EMERGENCY DISPATCH
# --------------------------------------------------

@router.post("/emergency")
def trigger_emergency(
    alert: IncidentAlert,
):

    result = (
        EmergencyOrchestrator()
        .handle_incident(alert)
    )

    # --------------------------------------------------
    # HUMAN APPROVAL REQUIRED
    # --------------------------------------------------

    if (
        result.get("status")
        == "human_review_required"
    ):

        mission_id = result[
            "mission_id"
        ]

        approval_request = (
            human_approval_agent
            .create_request(
                mission_id=mission_id,
                drone_id=result[
                    "fleet"
                ]["drone_id"],
                action=(
                    "mission_continuation"
                ),
                reason=(
                    "AI confidence remained below "
                    "the safe autonomous decision "
                    "threshold."
                ),
                risk_level="high",
            )
        )

        pending_approvals[
            mission_id
        ] = approval_request

        # --------------------------------------------------
        # IMPORTANT FIX:
        #
        # The orchestrator returns:
        #
        # result
        #   └── incident
        #       ├── decision
        #       ├── reason
        #       └── incident
        #           └── incident_type
        #
        # Therefore the correct lookup is:
        #
        # result["incident"]["incident"]["incident_type"]
        # --------------------------------------------------

        pending_missions[
            mission_id
        ] = {
            "mission_id": mission_id,

            "drone_id": result[
                "fleet"
            ]["drone_id"],

            "incident_type": result[
                "incident"
            ]["incident"]["incident_type"],

            "scenario": result[
                "mission"
            ]["steps"][2].get(
                "scenario",
                "normal",
            ),

            "result": result,
        }

        result["approval"] = (
            approval_request
        )

        return result

    # --------------------------------------------------
    # OTHER FAILURE
    # --------------------------------------------------

    if not result["success"]:
        raise HTTPException(
            status_code=400,
            detail=result,
        )

    return result


# --------------------------------------------------
# DRONE SIMULATOR ENDPOINTS
# --------------------------------------------------

@router.get("/{drone_id}")
def drone_status(
    drone_id: str,
):

    result = get_drone_status(
        drone_id
    )

    if not result["success"]:
        raise HTTPException(
            status_code=404,
            detail=result["error"],
        )

    return result


@router.post("/{drone_id}/takeoff")
def drone_takeoff(
    drone_id: str,
):

    result = takeoff(
        drone_id
    )

    if not result["success"]:
        raise HTTPException(
            status_code=400,
            detail=result["error"],
        )

    return result


@router.post("/{drone_id}/goto")
def drone_goto(
    drone_id: str,
    request: GotoRequest,
):

    result = goto(
        drone_id,
        request.latitude,
        request.longitude,
    )

    if not result["success"]:
        raise HTTPException(
            status_code=400,
            detail=result["error"],
        )

    return result


@router.post(
    "/{drone_id}/capture/rgb"
)
def drone_capture_rgb(
    drone_id: str,
    scenario: str = "normal",
):

    result = capture_rgb(
        drone_id,
        scenario,
    )

    if not result["success"]:
        raise HTTPException(
            status_code=400,
            detail=result["error"],
        )

    return result


@router.post(
    "/{drone_id}/capture/thermal"
)
def drone_capture_thermal(
    drone_id: str,
    scenario: str = "normal",
):

    result = capture_thermal(
        drone_id,
        scenario,
    )

    if not result["success"]:
        raise HTTPException(
            status_code=400,
            detail=result["error"],
        )

    return result


@router.post(
    "/{drone_id}/return-home"
)
def drone_return_home(
    drone_id: str,
):

    result = return_home(
        drone_id
    )

    if not result["success"]:
        raise HTTPException(
            status_code=400,
            detail=result["error"],
        )

    return result