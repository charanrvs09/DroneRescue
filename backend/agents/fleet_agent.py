from drone_simulator.fleet import get_all_drones
from drone_simulator.models import DroneStatus


class FleetAgent:
    """
    Selects the most suitable available drone for an incident.
    """

    def select_drone(
        self,
        incident_type: str,
    ) -> dict:
        drones = get_all_drones()

        candidates = [
            drone
            for drone in drones
            if drone.status == DroneStatus.AVAILABLE
            and drone.battery >= 25
        ]

        if not candidates:
            return {
                "selected": False,
                "reason": "No suitable drone is currently available.",
            }

        if incident_type in {"fire", "chemical_leak"}:
            thermal_candidates = [
                drone
                for drone in candidates
                if drone.capabilities.thermal_camera
            ]

            if thermal_candidates:
                candidates = thermal_candidates

        selected = max(
            candidates,
            key=lambda drone: drone.battery,
        )

        return {
            "selected": True,
            "drone_id": selected.id,
            "drone_name": selected.name,
            "reason": (
                f"Selected {selected.name} based on "
                f"availability, battery, and incident requirements."
            ),
            "battery": selected.battery,
            "capabilities": selected.capabilities.model_dump(),
        }