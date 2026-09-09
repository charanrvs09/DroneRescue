from pydantic import BaseModel


class IncidentAlert(BaseModel):
    incident_type: str
    location: dict
    source: str
    confidence: float
    description: str


class IncidentAgent:
    """
    Evaluates an incoming factory alert and determines
    whether drone-based verification is required.
    """

    DISPATCH_THRESHOLD = 0.60

    def evaluate(self, alert: IncidentAlert) -> dict:
        if alert.confidence < self.DISPATCH_THRESHOLD:
            return {
                "decision": "do_not_dispatch",
                "reason": (
                    "Alert confidence is too low for "
                    "immediate drone dispatch."
                ),
                "incident": alert.model_dump(),
            }

        if alert.incident_type in {
            "fire",
            "chemical_leak",
            "intrusion",
            "accident",
            "structural_damage",
            "flooding",
        }:
            return {
                "decision": "dispatch_drone",
                "reason": (
                    "Incident requires aerial situational "
                    "awareness."
                ),
                "incident": alert.model_dump(),
            }

        return {
            "decision": "request_more_information",
            "reason": (
                "Incident type is not currently supported "
                "for autonomous drone response."
            ),
            "incident": alert.model_dump(),
        }