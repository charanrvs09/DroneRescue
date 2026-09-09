import json
import sqlite3
from datetime import datetime
from pathlib import Path


class MissionMemory:
    """
    Persistent SQLite storage for DroneRescue missions.
    """

    def __init__(
        self,
        database_path: str = "backend/memory/drone_rescue.db",
    ):
        self.database_path = Path(database_path)

        self.database_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        self._initialize_database()

    def _connect(self):
        return sqlite3.connect(
            self.database_path
        )

    def _initialize_database(self):
        with self._connect() as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS missions (
                    mission_id TEXT PRIMARY KEY,
                    drone_id TEXT NOT NULL,
                    incident_type TEXT NOT NULL,
                    status TEXT NOT NULL,
                    replans INTEGER NOT NULL,
                    observations TEXT NOT NULL,
                    decisions TEXT NOT NULL,
                    created_at TEXT NOT NULL
                )
                """
            )

    def save_mission(
        self,
        state,
    ) -> None:
        with self._connect() as connection:
            connection.execute(
                """
                INSERT OR REPLACE INTO missions (
                    mission_id,
                    drone_id,
                    incident_type,
                    status,
                    replans,
                    observations,
                    decisions,
                    created_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    state.mission_id,
                    state.drone_id,
                    state.incident_type,
                    state.status,
                    state.replans,
                    json.dumps(state.observations),
                    json.dumps(state.decisions),
                    datetime.now().isoformat(),
                ),
            )

    def get_mission(
        self,
        mission_id: str,
    ) -> dict | None:
        with self._connect() as connection:
            cursor = connection.execute(
                """
                SELECT
                    mission_id,
                    drone_id,
                    incident_type,
                    status,
                    replans,
                    observations,
                    decisions,
                    created_at
                FROM missions
                WHERE mission_id = ?
                """,
                (mission_id,),
            )

            row = cursor.fetchone()

        if row is None:
            return None

        return {
            "mission_id": row[0],
            "drone_id": row[1],
            "incident_type": row[2],
            "status": row[3],
            "replans": row[4],
            "observations": json.loads(row[5]),
            "decisions": json.loads(row[6]),
            "created_at": row[7],
        }

    def get_all_missions(
        self,
        limit: int = 20,
    ) -> list[dict]:
        with self._connect() as connection:
            cursor = connection.execute(
                """
                SELECT
                    mission_id,
                    drone_id,
                    incident_type,
                    status,
                    replans,
                    observations,
                    decisions,
                    created_at
                FROM missions
                ORDER BY created_at DESC
                LIMIT ?
                """,
                (limit,),
            )

            rows = cursor.fetchall()

        missions = []

        for row in rows:
            missions.append(
                {
                    "mission_id": row[0],
                    "drone_id": row[1],
                    "incident_type": row[2],
                    "status": row[3],
                    "replans": row[4],
                    "observations": json.loads(row[5]),
                    "decisions": json.loads(row[6]),
                    "created_at": row[7],
                }
            )

        return missions