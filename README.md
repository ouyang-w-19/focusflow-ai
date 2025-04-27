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
│   ├── productivity_agent/   # <-- NEW
│   │   ├── __init__.py
│   │   ├── productivity_agent.py   # Core class: ProductivityAgent
│   │   ├── tools.py                # LangChain Tools wrapping agent methods
│   │   ├── session_handler.py      # Planning session manager
│   │   ├── planner_prompt.txt      # Optional: planner specific prompts
│   └── orchestrator.py       # Routing controller (not a LLM agent)
│
├── llm/                      # Local or remote LLM integration
│   └── llm_wrapper.py        # Unified interface for Qwen2:7B or GPT-4
│
├── schemas/
│   ├── planning_schema.json
│   ├── goal_tracking_schema.json
│   ├── habit_building_schema.json
│   ├── retrospectives_schema.json
│   ├── time_auditing_schema.json
│   ├── obstacle_management_schema.json
│   ├── vision_mission_definition_schema.json
│
├── graph/                    # Graph API wrappers
│   └── todo.py               # Task list, create/read/update tasks
│
├── auth/                     # Microsoft Graph API auth via MSAL
│   └── ms_graph_auth.py
│
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
│   ├── tasks.json            # Task storage
│   ├── plans.json            # Plan storage
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
- ProductivityAgent (plan management, task breakdown, prioritization, scheduling)
- Graph API (To Do and Calendar integration hooks prepared)
- Streamlit UI prototype (todo)
- FrontendAgent orchestration (intent detection, field collection)

Journaling agent design and basic Microsoft Graph delegated authentication are planned next. 



## Modular Agent System

FocusFlow AI is organized using a multi-agent architecture. Each agent is responsible for a specific domain of productivity (planning, journaling, goal tracking, etc.) and communicates through a structured input/output format.

### agents/frontend_agents/
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

#### FrontendAgent Features

- **Single-intent detection**: Detects and handles the first primary intent from user input.
- **Field prefill**: Extracts structured fields directly from user input before asking questions.
- **Conversational data collection**: Asks polite, natural questions only for missing fields.
- **Answer validation and hinting**: Validates user responses, provides smart hints if answers are incomplete.
- **Session management**: Tracks all collected fields in a dialog memory and prints a session summary.
- **Seamless fallback**: Handles both structured and unstructured intents cleanly.
- **Extensible design**: Modular structure ready for specialized agents for free-form conversation.

### agents/productivity_agent

ProductivityAgent is responsible for:

- Managing high-level **Plans** (`plans.json`)
- Managing actionable **Tasks** (`tasks.json`)
- Building **in-memory indexes** for fast search
- Conducting **conversational planning sessions** with user
- Providing **task scheduling and prioritization** support
- Offering **follow-up questions** for a natural flow

---

#### Files and Storage

| File | Purpose |
|:----|:--------|
| `/storage/plans.json` | Stores all user Plans (goal + milestones) |
| `/storage/tasks.json` | Stores all actionable Tasks |

✅ Local file storage  
✅ Tasks are linked optionally to Plans  
✅ Only reindex in-memory after full load

### llm/
| File              | Description |
|-------------------|-------------|
| llm_wrapper.py    | Wraps access to Qwen2:7B (Ollama) and optionally GPT-4 (Azure); used across agents |