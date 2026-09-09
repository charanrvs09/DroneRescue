from datetime import datetime
from pathlib import Path

from PIL import Image, ImageDraw


CAPTURE_DIR = Path(__file__).parent / "captures"
CAPTURE_DIR.mkdir(exist_ok=True)


def _add_telemetry(
    draw: ImageDraw.ImageDraw,
    drone_id: str,
    sensor: str,
    latitude: float,
    longitude: float,
    timestamp: str,
) -> None:
    draw.text(
        (40, 40),
        f"DroneRescue - {sensor.upper()} CAMERA",
        fill="white",
    )

    draw.text(
        (40, 80),
        f"Drone: {drone_id}",
        fill="white",
    )

    draw.text(
        (40, 120),
        f"Latitude: {latitude:.6f}",
        fill="white",
    )

    draw.text(
        (40, 160),
        f"Longitude: {longitude:.6f}",
        fill="white",
    )

    draw.text(
        (40, 200),
        f"Captured: {timestamp}",
        fill="white",
    )


def _create_rgb_fire_scene(
    drone_id: str,
    latitude: float,
    longitude: float,
) -> str:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")

    filename = f"{drone_id}_rgb_fire_{timestamp}.png"
    filepath = CAPTURE_DIR / filename

    image = Image.new("RGB", (1280, 720), "#536878")
    draw = ImageDraw.Draw(image)

    draw.rectangle(
        (0, 430, 1280, 720),
        fill="#4a4a3a",
    )

    draw.rectangle(
        (350, 250, 930, 500),
        fill="#777777",
    )

    draw.polygon(
        [(300, 250), (640, 150), (980, 250)],
        fill="#555555",
    )

    for x in (430, 560, 690, 820):
        draw.rectangle(
            (x, 310, x + 60, 380),
            fill="#9fb7c5",
        )

    draw.rectangle(
        (600, 400, 680, 500),
        fill="#303030",
    )

    draw.ellipse(
        (580, 180, 760, 400),
        fill="#ff8c00",
    )

    draw.ellipse(
        (610, 210, 730, 370),
        fill="#ffd700",
    )

    draw.ellipse(
        (645, 250, 700, 350),
        fill="#fff2a8",
    )

    for x, y, size in [
        (650, 150, 80),
        (600, 100, 100),
        (700, 80, 120),
        (550, 40, 90),
        (760, 30, 100),
    ]:
        draw.ellipse(
            (
                x - size // 2,
                y - size // 2,
                x + size // 2,
                y + size // 2,
            ),
            fill="#303030",
        )

    _add_telemetry(
        draw,
        drone_id,
        "rgb",
        latitude,
        longitude,
        timestamp,
    )

    image.save(filepath)

    return str(filepath)


def _create_rgb_unclear_scene(
    drone_id: str,
    latitude: float,
    longitude: float,
) -> str:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")

    filename = f"{drone_id}_rgb_unclear_{timestamp}.png"
    filepath = CAPTURE_DIR / filename

    image = Image.new("RGB", (1280, 720), "#777777")
    draw = ImageDraw.Draw(image)

    draw.rectangle(
        (0, 450, 1280, 720),
        fill="#555555",
    )

    draw.rectangle(
        (450, 300, 800, 500),
        fill="#666666",
    )

    draw.ellipse(
        (560, 250, 700, 390),
        fill="#888888",
    )

    _add_telemetry(
        draw,
        drone_id,
        "rgb",
        latitude,
        longitude,
        timestamp,
    )

    image.save(filepath)

    return str(filepath)


def _create_rgb_chemical_leak_scene(
    drone_id: str,
    latitude: float,
    longitude: float,
) -> str:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")

    filename = f"{drone_id}_rgb_chemical_leak_{timestamp}.png"
    filepath = CAPTURE_DIR / filename

    image = Image.new("RGB", (1280, 720), "#66727a")
    draw = ImageDraw.Draw(image)

    # Industrial ground
    draw.rectangle(
        (0, 430, 1280, 720),
        fill="#41484b",
    )

    # Storage tanks
    for x in (300, 500, 700):
        draw.rectangle(
            (x, 250, x + 130, 480),
            fill="#8c9699",
        )

        draw.ellipse(
            (x, 220, x + 130, 280),
            fill="#aab2b5",
        )

    # Chemical spill
    draw.ellipse(
        (520, 450, 850, 610),
        fill="#9acd32",
    )

    draw.ellipse(
        (600, 420, 780, 560),
        fill="#b6e35c",
    )

    # Vapor plume
    for x, y, size in [
        (650, 350, 90),
        (610, 280, 80),
        (690, 220, 100),
    ]:
        draw.ellipse(
            (
                x - size // 2,
                y - size // 2,
                x + size // 2,
                y + size // 2,
            ),
            fill="#d8e6d0",
        )

    _add_telemetry(
        draw,
        drone_id,
        "rgb",
        latitude,
        longitude,
        timestamp,
    )

    image.save(filepath)

    return str(filepath)


