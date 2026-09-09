from enum import Enum

from pydantic import BaseModel, Field


class DroneStatus(str, Enum):
    AVAILABLE = "available"
    FLYING = "flying"
    INSPECTING = "inspecting"
    RETURNING = "returning"
    CHARGING = "charging"
    OFFLINE = "offline"


class DroneCapabilities(BaseModel):
    rgb_camera: bool = True
    thermal_camera: bool = False


class Drone(BaseModel):
    id: str
    name: str
    battery: float = Field(ge=0, le=100)
    latitude: float
    longitude: float
    status: DroneStatus = DroneStatus.AVAILABLE
    capabilities: DroneCapabilities
    current_mission: str | None = None