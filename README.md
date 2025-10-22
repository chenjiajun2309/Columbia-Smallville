# Columbia Smallville
> LLM-driven multi-agent campus simulator for **memory**, **reflection**, **planning**, **action**, and **interaction** — with optional **RL policy heads** and **discriminator rewards (GAIL/DRAIL)**.

![python](https://img.shields.io/badge/Python-3.10+-blue)
![fastapi](https://img.shields.io/badge/FastAPI-API-green)
![react](https://img.shields.io/badge/React-Frontend-informational)
![pgvector](https://img.shields.io/badge/pgvector-embeddings-critical)
![license](https://img.shields.io/badge/License-MIT-black)

**Columbia Smallville** is a university-campus multi-agent simulation platform.  
Each agent is powered by a large language model (e.g., GPT-4 or API-compatible models) and equipped with **memory, reflection, planning, action, and social interaction**.  
Optionally, agents can mount **small-model policy heads** (LoRA/BC/Offline RL/Online RL) to learn specific behavior patterns and connect to **GAIL/DRAIL-style discriminator rewards**.

This project targets three goals:

1. **Research** — emergent campus society, information diffusion, and norm following.  
2. **Reinforcement Learning** — bridge from LLM “high-level cognition” to trainable “low-level policies”.  
3. **Application** — a reusable multi-agent environment (PettingZoo/Gymnasium compatible).

---

## ✨ Key Features

- **Campus World**: 2D campus map (classrooms, libraries, cafeterias, dorms, plazas), discrete-event scheduler, location capacity & queuing.
- **LLM Agent Stack**: three-tier memory (short-term / episodic / social) + reflection; ReAct decision loop; Top-k memory retrieval by **relevance / importance / recency**.
- **Tool Calls**: `move / talk / attend / buy / study / post / schedule / search` with an execution layer that validates constraints and returns failure feedback.
- **Data & Visualization**: PostgreSQL + pgvector to store memories/trajectories; event streams, social graphs, location heatmaps, daily diaries & summaries.
- **Trainable Modules (optional)**:
  - **Behavior Cloning / LoRA** for micro-behaviors like punctuality, queueing, courtesy, and study focus.
  - **Offline RL** (IQL/CQL, etc.) and **Online RL** (PPO/SAC, etc.).
  - **Discriminator Rewards**: standard GAIL `log(D) - log(1 - D)`; switchable **DRAIL diffusion discriminator** for smoother rewards.
- **Standardized APIs**: PettingZoo/Gymnasium adapters for plug-and-play with RL libraries.

---

## 🧭 Architecture Overview

[Frontend (React/Phaser)]
│
[FastAPI Gateway]
│
[Simulation Core: Discrete-Event Scheduler + World State]
├─ Tools (move/talk/post/...)
├─ Agent Runtime
│ ├─ Memory (vector store) / Reflection
│ ├─ Planner (ReAct)
│ └─ LLM Controller + Small-Model Policy Head (optional)
└─ RL Adapter (PettingZoo/Gymnasium)
│
[Storage: PostgreSQL + pgvector] + [Redis queues/cache]
[Training Sandbox: BC / Offline RL / Online RL + Discriminator (GAIL/DRAIL)]


---

## 🗂️ Repository Structure

├── sim-core/ # Simulation engine: world, scheduler, tools, adapters
├── agents/ # Memory/retrieval/reflection, ReAct planner, personas, prompts
├── api/ # FastAPI services and routes
├── frontend/ # React/Phaser 2D visualization
├── storage/ # DB schema, pgvector setup, migrations
├── training/ # LoRA/BC/Offline/Online RL, discriminator (GAIL/DRAIL)
├── datasets/ # Synthetic/recorded expert demonstrations & trajectories
├── scripts/ # Bootstrap, evaluation, data generation, replay
└── docs/ # Design docs, metrics dashboards, figures


---

## 🚀 Quick Start

### 1) Requirements
- Python **3.10+**, Node **18+**, PostgreSQL **14+** (with `pgvector` installed)  
- Or use **Docker Compose** for a one-command setup (`docker-compose.yml`)

### 2) Installation
```bash
git clone https://github.com/<your-org>/columbia-smallville.git
cd columbia-smallville
cp .env.example .env         # Fill in OPENAI_API_KEY or a compatible LLM endpoint
make setup                   # Or: pip install -r requirements.txt && npm --prefix frontend i
```
### 3) Initialize Database
make db.up        # Start Postgres (or: docker compose up -d db)
make db.init      # Create tables and pgvector indexes
### 4) Launch Services & Frontend
make api.up       # uvicorn api.main:app --reload
make web.up       # npm --prefix frontend run dev
### 5) Run a Minimal Simulation
python scripts/bootstrap_world.py              # Load campus POIs, classes, events
python scripts/run_sim.py --agents 25 --hours 24
### 6) Optional: Training & Discriminator
# Generate "expert demos" (simulated by LLM) and export JSONL/Parquet
python training/generate_experts.py --days 7 --persons 30
# Behavior Cloning + LoRA
python training/train_bc_lora.py --dataset datasets/experts.parquet --out ckpts/bc_lora
# Offline RL (e.g., IQL)
python training/train_iql.py --dataset datasets/experts.parquet
# Online PPO (via PettingZoo adapter)
python training/train_ppo.py --env CampusParallel-v0
# Discriminator rewards (GAIL / DRAIL)
python training/train_disc.py --algo gail     # or --algo drail

## 🧠 Agent Capabilities
- **Memory**: Events, dialogues, and relationships stored as natural language + metadata + embeddings.
- **Retrieval**: Top-k memory injection weighted by relevance × importance × recency.
- **Reflection**: Threshold-triggered high-level summaries (e.g., “I’m rushing an ML assignment; reduce social time”).
- **Plan & Execute**: ReAct loop generates micro-plans, invokes tools, and retries on failures.
- **Social**: Build relationships, send/accept invites, model information diffusion and RSVP funnels.

## 📊 Evaluation Metrics
- **City-level**: class/event attendance, location heatmaps, information diffusion speed, norm-violation rate (lateness, queue cutting, noise).
- **Individual-level**: schedule adherence, task latency, memory-reference rate, courtesy/cooperation score.
- **A/B Baselines**: Base vs +BC/Offline RL vs +Online RL vs +Discriminator (DRAIL).

## 🛠️ Team Roles (Example)
- **A — Systems & Backend**: simulation core, tool executor, API, visualization, DB/pgvector.
- **B — Cognition & Prompts**: memory/retrieval/reflection, ReAct, personas & social layer, class/event generators.
- **C — Training & Discriminator**: synthetic demos, LoRA/BC/Offline RL, online RL (PPO), GAIL/DRAIL.

## 🔒 Ethics & Safety
- For research and education only — not affiliated with Columbia University.
- Enable content filtering, logging, and privacy redaction for public demos.
- Clearly distinguish simulated agents from real individuals; no impersonation.

## 🗺️ Roadmap
- **MVP**: 25+ agents, visualization, memory/reflection, social diffusion, daily diaries
- **RL Plugins**: BC → Offline RL (IQL/CQL) → Online RL (PPO)
- **Discriminator Rewards**: GAIL → DRAIL (diffusion discriminator)
- **Analytics Dashboard & Replay System**
- **Large-Scale Simulation**: 50–100 agents

## 📚 References
- **Generative Agents** — memory-reflection-planning paradigm
- **ReAct** — reasoning-and-acting loop for tool-using agents
- **PettingZoo / Gymnasium** — environment standards for (multi-)agent RL
- **DRAIL** — diffusion-reward adversarial imitation learning

## 📄 License
MIT