def _create_rgb_intrusion_scene(
    drone_id: str,
    latitude: float,
    longitude: float,
) -> str:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")

    filename = f"{drone_id}_rgb_intrusion_{timestamp}.png"
    filepath = CAPTURE_DIR / filename

    image = Image.new("RGB", (1280, 720), "#303b46")
    draw = ImageDraw.Draw(image)

    # Restricted facility
    draw.rectangle(
        (250, 250, 1030, 520),
        fill="#59646c",
    )

    # Fence
    for x in range(220, 1080, 60):
        draw.line(
            (x, 230, x, 560),
            fill="#b7bec2",
            width=3,
        )

    for y in range(260, 560, 60):
        draw.line(
            (220, y, 1080, y),
            fill="#b7bec2",
            width=2,
        )

    # Person
    draw.ellipse(
        (610, 300, 680, 370),
        fill="#202020",
    )

    draw.rectangle(
        (625, 370, 665, 480),
        fill="#202020",
    )

    draw.line(
        (625, 400, 580, 450),
        fill="#202020",
        width=12,
    )

    draw.line(
        (665, 400, 710, 450),
        fill="#202020",
        width=12,
    )

    # Vehicle
    draw.rectangle(
        (780, 430, 930, 490),
        fill="#202020",
    )

    draw.ellipse(
        (800, 470, 835, 505),
        fill="#111111",
    )

    draw.ellipse(
        (875, 470, 910, 505),
        fill="#111111",
    )

    _add_telemetry(
        draw,
        drone_id,
        "rgb",
        latitude,
        longitude,
        timestamp,
    )

    image.save(filepath)

    return str(filepath)


def _create_rgb_accident_scene(
    drone_id: str,
    latitude: float,
    longitude: float,
) -> str:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")

    filename = f"{drone_id}_rgb_accident_{timestamp}.png"
    filepath = CAPTURE_DIR / filename

    image = Image.new("RGB", (1280, 720), "#69747a")
    draw = ImageDraw.Draw(image)

    # Road
    draw.rectangle(
        (0, 250, 1280, 650),
        fill="#303338",
    )

    # Road markings
    for x in range(0, 1280, 180):
        draw.rectangle(
            (x, 440, x + 90, 455),
            fill="#d9d9d9",
        )

    # Damaged vehicle
    draw.polygon(
        [
            (450, 390),
            (600, 330),
            (800, 350),
            (880, 430),
            (820, 500),
            (560, 490),
        ],
        fill="#a83b32",
    )

    draw.rectangle(
        (550, 350, 720, 430),
        fill="#5f7785",
    )

    # Person near accident
    draw.ellipse(
        (350, 470, 400, 520),
        fill="#202020",
    )

    draw.line(
        (375, 520, 375, 610),
        fill="#202020",
        width=15,
    )

    draw.line(
        (375, 545, 330, 580),
        fill="#202020",
        width=10,
    )

    draw.line(
        (375, 545, 420, 580),
        fill="#202020",
        width=10,
    )

    _add_telemetry(
        draw,
        drone_id,
        "rgb",
        latitude,
        longitude,
        timestamp,
    )

    image.save(filepath)

    return str(filepath)


def _create_rgb_structural_damage_scene(
    drone_id: str,
    latitude: float,
    longitude: float,
) -> str:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")

    filename = f"{drone_id}_rgb_structural_damage_{timestamp}.png"
    filepath = CAPTURE_DIR / filename

    image = Image.new("RGB", (1280, 720), "#59656b")
    draw = ImageDraw.Draw(image)

    # Building
    draw.rectangle(
        (300, 180, 980, 570),
        fill="#7c8285",
    )

    # Damaged section
    draw.polygon(
        [
            (650, 180),
            (980, 180),
            (980, 570),
            (760, 500),
            (700, 380),
        ],
        fill="#4e5356",
    )

    # Cracks
    crack_lines = [
        [(520, 220), (550, 300), (510, 390), (560, 470)],
        [(650, 240), (620, 330), (680, 400), (640, 520)],
        [(820, 220), (780, 300), (840, 380), (790, 480)],
    ]

    for points in crack_lines:
        draw.line(
            points,
            fill="#252525",
            width=8,
        )

    # Fallen debris
    for x, y, w, h in [
        (250, 540, 100, 50),
        (390, 560, 120, 40),
        (850, 560, 140, 45),
    ]:
        draw.rectangle(
            (x, y, x + w, y + h),
            fill="#454545",
        )

    _add_telemetry(
        draw,
        drone_id,
        "rgb",
        latitude,
        longitude,
        timestamp,
    )

    image.save(filepath)

    return str(filepath)


