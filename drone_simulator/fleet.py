from drone_simulator.models import Drone, DroneCapabilities, DroneStatus

DRONES = [
    Drone(
        id="D1",
        name="Rescue-01",
        battery=85,
        latitude=17.6868,
        longitude=83.2185,
        status=DroneStatus.AVAILABLE,
        capabilities=DroneCapabilities(
            rgb_camera=True,
            thermal_camera=True,
        ),
    ),
    Drone(
        id="D2",
        name="Rescue-02",
        battery=63,
        latitude=17.7046,
        longitude=83.3013,
        status=DroneStatus.AVAILABLE,
        capabilities=DroneCapabilities(
            rgb_camera=True,
            thermal_camera=False,
        ),
    ),
    Drone(
        id="D3",
        name="Rescue-03",
        battery=91,
        latitude=17.7299,
        longitude=83.3042,
        status=DroneStatus.INSPECTING,
        capabilities=DroneCapabilities(
            rgb_camera=True,
            thermal_camera=True,
        ),
        current_mission="Infrastructure inspection",
    ),
]


def get_all_drones() -> list[Drone]:
    return DRONES


def get_drone(drone_id: str) -> Drone | None:
    for drone in DRONES:
        if drone.id == drone_id:
            return drone

    return None