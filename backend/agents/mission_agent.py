class MissionAgent:
    """
    Creates the initial flight mission.

    AI-driven follow-up actions are decided after
    the drone captures its first RGB observation.
    """

    def create_mission(
        self,
        drone_id: str,
        incident_type: str,
        latitude: float,
        longitude: float,
        guidance: list[dict] | None = None,
    ) -> dict:

        mission = [
            {
                "step": 1,
                "action": "takeoff",
                "drone_id": drone_id,
            },
            {
                "step": 2,
                "action": "goto",
                "drone_id": drone_id,
                "latitude": latitude,
                "longitude": longitude,
            },
            {
                "step": 3,
                "action": "capture_rgb",
                "drone_id": drone_id,
                "scenario": incident_type,
            },
        ]

        mission.append(
            {
                "step": 4,
                "action": "return_home",
                "drone_id": drone_id,
            }
        )

        return {
            "mission_created": True,
            "drone_id": drone_id,
            "incident_type": incident_type,
            "waypoint": {
                "latitude": latitude,
                "longitude": longitude,
            },
            "steps": mission,
            "guidance_sources": [
                item["source"]
                for item in (guidance or [])
            ],
        }