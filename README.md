🧠 GreenMesh: Agentic AI Governance System

An Agentic AI ecosystem for intelligent, transparent, and auditable city-scale decision-making — built with multiple autonomous agents collaborating through a shared state graph.
Developed for the Hack N Pitch 2025 hackathon.

🚀 Overview

GreenMesh is a multi-agent AI framework that simulates an intelligent digital twin for smart governance.

Each AI agent acts as an autonomous specialist (like perception, safety, planning, and audit) and together they form an Agentic AI pipeline that can:

Perceive data from environmental sources (CSV / simulated sensors)

Fuse and verify that data for anomalies

Plan optimal actions through reasoning and simulation

Execute plans while maintaining full auditability

Learn from outcomes and continuously improve

The system uses LangGraph-style agent orchestration and Gemini LLM for reasoning and explainability, enabling autonomous coordination between agents.

⚙️ Tech Stack
Layer	Technology Used
Language	Python 3.11
Core Framework	Custom multi-agent orchestration (LangGraph-style)
LLM Provider	Google Gemini (via google-generativeai)
Environment Management	Anaconda
Data	Static CSV stream (simulating IoT sensors)
Storage	JSONL Ledger (blockchain-like audit chain)
Tools	Digital twin simulation, anomaly detection, dispatch system
Version Control	Git + GitHub
🧩 Project Workflow
🔁 Step-by-Step Agent Flow

Perception Agent
Reads raw environmental data (currently from CSV) and normalizes it into structured sensor events.

Fusion Agent
Aggregates recent readings into zone-wise metrics (average water level, garbage index, etc.) and optionally uses the LLM for textual summaries.

Safety Agent
Detects anomalies or spoofing using a simple adversarial detector and marks world state as verified/unverified. LLM explains safety decisions.

Situation Assessor Agent
Interprets the verified world state to identify incidents (e.g., high flood or pollution risk) and assesses severity.

Coalition Agent
Decides which roles or departments should handle each incident (Planner, Executor, Traffic, etc.).

Planner Agent
The “brain” of the system.
Uses Gemini to propose multiple candidate plans (JSON), simulates them with a digital twin tool, ranks by impact and confidence, and generates explainability cards.

Negotiation Agent
Auto-approves or allows human approval of the best plan.

Executor Agent
Executes each step via predefined tools (e.g., dispatch trucks, monitor area).

Audit Agent
Logs every plan and execution result into an immutable ledger (JSONL file) with hash chaining — ensuring transparency and traceability.

Learning Agent
Reads audit logs and suggests planner improvements (e.g., “increase weight on impact by 5%”).

🧠 LangGraph-Style System Architecture

Below is the schematic graph of the agent workflow that represents the LangGraph-like flow of the system:

          ┌──────────────────┐
          │  PerceptionAgent │
          └──────┬───────────┘
                 │
                 ▼
          ┌──────────────────┐
          │   FusionAgent    │
          └──────┬───────────┘
                 │
                 ▼
          ┌──────────────────┐
          │   SafetyAgent    │
          └──────┬───────────┘
                 │
                 ▼
          ┌────────────────────────┐
          │  SituationAssessor     │
          └──────┬─────────────────┘
                 │
                 ▼
          ┌──────────────────┐
          │  CoalitionAgent  │
          └──────┬───────────┘
                 │
                 ▼
          ┌──────────────────┐
          │   PlannerAgent   │
          └──────┬───────────┘
                 │
                 ▼
          ┌──────────────────┐
          │ NegotiationAgent │
          └──────┬───────────┘
                 │
                 ▼
          ┌──────────────────┐
          │  ExecutorAgent   │
          └──────┬───────────┘
                 │
                 ▼
          ┌──────────────────┐
          │   AuditAgent     │
          └──────┬───────────┘
                 │
                 ▼
          ┌──────────────────┐
          │  LearningAgent   │
          └──────────────────┘


All agents operate over a shared state object and communicate implicitly through it.
Each agent contributes domain-specific reasoning while maintaining autonomy and composability.

🧮 Example Output Snapshot (Ledger Entries)

Each decision cycle appends a JSON object to data/ledger.jsonl like:

{
  "ts": 1761477393.1624007,
  "entry": {
    "plan_id": "p1",
    "plan_name": "alert_and_dispatch",
    "rationale": ["water > threshold"],
    "explain_card": "{\"plans\":[{\"id\":\"p1\",\"name\":\"alert_and_dispatch\",\"cost\":100,\"time_min\":30,\"confidence\":0.9}]}",
    "execution": []
  },
  "prev": "1111965be21e64...",
  "hash": "819c6495062466209b88bc7d3b97d7f76aeca9cc5f782d40a572c97e0adfcb2f"
}


This forms an immutable audit trail, similar to a blockchain ledger — ensuring every plan and its justification can be traced.

🧠 Why This Project Stands Out

✅ Fully Agentic Architecture — Multiple autonomous agents collaborating via shared state.
✅ Explainable AI — Every decision and plan is accompanied by a generated Explain Card.
✅ Transparent Ledger System — Blockchain-like append-only audit history.
✅ LLM + Tools Hybrid Reasoning — Gemini provides reasoning; tools perform deterministic simulations.
✅ Extensible Framework — Adding new agents (e.g., Forecasting, Human Feedback) takes minutes.
✅ Modular Codebase — Each agent is isolated, testable, and pluggable.

🧰 How to Run

Clone the Repository

git clone https://github.com/govindaa-sharma/GreenMesh.git
cd GreenMesh


Create and Activate Conda Environment

conda create -n greenmesh python=3.11 -y
conda activate greenmesh


Install Requirements

pip install -r requirements.txt


Add Gemini API Key in .env

GEMINI_API_KEY=your_api_key_here


Run the System

python graph.py

📊 Current Data Source (as of this version)

Right now, GreenMesh uses a static CSV file (data/simulated_sensors.csv) that contains simulated sensor data for water level, garbage index, and air quality.

Each tick in the system reads a new CSV line and treats it as a live sensor reading — giving a controlled simulation environment for agent reasoning and testing.

Example CSV snippet:

timestamp,sensor_id,sensor_type,location,value
1761477000,W001,WaterLevel,ZoneA,2.5
1761477001,G001,GarbageLevel,ZoneB,89.3
1761477002,A001,AirQuality,ZoneC,45.6

🔮 Upcoming Enhancement (Next Commit)

We will replace the static CSV with a synthetic real-time data generator that:

Continuously streams new simulated readings

Occasionally injects anomalies

Optionally merges real API data (OpenAQ / OpenWeatherMap)

Makes the system appear fully live and autonomous

This will make the project demonstrate self-evolving AI collaboration in real-time.

🧑‍💻 Contributors
Name	Role
Govinda Sharma	AI Systems Engineer, Multi-Agent Designer
Teammate	Planner & Backend Integration
🏁 License

This project is licensed under the MIT License — free for educational and research use.

📘 Citation (Hackathon Submission)

GreenMesh: An Agentic AI Governance System for Smart City Coordination
Built using Python, Gemini, and modular autonomous agents for the Hack N Pitch 2025.
