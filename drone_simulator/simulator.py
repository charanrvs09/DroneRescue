from drone_simulator.camera import (
    capture_rgb_frame,
    capture_thermal_frame,
)
from drone_simulator.fleet import get_drone
from drone_simulator.models import DroneStatus


def get_drone_status(drone_id: str):
    drone = get_drone(drone_id)

    if drone is None:
        return {
            "success": False,
            "error": f"Drone {drone_id} not found",
        }

    return {
        "success": True,
        "drone": drone.model_dump(),
    }


def takeoff(drone_id: str):
    drone = get_drone(drone_id)

    if drone is None:
        return {
            "success": False,
            "error": f"Drone {drone_id} not found",
        }

    if drone.status != DroneStatus.AVAILABLE:
        return {
            "success": False,
            "error": f"Drone {drone_id} is not available",
        }

    if drone.battery < 25:
        return {
            "success": False,
            "error": f"Drone {drone_id} has insufficient battery",
        }

    drone.status = DroneStatus.FLYING

    return {
        "success": True,
        "message": f"{drone.name} took off successfully",
        "drone_id": drone.id,
        "battery": drone.battery,
    }


def goto(
    drone_id: str,
    latitude: float,
    longitude: float,
):
    drone = get_drone(drone_id)

    if drone is None:
        return {
            "success": False,
            "error": f"Drone {drone_id} not found",
        }

    if drone.status not in {
        DroneStatus.FLYING,
        DroneStatus.INSPECTING,
    }:
        return {
            "success": False,
            "error": f"Drone {drone_id} is not currently flying",
        }

    drone.latitude = latitude
    drone.longitude = longitude

    return {
        "success": True,
        "message": f"{drone.name} moved to target location",
        "drone_id": drone.id,
        "latitude": latitude,
        "longitude": longitude,
    }


def capture_rgb(
    drone_id: str,
    scenario: str = "normal",
):
    drone = get_drone(drone_id)

    if drone is None:
        return {
            "success": False,
            "error": f"Drone {drone_id} not found",
        }

    if not drone.capabilities.rgb_camera:
        return {
            "success": False,
            "error": f"Drone {drone_id} does not have an RGB camera",
        }

    image_path = capture_rgb_frame(
        drone.id,
        drone.latitude,
        drone.longitude,
        scenario,
    )

    return {
        "success": True,
        "drone_id": drone.id,
        "sensor": "rgb",
        "scenario": scenario,
        "image": image_path,
    }


def capture_thermal(
    drone_id: str,
    scenario: str = "normal",
):
    drone = get_drone(drone_id)

    if drone is None:
        return {
            "success": False,
            "error": f"Drone {drone_id} not found",
        }

    if not drone.capabilities.thermal_camera:
        return {
            "success": False,
            "error": f"Drone {drone_id} does not have a thermal camera",
        }

    image_path = capture_thermal_frame(
        drone.id,
        drone.latitude,
        drone.longitude,
        scenario,
    )

    return {
        "success": True,
        "drone_id": drone.id,
        "sensor": "thermal",
        "scenario": scenario,
        "image": image_path,
    }


def return_home(drone_id: str):
    drone = get_drone(drone_id)

    if drone is None:
        return {
            "success": False,
            "error": f"Drone {drone_id} not found",
        }

    drone.status = DroneStatus.RETURNING

    # Simulate the drone completing its return journey.
    drone.status = DroneStatus.AVAILABLE
    drone.current_mission = None

    return {
        "success": True,
        "message": f"{drone.name} returned home safely",
        "drone_id": drone.id,
        "status": drone.status.value,
        "battery": drone.battery,
    }