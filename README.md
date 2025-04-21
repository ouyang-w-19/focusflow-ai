## 🧱 FocusFlow AI – Repo Overview (Updated)

A productivity-focused AI agent system that helps users plan tasks, sync with Microsoft 365, and journal progress via a chat-based UI.

---

### 📁 Repo Structure

```
focusflow-ai/
│
├── auth/                     # Microsoft Graph API authentication (via MSAL)
│   └── ms_graph_auth.py      # Token retrieval logic (client credentials for now)
│
├── graph/                    # Graph API wrappers
│   └── todo.py               # Task list and To Do API interactions
│   └── calendar.py           # [Planned] Calendar sync for time blocking
│
├── agents/                   # Core LLM agents
│   └── task_agent.py         # Turns goals into subtasks (via LLM)
│   └── journal_agent.py      # [Planned] Journaling interaction agent
│
├── prompts/                  # Prompt templates (LLM inputs)
│   └── journal.txt
│   └── planner.txt
│
├── ui/                       # Streamlit chat UI
│   └── app.py
│
├── data/                     # Local storage for tasks and journals
│   ├── tasks.db / tasks.json
│   └── journals/
│       └── 2025-04-16.json
│
├── tests/                    # Test files
│   └── test_graph_todo.py    # Tests Microsoft Graph To Do functionality
│   └── test_ollama.py        # Tests local LLM connectivity via Ollama
│   └── test_task_agent.py    # Tests TaskAgent's goal-to-task breakdown
│
├── config.py                 # Loads secrets from .env
├── .env                      # Dev secrets (ignored)
├── .env.example              # Template file for credentials setup
├── .gitignore                # Ignores secrets, .db/.json, cache
├── requirements.txt          # All Python dependencies
├── run.py                    # Entrypoint: runs Streamlit app
└── README.md
│   └── test_graph_todo.py    # Tests Microsoft Graph To Do functionality
│
├── config.py                 # Loads secrets from .env
├── .env                      # Dev secrets (ignored)
├── .env.example              # Template file for credentials setup
├── .gitignore                # Ignores secrets, .db/.json, cache
├── requirements.txt          # All Python dependencies
├── run.py                    # Entrypoint: runs Streamlit app
└── README.md
```

---

### 🔐 Environment Variables

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

### 📦 How to Run It Locally

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the Streamlit UI
python run.py

# 3. Optionally test To Do API integration
python -m tests.test_graph_todo
```

---

### 🔌 Microsoft Graph API Integration

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

### 🛡 Repo Security Notes
- `.env`, `.json`, `.db` are ignored by Git
- Repo is **private** during development; will be made **public** upon cleanup before submission

---

### ✅ Contributions & Modules Actively Maintained
- Agent logic (task breakdown)
- Graph API (To Do integration)
- Streamlit UI prototype

Journaling, nudging, and delegated authentication are in progress.

