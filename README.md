


🚁 DroneRescue — Multi-Agent AI for Autonomous Drone Emergency Response
An agentic AI platform that coordinates autonomous drones for emergency response using multi-agent planning, RAG, vision analysis, dynamic replanning, deterministic safety controls, human-in-the-loop authorization, and persistent mission memory.





🌐 Live Demo
Component	Link
Mission Control — Frontend	https://drone-rescue.vercel.app/
DroneRescue API — Backend	https://dronerescue-api.onrender.com/
API Health Check	https://dronerescue-api.onrender.com/health
Demo Login
Email: operator@dronerescue.ai
Password: demo123
The login is a lightweight demo gate for the prototype UI, not a production authentication system.

🎯 Problem
Emergency response teams often need rapid situational awareness before sending people into hazardous environments.

A drone can provide aerial intelligence, but a useful autonomous response system needs to answer several questions:

Which drone should respond?

Does it have enough battery?

What sensors does it have?

What operational procedure applies?

Is the planned flight safe?

What does the aerial imagery show?

What should happen if the visual evidence is uncertain?

When should autonomy stop and a human take over?

How can previous mission decisions be retained?

DroneRescue addresses these problems through a controlled multi-agent workflow.

🧠 Core Idea
The system treats an emergency mission as a closed-loop decision process, rather than a single AI request.

Incident
   │
   ▼
┌────────────────────┐
│  Incident Agent    │
└─────────┬──────────┘
          ▼
┌────────────────────┐
│   Fleet Agent      │──────► Drone Status / Capabilities
└─────────┬──────────┘
          ▼
┌────────────────────┐
│ Knowledge / RAG     │─────► Emergency Protocols
└─────────┬──────────┘
          ▼
┌────────────────────┐
│  Mission Planner   │
└─────────┬──────────┘
          ▼
┌────────────────────┐
│ Safety Governor    │
│  Deterministic     │
└──────┬────────┬────┘
       │        │
     SAFE     UNSAFE
       │        │
       ▼        ▼
   Execute    Human /
              Fallback
       │
       ▼
┌────────────────────┐
│ Drone Simulator    │
└─────────┬──────────┘
          ▼
   RGB / Thermal
          │
          ▼
┌────────────────────┐
│ Vision Analysis    │
└─────────┬──────────┘
          ▼
┌────────────────────┐
│ Decision Agent     │
└──────┬────────┬────┘
       │        │
   Continue   Replan
       │        │
       └────┬───┘
            ▼
      Mission Memory
🤖 Multi-Agent Architecture
1. Incident Agent
Normalizes the incoming emergency report into a structured mission request.

Responsibilities

Identify incident type

Extract location

Normalize incident metadata

Create the initial mission context

2. Fleet Agent
Selects the most appropriate drone from the simulated fleet.

It considers:

Battery level

Availability

Location

RGB capability

Thermal capability

Current mission state

Example fleet:

Drone	Battery	Status	RGB	Thermal
Rescue-01 (D1)	85%	Available	✓	✓
Rescue-02 (D2)	63%	Available	✓	✗
Rescue-03 (D3)	91%	Inspecting	✓	✓
3. Knowledge / RAG Agent
Retrieves operational guidance from the mission knowledge base.

Current knowledge sources include:

knowledge_base/
├── battery_policy.txt
├── drone_safety.txt
├── emergency_response.txt
├── fire_protocol.txt
└── security_protocol.txt
The retrieved guidance is attached to the mission planning context instead of relying only on model memory.

4. Mission Agent
Converts the incident and operational guidance into executable mission steps.

Example:

1. Takeoff
2. Navigate to incident
3. Capture RGB imagery
4. Analyze evidence
5. Perform additional inspection if required
6. Return home
5. Safety Governor
The Safety Governor is intentionally deterministic.

AI agents do not directly bypass the safety layer to control the simulated drone.

It validates actions against constraints such as:

Minimum battery thresholds

Geofence

Drone availability

Thermal sensor capability

Required coordinates

Action-specific safety rules

Example:

AI Agent
   │
   ▼
Proposed Drone Action
   │
   ▼
Safety Governor
   │
   ├── APPROVED ──► Drone Simulator
   │
   └── BLOCKED ───► Fallback / Human Review
