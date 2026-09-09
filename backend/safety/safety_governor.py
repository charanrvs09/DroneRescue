from math import asin, cos, radians, sin, sqrt

from drone_simulator.fleet import get_drone
from drone_simulator.models import DroneStatus


class SafetyGovernor:
    """
    Deterministic safety layer between AI decisions
    and drone execution.

    AI can recommend actions, but the Safety Governor
    has the final authority to approve or block them.
    """

    # Minimum battery required for different actions.
    MIN_BATTERY = {
        "takeoff": 25.0,
        "goto": 20.0,
        "capture_rgb": 15.0,
        "capture_thermal": 20.0,
        "return_home": 10.0,
    }

    # Operational geofence.
    GEOFENCE_CENTER = {
        "latitude": 17.6868,
        "longitude": 83.2185,
    }

    GEOFENCE_RADIUS_KM = 10.0

    def _distance_km(
        self,
        latitude: float,
        longitude: float,
    ) -> float:
        """
        Calculate great-circle distance from the
        operational center using the Haversine formula.
        """

        lat1 = radians(
            self.GEOFENCE_CENTER["latitude"]
        )
        lon1 = radians(
            self.GEOFENCE_CENTER["longitude"]
        )

        lat2 = radians(latitude)
        lon2 = radians(longitude)

        delta_lat = lat2 - lat1
        delta_lon = lon2 - lon1

        a = (
            sin(delta_lat / 2) ** 2
            + cos(lat1)
            * cos(lat2)
            * sin(delta_lon / 2) ** 2
        )

        return 6371.0 * 2 * asin(sqrt(a))

    def validate(
        self,
        drone_id: str,
        action: str,
        latitude: float | None = None,
        longitude: float | None = None,
    ) -> dict:
        """
        Validate a proposed drone action.

        Checks:
        1. Drone exists
        2. Drone is not offline
        3. Battery is sufficient
        4. Required hardware exists
        5. Goto destination is inside geofence
        """

        drone = get_drone(drone_id)

        if drone is None:
            return {
                "approved": False,
                "reason": f"Drone {drone_id} not found.",
                "rule": "DRONE_EXISTS",
            }

        if drone.status == DroneStatus.OFFLINE:
            return {
                "approved": False,
                "reason": f"Drone {drone_id} is offline.",
                "rule": "DRONE_STATUS",
            }

        required_battery = self.MIN_BATTERY.get(
            action,
            15.0,
        )

        if drone.battery < required_battery:
            return {
                "approved": False,
                "reason": (
                    f"Battery too low for {action}: "
                    f"{drone.battery}% available, "
                    f"{required_battery}% required."
                ),
                "rule": "BATTERY",
                "battery": drone.battery,
                "required_battery": required_battery,
            }

        if (
            action == "capture_thermal"
            and not drone.capabilities.thermal_camera
        ):
            return {
                "approved": False,
                "reason": (
                    f"Drone {drone_id} does not "
                    "have a thermal camera."
                ),
                "rule": "THERMAL_CAPABILITY",
            }

        if action == "goto":
            if latitude is None or longitude is None:
                return {
                    "approved": False,
                    "reason": (
                        "Goto action requires "
                        "latitude and longitude."
                    ),
                    "rule": "GEOFENCE_COORDINATES",
                }

            distance = self._distance_km(
                latitude,
                longitude,
            )

            if distance > self.GEOFENCE_RADIUS_KM:
                return {
                    "approved": False,
                    "reason": (
                        f"Destination is {distance:.2f} km "
                        f"from the operational center. "
                        f"Maximum allowed radius is "
                        f"{self.GEOFENCE_RADIUS_KM:.1f} km."
                    ),
                    "rule": "GEOFENCE",
                    "distance_km": round(distance, 2),
                    "max_distance_km": self.GEOFENCE_RADIUS_KM,
                }

        return {
            "approved": True,
            "reason": "All safety checks passed.",
            "rule": "APPROVED",
            "drone_id": drone_id,
            "action": action,
            "battery": drone.battery,
        }