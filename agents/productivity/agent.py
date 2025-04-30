# /agents/productivity/agent.py
"""Productivity agent — plan & task storage helpers.

Public tool surface (for the LLM layer):
    • find_similar_plans(goal: str, threshold: float = 0.8) -> List[PlanRecord]
    • create_plan(...)
    • list_plans(), list_tasks(), create_task(), complete_task(), schedule_day(), summarize_plan()

`create_plan()` is now *deliberately* agnostic of duplicate detection; callers must run
`find_similar_plans()` first if they want to warn the user.
"""

from __future__ import annotations

import json
import uuid
import difflib
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Optional, TypedDict

import jsonschema
from filelock import FileLock

# ─────────────────────────────────────────────────────
# Paths & constants

BASE_DIR = Path(__file__).parents[2]  # project root
DATA_DIR = BASE_DIR / "data"
SCHEMA_DIR = BASE_DIR / "schemas"
PLANS_FILE = DATA_DIR / "plans.json"
TASKS_FILE = DATA_DIR / "tasks.json"
LOCK_SUFFIX = ".lock"
LOCK_TIMEOUT = 10  # seconds

# Fuzzy‑match settings for duplicate search (used by find_similar_plans only)
SIMILARITY_THRESHOLD = 0.8

# ─────────────────────────────────────────────────────
# Typed records

# === Typed records ===
class TaskRecord(TypedDict):
    id: str
    title: str
    completed: bool
    plan_id: Optional[str]
    milestone_id: Optional[str]
    priority: Optional[str]
    deadline: Optional[str]
    estimated_time: Optional[int]
    created_at: str
    complete_at: Optional[str]

class MilestoneRecord(TypedDict):
    id: str
    title: str
    task_ids: List[str]
    completed: bool

class PlanRecord(TypedDict):
    id: str
    goal: str
    deadline: str
    priority: str
    status: Optional[str]
    milestones: List[MilestoneRecord]
    tasks: List[str]
    created_at: str
    progress: int

# === JSON helpers with locking & atomic writes ===
def _load_json(path: Path) -> List[dict]:
    path.parent.mkdir(parents=True, exist_ok=True)
    lock = FileLock(str(path) + LOCK_SUFFIX, timeout=LOCK_TIMEOUT)
    with lock:
        if not path.exists():
            return []
        return json.loads(path.read_text(encoding="utf-8"))