This separation is a key design principle:

AI proposes. Deterministic safety logic disposes.

6. Vision Analysis
The vision layer analyzes captured aerial imagery and returns structured observations:

{
  "incident_type": "fire",
  "confidence": 0.94,
  "severity": "high",
  "summary": "A fire incident is visible...",
  "evidence": [
    "Visible flames",
    "Smoke plume detected",
    "Structure appears affected"
  ],
  "recommended_action": "Perform thermal inspection"
}
The current prototype includes a deterministic vision fallback so the complete workflow remains runnable without external VLM API credits.

The service is structured behind a VLMService abstraction so a production vision model can be plugged in later.

7. Decision Agent
The Decision Agent converts vision results into the next operational decision.

Examples:

Vision Result	Decision
Confidence < 60%	Re-capture / Replan
Fire detected	Thermal inspection
Chemical leak	Remote hazard inspection
Intrusion	Aerial surveillance
Accident	Scene assessment
Structural damage	Structural inspection
Flooding	Flood mapping
This makes the vision output behaviorally meaningful instead of merely displaying an AI-generated description.

8. Replanning Agent
When the vision system is uncertain, the mission does not blindly continue.

Instead:

Low Confidence
      │
      ▼
Reposition / Recapture
      │
      ▼
Vision Analysis
      │
   ┌──┴──┐
   ▼     ▼
Confident  Still Unclear
   │           │
   ▼           ▼
Continue    Human Review
Automatic replanning is bounded to prevent uncontrolled autonomous loops.

9. Human-in-the-Loop Authorization
High-risk or unresolved missions can transition to:

AWAITING HUMAN APPROVAL
The operator can:

Approve continuation

Reject the action

Trigger a safe fallback

For example, an uncertain fire mission can require operator authorization before thermal verification.

This provides bounded autonomy rather than unrestricted autonomy.

10. Mission Memory
Mission state is persisted in SQLite.

Stored information includes:

Mission ID

Drone ID

Incident type

Mission status

Replan count

Observations

Decisions

Creation time

This allows the Mission Ledger to show historical mission activity.

🔄 Example Mission
Fire Emergency
1. Fire incident received
              ↓
2. Fleet Agent selects D1
              ↓
3. RAG retrieves Fire Protocol
              ↓
4. Mission Planner creates mission
              ↓
5. Safety Governor validates actions
              ↓
6. Drone takes off and reaches incident
              ↓
7. RGB image captured
              ↓
8. Vision confidence = 35%
              ↓
9. Decision Agent requests recapture
              ↓
10. Replanning Agent performs bounded replan
              ↓
11. Evidence remains uncertain
              ↓
12. Human authorization requested
              ↓
13. Operator approves continuation
              ↓
14. Thermal verification performed
              ↓
15. Drone returns home
              ↓
16. Mission stored in Mission Ledger
This demonstrates the key agentic behavior:

Observe → Decide → Act → Re-observe → Replan → Escalate when necessary.

🖥️ Mission Control Dashboard
The frontend is designed as an operational command interface rather than a generic CRUD dashboard.

Dashboard includes
Live operations header

Geospatial operations map

Drone telemetry

Fleet status

Emergency dispatch

Incident selection

Autonomous intelligence pipeline

Vision confidence

Safety Governor status

Human authorization state

Mission ledger

Persistent mission history

🏗️ Project Structure
DroneRescue/
│
├── backend/
│   ├── agents/
│   │   ├── decision_agent.py
│   │   ├── fleet_agent.py
│   │   ├── human_approval.py
│   │   ├── incident_agent.py
│   │   ├── knowledge_agent.py
│   │   ├── mission_agent.py
│   │   ├── mission_executor.py
│   │   ├── mission_memory.py
│   │   ├── mission_state.py
│   │   ├── orchestrator.py
│   │   ├── replanning_agent.py
│   │   ├── response_agent.py
│   │   └── vision_loop.py
│   │
│   ├── api/
│   │   └── drone_routes.py
│   │
│   ├── memory/
│   │   └── mission_memory.py
│   │
│   ├── rag/
│   │   └── rag_service.py
│   │
│   ├── safety/
│   │   └── safety_governor.py
│   │
│   ├── vision/
│   │   └── vlm_service.py
│   │
│   ├── drone_simulator/
│   │   ├── camera.py
│   │   ├── fleet.py
│   │   ├── models.py
│   │   └── simulator.py
│   │
│   ├── knowledge_base/
│   │   ├── battery_policy.txt
│   │   ├── drone_safety.txt
│   │   ├── emergency_response.txt
│   │   ├── fire_protocol.txt
│   │   └── security_protocol.txt
│   │
│   ├── main.py
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   └── App.jsx
│   ├── package.json
│   └── vite.config.js
│
├── .gitignore
└── README.md
🛠️ Technology Stack
Frontend
React

