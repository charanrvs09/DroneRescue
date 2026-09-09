from pydantic import BaseModel


class ApprovalRequest(BaseModel):
    """
    Represents an action requiring human authorization.
    """

    mission_id: str
    drone_id: str
    action: str
    reason: str
    risk_level: str = "high"


class HumanApprovalAgent:
    """
    Handles human authorization for high-risk actions.
    """

    def create_request(
        self,
        mission_id: str,
        drone_id: str,
        action: str,
        reason: str,
        risk_level: str = "high",
    ) -> dict:

        request = ApprovalRequest(
            mission_id=mission_id,
            drone_id=drone_id,
            action=action,
            reason=reason,
            risk_level=risk_level,
        )

        return {
            "status": "awaiting_human_approval",
            "approval_required": True,
            "request": request.model_dump(),
        }

    def resolve(
        self,
        approval_request: dict,
        approved: bool,
        operator: str = "human_operator",
    ) -> dict:

        request = approval_request["request"]

        if approved:
            return {
                "status": "approved",
                "approved": True,
                "operator": operator,
                "mission_id": request["mission_id"],
                "drone_id": request["drone_id"],
                "action": request["action"],
            }

        return {
            "status": "rejected",
            "approved": False,
            "operator": operator,
            "mission_id": request["mission_id"],
            "drone_id": request["drone_id"],
            "action": request["action"],
            "reason": "Human operator rejected the action.",
        }