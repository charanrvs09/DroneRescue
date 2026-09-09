# 🚁 DroneRescue

### Multi-Agent AI for Autonomous Drone Emergency Response

DroneRescue is an agentic AI platform that enables autonomous drone-based emergency response. It combines multi-agent orchestration, RAG, vision analysis, dynamic replanning, deterministic safety validation, human-in-the-loop approval, and mission memory.

## 🌐 Live Demo

**Frontend:** https://drone-rescue.vercel.app/

**Backend API:** https://dronerescue-api.onrender.com/

**API Health:** https://dronerescue-api.onrender.com/health

### Demo Login
- **Email:** operator@dronerescue.ai
- **Password:** demo123

## ✨ Key Features

- 🤖 Multi-agent emergency response
- 🚁 Intelligent drone fleet selection
- 📚 RAG-based emergency protocol retrieval
- 👁️ RGB and thermal vision analysis
- 🔄 Dynamic mission replanning
- 🛡️ Deterministic Safety Governor
- 🧑‍✈️ Human-in-the-loop authorization
- 💾 Persistent mission memory
- 🖥️ Real-time mission control dashboard
- 🧪 Simulated drone fleet and emergency scenarios

## 🧠 Workflow

```text
Incident
   ↓
Incident Agent
   ↓
Fleet Selection
   ↓
RAG Knowledge Retrieval
   ↓
Mission Planning
   ↓
Safety Governor
   ↓
Drone Execution
   ↓
Vision Analysis
   ↓
Decision
   ↓
Continue / Replan / Human Approval
   ↓
Mission Memory





🛠️ Tech Stack

Frontend: React, Vite, Tailwind CSS
Backend: Python, FastAPI, Pydantic, SQLite
AI: LangGraph, LangChain, RAG, VLM Service
Vector Store: ChromaDB
Deployment: Vercel + Render

🚨 Supported Scenarios

Fire, Chemical Leak, Intrusion, Accident, Structural Damage, Flooding, and Uncertain Visual Observations.

🎯 Core Principle

AI proposes. Deterministic safety logic validates. Humans take control when necessary.

📂 Repository

https://github.com/rvscharan07-cyber/DroneRescue