Vite

Tailwind CSS

Modern responsive dashboard UI

Backend
Python

FastAPI

Pydantic

SQLite

HTTPX

Agentic AI
LangGraph

LangChain

Agent-based orchestration

Decision loops

Human-in-the-loop workflows

Retrieval
ChromaDB

RAG knowledge retrieval

Vision
VLM service abstraction

RGB and thermal image simulation

Structured vision analysis

Confidence-driven decisions

Drone Layer
Custom drone simulator

Simulated fleet

Mission execution APIs

RGB / thermal sensors

Battery and geofence constraints

Deployment
Vercel — frontend

Render — backend

🚀 Run Locally
1. Clone
git clone https://github.com/rvscharan07-cyber/DroneRescue.git
cd DroneRescue
2. Backend
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
Start the API:

uvicorn backend.main:app --reload
Backend:

http://127.0.0.1:8000
Health check:

http://127.0.0.1:8000/health
3. Frontend
Open another terminal:

cd frontend
npm install
npm run dev
Frontend:

http://localhost:5173
4. Configure API URL
Create:

frontend/.env
Add:

VITE_API_URL=http://127.0.0.1:8000
🔐 Safety Philosophy
DroneRescue is designed around bounded autonomy.

The AI system can:

Interpret an incident

Select a drone

Retrieve procedures

Plan a mission

Analyze imagery

Decide whether to continue or replan

But safety-critical execution is still passed through deterministic controls.

                 AI
                  │
         ┌────────▼────────┐
         │ Proposed Action │
         └────────┬────────┘
                  │
         ┌────────▼────────┐
         │ Safety Governor │
         └────────┬────────┘
                  │
        ┌─────────┴─────────┐
        ▼                   ▼
     Approved              Blocked
        │                   │
        ▼                   ▼
  Drone Execution      Human/Fallback
This architecture is intended to make autonomous systems more predictable, auditable, and controllable.

📊 Observability
The dashboard exposes important mission state rather than treating the agent as a black box.

Operators can see:

Current mission

Selected drone

Vision confidence

Retrieved knowledge source

Agent decisions

Safety status

Replanning count

Human authorization state

Historical mission records

🧪 Supported Incident Scenarios
The simulator supports:

🔥 Fire

☣️ Chemical leak

🚨 Intrusion

🚑 Accident / medical response

🏗️ Structural damage

🌊 Flooding

❓ Unclear / low-confidence observations

🧑‍✈️ Persistent uncertainty requiring human review

🔮 Future Production Extensions
The current system is intentionally simulator-first. A production implementation could replace the simulated components with:

Real drone fleet APIs

MAVLink / PX4 / ArduPilot integration

Real-time telemetry streams

Production VLMs

Live thermal cameras

Weather APIs

Dynamic no-fly-zone data

PostGIS/geospatial storage

Redis/Kafka event streaming

PostgreSQL mission memory

Enterprise authentication and RBAC

Stronger audit logging

Cloud object storage for imagery

Real-time WebSocket mission updates

The architecture is designed so these components can be introduced without changing the core safety and decision flow.

🎓 Why This Project Matters
DroneRescue demonstrates more than simply calling an LLM.

It combines:

Multi-agent orchestration + RAG + vision + planning + tool execution + safety constraints + dynamic replanning + human oversight + persistent memory.

The important design principle is:

Autonomy should be useful, explainable, bounded, and interruptible.

👨‍💻 Author
Charan Rvs

Built as an Agentic AI engineering project focused on autonomous drone operations and emergency response.

📄 License
This project is available under the MIT License.
