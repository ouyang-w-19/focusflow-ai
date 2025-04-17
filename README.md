## 🧱 FocusFlow AI – Repo Structure Overview

Hey team, here's a quick summary of how the project is structured so far:

---

### 📁 Repo Structure

```
focusflow-ai/
│
├── auth/                     # Microsoft Graph API auth via MSAL
│   └── ms_graph_auth.py
│
├── graph/                    # Graph API wrappers
│   └── todo.py               # Task list, create/read/update tasks
│
├── agents/                   # Agent logic and orchestration
│   └── task_agent.py
│   └── journal_agent.py
│
├── prompts/                  # Prompt templates for journaling & planning
│   └── journal.txt
│   └── planner.txt
│
├── ui/                       # Streamlit app logic
│   └── app.py
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

---

### 🔐 Environment Variables

Secrets like Microsoft client ID and secret are stored in `.env` (not committed). Use `.env.example` as a template.

```bash
cp .env.example .env
# Then fill in:
# CLIENT_ID=
# TENANT_ID=
# CLIENT_SECRET=
```

---

### 📦 How to Run It Locally

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Start the app
python run.py
```

---

### 🛡 Notes on Security

- `.env`, `*.json`, and `*.db` are ignored via `.gitignore`
- The repo is **private** for now — will be made **public** after cleanup before hackathon submission

