from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.api.drone_routes import router as drone_router
from backend.memory.mission_memory import MissionMemory


app = FastAPI(
    title="DroneRescue API",
    description="Agentic AI platform for autonomous drone emergency response",
    version="0.1.0",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(drone_router)

mission_memory = MissionMemory()


@app.get("/")
def root():
    return {
        "message": "DroneRescue backend is running",
        "version": "0.1.0",
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "services": {
            "api": "operational",
            "drone_simulator": "operational",
            "safety_governor": "operational",
            "rag": "operational",
            "vision": "operational",
            "mission_memory": "operational",
        },
    }