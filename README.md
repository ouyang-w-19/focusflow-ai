## FocusFlow AI – Repo Overview

A productivity-focused AI agent system that helps users plan tasks, sync with Microsoft 365, and journal progress via a chat-based UI.

---


## Repository Structure

```
focusflow-ai/
│
├── agents/                   # Agent logic and orchestration
│   ├── frontend_agent/
│   │   ├── __init__.py
│   │   ├── frontend_agent.py
│   │   ├── intent_detector.py
│   │   ├── field_collector.py
│   │   ├── dialog_manager.py
│   │   ├── dispatcher.py
│   ├── base_agent.py
│   ├── planning_agent.py
│   ├── journal_agent.py
│   ├── goal_tracker_agent.py
│   └── orchestrator.py       # Routing controller (not a LLM agent)
│
├── llm/                      # Local or remote LLM integration
│   └── llm_wrapper.py        # Unified interface for Qwen2:7B or GPT-4
│
├── graph/                    # Graph API wrappers
│   └── todo.py               # Task list, create/read/update tasks
│
├── auth/                     # Microsoft Graph API auth via MSAL
│   └── ms_graph_auth.py
│
├── prompts/                  # Prompt templates for journaling & planning
│   ├── journal.txt
│   └── planner.txt
│
├── ui/                       # Streamlit app logic
│   └── app.py
│
├── tests/                    # Test scripts for agents and API wrappers
│   ├── test_ollama.py
│   ├── test_task_agent.py
│   └── test_graph_todo.py
│
├── data/                     # Local cache (SQLite or JSON)
│   ├── tasks.db              # Or tasks.json
│   └── journals/
│       └── 2025-04-16.json
│
├── config.py                 # Loads secrets from .env
├── .env                      # Contains client_id, tenant_id, secret (not committed)
├── .env.example              # Template for team use
├── .gitignore                # Ignores secrets, cache, compiled files
├── requirements.txt          # Python dependencies
├── run.py                    # Entrypoint: launches Streamlit UI
└── README.md
```

### Environment Variables

Use `.env.example` as a template:
```bash
cp .env.example .env
```
Update with credentials:
```env
APPLICATION_CLIENT_ID=...
CLIENT_SECRET_VALUE=...
DIRECTORY_TENANT_ID=...
SCOPES=https://graph.microsoft.com/.default
USER_ID=...   # Used for client credentials flow
```

---

### How to Run It Locally

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the Streamlit UI
python run.py

# 3. Optionally test To Do API integration
python -m tests.test_graph_todo
```

---

### Microsoft Graph API Integration

**Current State:**
- Authentication via `msal` (client credentials flow)
- Task list reading and creation available via `graph/todo.py`
- Testing via `tests/test_graph_todo.py`

**Limitation:**
- Microsoft To Do API requires **delegated (user) permissions** — app-only token returns `401 Access Denied`

**Planned Fix:**
- Migrate to **authorization code flow** with user login
- Use `/me/todo/lists` endpoints
- Add delegated permissions in Azure: `Tasks.ReadWrite`, `User.Read`, `offline_access`

**Request Made:**
- We’ve asked the teammate who set up the dev account to approve shared testing access and provide credentials if allowed

---

### Repo Security Notes
- `.env`, `.json`, `.db` are ignored by Git
- Repo is **private** during development; will be made **public** upon cleanup before submission

---

### Contributions & Modules Actively Maintained
- Agent logic (task breakdown)
- Graph API (To Do integration)
- Streamlit UI prototype

Journaling, nudging, and delegated authentication are in progress.



### Modular Agent System

FocusFlow AI is organized using a multi-agent architecture. Each agent is responsible for a specific domain of productivity (planning, journaling, goal tracking, etc.) and communicates through a structured input/output format.

#### agents/
| File                     | Description |
|--------------------------|-------------|
| base_agent.py            | Base class for all LLM agents (shared logic, memory) |
| planning_agent.py        | Plans, breaks down tasks, suggests time blocks |
| journal_agent.py         | Placeholder for reflection/journaling agent |
| goal_tracker_agent.py    | Placeholder for goal/habit tracking agent |
| orchestrator.py          | Non-agent controller for routing structured input to domain agents |


#### agents/frontend_agents/
```
+-----------------+                    +-----------------+                  +------------------+
|  User Interface |  <--Input/Reply--> | FrontendAgent   | --> Dispatch --> | Orchestrator     |
+-----------------+                    +-----------------+                  +------------------+
                                          |
                                          |
                        +-----------------+-----------------+
                        |                                   |
              +------------------+           +--------------------+
              |  Intent Detector  |          | Dialog Manager      |
              +------------------+           +--------------------+
                       |                                 |
            (LangChain agent chain)           (stores collected fields)
                       |                                 |
              +------------------+           +--------------------+
              |  Field Collector  |  <---
              +------------------+
                       |
            (LangChain agent chain with short-term context)
                       |
              +------------------+
              | Dispatcher (API client) |
              +------------------+
                       |
              +------------------+
              | LLMWrapper       |
              +------------------+
```

#### llm/
| File              | Description |
|-------------------|-------------|
| llm_wrapper.py    | Wraps access to Qwen2:7B (Ollama) and optionally GPT-4 (Azure); used across agents |