def _create_rgb_flooding_scene(
    drone_id: str,
    latitude: float,
    longitude: float,
) -> str:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")

    filename = f"{drone_id}_rgb_flooding_{timestamp}.png"
    filepath = CAPTURE_DIR / filename

    image = Image.new("RGB", (1280, 720), "#607d8b")
    draw = ImageDraw.Draw(image)

    # Flood water
    draw.rectangle(
        (0, 300, 1280, 720),
        fill="#2f6f91",
    )

    # Road partially submerged
    draw.polygon(
        [
            (0, 430),
            (1280, 350),
            (1280, 500),
            (0, 600),
        ],
        fill="#455a64",
    )

    # Buildings
    for x in (250, 600, 900):
        draw.rectangle(
            (x, 170, x + 180, 450),
            fill="#858585",
        )

        for wx in (x + 30, x + 100):
            draw.rectangle(
                (wx, 230, wx + 40, 290),
                fill="#9db6c4",
            )

    # Floating debris
    for x, y in [
        (180, 570),
        (430, 500),
        (720, 590),
        (1040, 470),
    ]:
        draw.rectangle(
            (x, y, x + 80, y + 30),
            fill="#765a3a",
        )

    _add_telemetry(
        draw,
        drone_id,
        "rgb",
        latitude,
        longitude,
        timestamp,
    )

    image.save(filepath)

    return str(filepath)


def _create_thermal_fire_scene(
    drone_id: str,
    latitude: float,
    longitude: float,
) -> str:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")

    filename = f"{drone_id}_thermal_fire_{timestamp}.png"
    filepath = CAPTURE_DIR / filename

    image = Image.new("RGB", (1280, 720), "#101010")
    draw = ImageDraw.Draw(image)

    draw.rectangle(
        (350, 250, 930, 500),
        fill="#202060",
    )

    draw.polygon(
        [(300, 250), (640, 150), (980, 250)],
        fill="#303080",
    )

    draw.ellipse(
        (560, 170, 780, 410),
        fill="#ff4500",
    )

    draw.ellipse(
        (610, 210, 730, 370),
        fill="#ff8c00",
    )

    draw.ellipse(
        (645, 250, 700, 350),
        fill="#ffff00",
    )

    _add_telemetry(
        draw,
        drone_id,
        "thermal",
        latitude,
        longitude,
        timestamp,
    )

    image.save(filepath)

    return str(filepath)


def capture_rgb_frame(
    drone_id: str,
    latitude: float,
    longitude: float,
    scenario: str = "normal",
) -> str:

    scenario = scenario.lower()

    if scenario == "fire":
        return _create_rgb_fire_scene(
            drone_id,
            latitude,
            longitude,
        )

    if scenario == "unclear":
        return _create_rgb_unclear_scene(
            drone_id,
            latitude,
            longitude,
        )

    if scenario == "chemical_leak":
        return _create_rgb_chemical_leak_scene(
            drone_id,
            latitude,
            longitude,
        )

    if scenario == "intrusion":
        return _create_rgb_intrusion_scene(
            drone_id,
            latitude,
            longitude,
        )

    if scenario == "accident":
        return _create_rgb_accident_scene(
            drone_id,
            latitude,
            longitude,
        )

    if scenario == "structural_damage":
        return _create_rgb_structural_damage_scene(
            drone_id,
            latitude,
            longitude,
        )

    if scenario == "flooding":
        return _create_rgb_flooding_scene(
            drone_id,
            latitude,
            longitude,
        )

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")

    filename = f"{drone_id}_rgb_{timestamp}.png"
    filepath = CAPTURE_DIR / filename

    image = Image.new(
        "RGB",
        (1280, 720),
        "black",
    )

    draw = ImageDraw.Draw(image)

    _add_telemetry(
        draw,
        drone_id,
        "rgb",
        latitude,
        longitude,
        timestamp,
    )

    image.save(filepath)

    return str(filepath)


def capture_thermal_frame(
    drone_id: str,
    latitude: float,
    longitude: float,
    scenario: str = "normal",
) -> str:

    if scenario.lower() == "fire":
        return _create_thermal_fire_scene(
            drone_id,
            latitude,
            longitude,
        )

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")

    filename = f"{drone_id}_thermal_{timestamp}.png"
    filepath = CAPTURE_DIR / filename

    image = Image.new(
        "RGB",
        (1280, 720),
        "black",
    )

    draw = ImageDraw.Draw(image)

    _add_telemetry(
        draw,
        drone_id,
        "thermal",
        latitude,
        longitude,
        timestamp,
    )

    image.save(filepath)

    return str(filepath)