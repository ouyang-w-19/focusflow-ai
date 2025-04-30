# /agents/productivity/tools.py
"""LangChain tool wrappers around the domain‑level productivity agent functions.

Expose a clean, typed tool surface to the LLM runtime.
"""

from typing import List, Optional, Dict, Any
from langchain_core.tools import tool

from agents.productivity.agent import (
    create_plan as domain_create_plan,
    create_task as domain_create_task,
    complete_task as domain_complete_task,
    list_tasks as domain_list_tasks,
    schedule_day as domain_schedule_day,
    summarize_plan as domain_summarize_plan,
    find_similar_plans as domain_find_similar_plans,
)

# ─────────────────────────────────────────────────────
# Plan‑level tools


@tool
def create_plan(goal: str, deadline: str, priority: str, milestones: List[str]) -> str:
    """Create a new plan with the given goal, deadline, priority and milestones."""
    try:
        plan = domain_create_plan(goal=goal, deadline=deadline, priority=priority, milestones=milestones)
        return f"✅ Plan created: {plan['goal']} (id={plan['id']})"
    except Exception as e:
        return f"⚠️ Error creating plan: {e}"


@tool
def find_similar_plans(goal: str, threshold: float = 0.8) -> List[Dict[str, Any]]:
    """Return plans whose goal is fuzzy‑matched to *goal* (≥ *threshold*)."""
    try:
        return domain_find_similar_plans(goal, threshold)
    except Exception as e:
        return [{"error": str(e)}]


# ─────────────────────────────────────────────────────
# Task‑level tools


@tool
def create_task(
    title: str,
    priority: Optional[str] = None,
    deadline: Optional[str] = None,
    estimated_time: Optional[int] = None,
    plan_id: Optional[str] = None,
    milestone_id: Optional[str] = None,
) -> str:
    """Create a task, optionally linked to a plan and/or milestone."""
    try:
        task = domain_create_task(
            title=title,
            priority=priority,
            deadline=deadline,
            estimated_time=estimated_time,
            plan_id=plan_id,
            milestone_id=milestone_id,
        )
        return f"✅ Task created: {task['title']} (id={task['id']})"
    except Exception as e:
        return f"⚠️ Error creating task: {e}"


@tool
def complete_task(task_id: str) -> str:
    """Mark the specified task as complete."""
    try:
        task = domain_complete_task(task_id)
        return f"✅ Task '{task['title']}' marked complete at {task['complete_at']}."
    except KeyError:
        return f"⚠️ Task with ID {task_id} not found."
    except Exception as e:
        return f"⚠️ Error completing task: {e}"


@tool
def list_tasks() -> List[Dict[str, Any]]:
    """Return all tasks stored in the system."""
    try:
        return domain_list_tasks()
    except Exception as e:
        return [{"error": str(e)}]


# ─────────────────────────────────────────────────────
# Schedule & summary


@tool
def schedule_day(available_hours: int = 8) -> Dict[str, str]:
    """Build a simple hourly schedule for the next `available_hours`."""
    try:
        return domain_schedule_day(available_hours)
    except Exception as e:
        return {"error": str(e)}


@tool
def summarize_plan(plan_id: str) -> str:
    """Generate a human‑readable summary of the requested plan ID."""
    try:
        return domain_summarize_plan(plan_id)
    except KeyError:
        return f"⚠️ Plan with ID {plan_id} not found."
    except Exception as e:
        return f"⚠️ Error summarizing plan: {e}"


# ─────────────────────────────────────────────────────
# Registry


tool_registry = [
    create_plan,
    find_similar_plans,
    create_task,
    complete_task,
    list_tasks,
    schedule_day,
    summarize_plan,
]