def _save_json(path: Path, data: List[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(path.suffix + ".tmp")
    lock = FileLock(str(path) + LOCK_SUFFIX, timeout=LOCK_TIMEOUT)
    with lock:
        temp.write_text(json.dumps(data, indent=2), encoding="utf-8")
        temp.replace(path)

# === Schema validation ===
def _validate(instance: dict, schema_file: str):
    schema_path = SCHEMA_DIR / schema_file
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    jsonschema.validate(instance=instance, schema=schema)

# ─────────────────────────────────────────────────────
# Helper utilities (string similarity, listing)


def _string_similarity(a: str, b: str) -> float:
    """Return fuzzy ratio (0‑1) between two strings using SequenceMatcher."""
    return difflib.SequenceMatcher(None, a.casefold(), b.casefold()).ratio()


def find_similar_plans(goal: str, threshold: float = SIMILARITY_THRESHOLD) -> List[PlanRecord]:
    """Return stored plans whose goal resembles *goal* >= *threshold*."""
    plans: List[PlanRecord] = _load_json(PLANS_FILE)  # type: ignore[assignment]
    return [p for p in plans if _string_similarity(goal, p.get("goal", "")) >= threshold]


def list_plans() -> List[PlanRecord]:  # type: ignore[override]
    """Return all plans (read‑only)."""
    return _load_json(PLANS_FILE)  # type: ignore[return-value]


def list_tasks() -> List[TaskRecord]:  # type: ignore[override]
    """Return all tasks (read‑only)."""
    return _load_json(TASKS_FILE)  # type: ignore[return-value]


# ─────────────────────────────────────────────────────
# Plan CRUD

def create_plan(
    goal: str,
    deadline: str,
    priority: str,
    milestones: List[str],
    status: Optional[str] = "in_progress"
) -> PlanRecord:
    """
    Create a new plan with milestones and empty tasks list — duplicate detection left to caller.
    """
    plans = _load_json(PLANS_FILE)
    plan_id = uuid.uuid4().hex

    new_plan: PlanRecord = {
        "id": plan_id,
        "goal": goal,
        "deadline": deadline,
        "priority": priority,
        "status": status,
        "milestones": [
            {"id": uuid.uuid4().hex, "title": title, "task_ids": [], "completed": False}
            for title in milestones
        ],
        "tasks": [],
        "created_at": datetime.utcnow().isoformat(),
        "progress": 0
    }

    # validate
    _validate(new_plan, "planning_schema.json")

    plans.append(new_plan)
    _save_json(PLANS_FILE, plans)
    return new_plan

# ─────────────────────────────────────────────────────
# Task CRUD

def create_task(
    title: str,
    priority: Optional[str] = None,
    deadline: Optional[str] = None,
    estimated_time: Optional[int] = None,
    plan_id: Optional[str] = None,
    milestone_id: Optional[str] = None
) -> TaskRecord:
    """
    Create a task, optionally linked to a plan & milestone.
    """
    tasks = _load_json(TASKS_FILE)
    new_task: TaskRecord = {
        "id": uuid.uuid4().hex,
        "title": title,
        "completed": False,
        "plan_id": plan_id,
        "milestone_id": milestone_id,
        "priority": priority,
        "deadline": deadline,
        "estimated_time": estimated_time,
        "created_at": datetime.utcnow().isoformat(),
        "complete_at": None
    }

    # validate
    _validate(new_task, "task_schema.json")

    tasks.append(new_task)
    _save_json(TASKS_FILE, tasks)

    # Link into plan & milestone if provided
    if plan_id:
        _attach_task_to_plan(plan_id, new_task["id"])
    if milestone_id:
        _attach_task_to_milestone(plan_id, milestone_id, new_task["id"])
    return new_task

def _attach_task_to_plan(plan_id: str, task_id: str):
    plans = _load_json(PLANS_FILE)
    for plan in plans:
        if plan["id"] == plan_id:
            plan.setdefault("tasks", []).append(task_id)
            _save_json(PLANS_FILE, plans)
            return
    raise KeyError(f"Plan {plan_id} not found")

def _attach_task_to_milestone(plan_id: str, milestone_id: str, task_id: str):
    plans = _load_json(PLANS_FILE)
    for plan in plans:
        if plan["id"] == plan_id:
            for ms in plan["milestones"]:
                if ms["id"] == milestone_id:
                    ms.setdefault("task_ids", []).append(task_id)
                    _save_json(PLANS_FILE, plans)
                    return
            raise KeyError(f"Milestone {milestone_id} not found in plan {plan_id}")
    raise KeyError(f"Plan {plan_id} not found")

def complete_task(task_id: str) -> TaskRecord:
    """
    Mark a task complete, set `complete_at`, update milestone & plan progress.
    """
    tasks = _load_json(TASKS_FILE)
    for t in tasks:
        if t["id"] == task_id:
            t["completed"] = True
            t["complete_at"] = datetime.utcnow().isoformat()
            _save_json(TASKS_FILE, tasks)

            # Update milestone & plan
            plan_id = t.get("plan_id")
            if plan_id:
                _update_milestone_completion(plan_id, task_id)
                _update_plan_progress(plan_id)
            return t
    raise KeyError(f"Task {task_id} not found")

def list_tasks() -> List[dict]:
    """List all current tasks."""
    return _load_json(TASKS_FILE)

# ─────────────────────────────────────────────────────
# Milestone & progress helpers

def _update_milestone_completion(plan_id: str, task_id: str):
    plans = _load_json(PLANS_FILE)
    tasks = {t["id"]: t for t in _load_json(TASKS_FILE)}
    for plan in plans:
        if plan["id"] == plan_id:
            changed = False
            for ms in plan["milestones"]:
                if task_id in ms.get("task_ids", []):
                    all_done = all(tasks[tid]["completed"] for tid in ms["task_ids"])
                    if ms["completed"] != all_done:
                        ms["completed"] = all_done
                        changed = True
            if changed:
                _save_json(PLANS_FILE, plans)
            return
    raise KeyError(f"Plan {plan_id} not found")

def _update_plan_progress(plan_id: str):
    plans = _load_json(PLANS_FILE)
    for plan in plans:
        if plan["id"] == plan_id:
            mss = plan.get("milestones", [])
            plan["progress"] = (
                0 if not mss else int(
                    sum(1 for ms in mss if ms["completed"]) / len(mss) * 100
                )
            )
            _save_json(PLANS_FILE, plans)
            return
    raise KeyError(f"Plan {plan_id} not found")


# (schedule_day & summarize_plan)
# ─────────────────────────────────────────────────────

def schedule_day(available_hours: Optional[int] = 8) -> dict:
    """Generate a daily schedule based on tasks and available hours."""
    tasks = _load_json(TASKS_FILE)
    tasks = [t for t in tasks if not t.get("completed")]
    tasks.sort(key=lambda t: (t.get("priority", "medium"), t.get("deadline", "9999-12-31")))

    schedule = {}
    current_time = datetime.utcnow().replace(hour=9, minute=0)
    for task in tasks[:available_hours]:
        end_time = current_time + timedelta(hours=1)
        schedule[f"{current_time.strftime('%H:%M')} - {end_time.strftime('%H:%M')}"] = task["title"]
        current_time = end_time

    return schedule

# ─────────────────────────────────────────────────────

def summarize_plan(plan_id: str) -> str:
    """Summarize the key fields of a plan by ID."""
    plans = _load_json(PLANS_FILE)
    for plan in plans:
        if plan["id"] == plan_id:
            milestones = ", ".join(m["title"] for m in plan.get("milestones", []))
            return (
                f"Goal: {plan['goal']}\n"
                f"Deadline: {plan['deadline']}\n"
                f"Priority: {plan['priority']}\n"
                f"Milestones: {milestones}"
            )
    return f"⚠️ Plan with ID {plan_id} not found."