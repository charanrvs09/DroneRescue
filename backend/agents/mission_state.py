from pydantic import BaseModel, Field


class MissionState(BaseModel):
    """
    Shared state maintained during an emergency mission.
    """

    mission_id: str
    drone_id: str
    incident_type: str

    current_step: int = 0

    observations: list[dict] = Field(
        default_factory=list
    )

    decisions: list[dict] = Field(
        default_factory=list
    )

    actions: list[dict] = Field(
        default_factory=list
    )

    status: str = "initialized"

    replans: int = 0

    def add_observation(
        self,
        image: str,
        analysis: dict,
    ) -> None:
        self.observations.append(
            {
                "image": image,
                "analysis": analysis,
            }
        )

    def add_decision(
        self,
        decision: dict,
    ) -> None:
        self.decisions.append(decision)

    def add_action(
        self,
        action: dict,
    ) -> None:
        self.actions.append(action)

    def record_replan(self) -> None:
        self.replans += 1
        self.status = "replanning"