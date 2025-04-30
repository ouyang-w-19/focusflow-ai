# FocusFlow AI – Repo Overview

A modular, local‑first productivity assistant powered by LangGraph.  It helps you plan goals, break them down into tasks, schedule your day, and (soon) reflect in a journal.  All data is stored on‑device by default.

---


## Repository Structure

```
focusflow-ai/
│
├── graphs/                      # 💡 LangGraph state machine definitions
│   ├── main_graph.py           # The root LangGraph with entrypoint → router → agent → responder
│   ├── types.py                # state object
│   └── nodes/                  # Atomic LangGraph node functions
│       ├── entrypoint.py
│       ├── router.py
│       ├── responder.py
│       ├── productivity_llm.py
│       ├── router_llm.py
│       └── journal_llm.py      # (TODO) Journal
│
├── agents/                     # 💡 Tool-backed logic per agent
│   ├── productivity/
│   │   ├── tools.py            # LangChain-compatible tool wrappers
│   │   ├── agent.py            # ProductivityAgent business logic
│   │   └── prompt_fragments/   # Modular adaptive prompt parts
│   │       ├── base.txt
│   │       ├── planning.txt
│   │       ├── tasks.txt
│   │       ├── scheduling.txt
│   │       └── tracking.txt
│   └── journal/                 # (TODO) Journal               
│       ├── tools.py
│       ├── agent.py
│       └── prompt_fragments/
│           ├── base.txt
│           └── journaling.txt
│
├── memory/                     # 💾 Memory backend (LangGraph Checkpointer)
│   ├── checkpointer.py         # Uses SqliteSaver or other backend
│   └── summarizer.py           # (TODO) Summarize old turns for long-term context
│
├── llm/                        # 🤖 LLM wrappers (OpenAI, Ollama, etc.)
│   └── llm_wrapper.py
│
├── schemas/                    # 📜 JSON schema definitions for plans, tasks, etc.
│   ├── task_schema.json
│   ├── planning_schema.json
│   └── ...
│
├── data/                       # 📁 Local data persistence
│   ├── plans.json
│   ├── tasks.json
│   └── focus.db                # LangGraph SQLite checkpointer
│
├── cli/                        # 💻 CLI runtime
│   └── main.py                 # CLI entrypoint with LangGraph execution loop
│
├── tests/                      # ✅ Unit & flow tests
│   ├── test_route_llm.py
│   └── test_productivity_llm.py
│
├── requirements.txt
├── .env / config.py            # API keys, model config
└── README.md



```

### Environment Variables

Use `.env.example` as a template:
```bash
cp .env.example .env
```
Update with credentials:
```env

# Local LLM config (for LangChain + Ollama)
OLLAMA_HOST=http://192.168.1.42:11434  # Replace with your Ollama server IP

```

---

### How to Run It Locally

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the cli interface demo
python -m cli.main

# 3. Optionally test To Do API integration
python -m tests.test_route_llm
python -m tests.test_productivity_llm
```

---
### Modules in Active Development

| Module | Status |
|--------|--------|
| ✅ Productivity      | Plans, tasks, scheduling, tracking |
| ✅ Route             | Intent detection, conversation routing |
| ✅ CLI Runner        | LangGraph-based session manager |
| 🕒 JournalAgent      | Scheduled for post-v0.1 |
| 🕒 MS Graph Delegated Auth | Scheduled for post-v0.1 |


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




### Graph Structure

```
main_graph 
    entrypoint --> router
    router -->|productivity|productivity
    router -->|None or chatbot | responder
    productivity --> responder
```
| Node        | Description                            |
|-------------|----------------------------------------|
| `entrypoint` | Initializes thread + logs user input   |
| `router`     | Routes to productivity or chatbot (will be replaced by journal or other specialized node)  based on user conversation domain (`agent_route`)  |
| `responder`  | Fallback assistant response            |
| `productivity` |  productivity logic |

---

#### Files and Storage

| File | Purpose |
|:----|:--------|
| `/data/plans.json` | Stores all user Plans (goal + milestones) |
| `/data/tasks.json` | Stores all actionable Tasks |

✅ Local file storage  
✅ Tasks are linked optionally to Plans  
✅ Only reindex in-memory after full load

### llm/
| File              | Description |
|-------------------|-------------|
| llm_wrapper.py    | Wraps access to Qwen2.5:3B (Ollama) and optionally GPT-4 (Azure); used across agents |



### Contributions & Modules Actively Maintained
- Productivity (plan management, task breakdown, prioritization, scheduling)
- Streamlit UI prototype (todo)
- graph

Journaling agent design and basic Microsoft Graph delegated authentication are planned next. Microsoft Graph integration (for To Do and Calendar) is deferred until API functions are fully stabilized. The Productivity Agent currently focuses on local planning, task management, and scheduling.

