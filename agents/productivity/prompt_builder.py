# /agents/productivity/prompt_builder.py

import os
from typing import Optional

PROMPT_DIR = os.path.join(os.path.dirname(__file__), "prompt_fragments")

def load_fragment(filename: str) -> str:
    """
    Utility to load a prompt fragment from disk.
    """
    path = os.path.join(PROMPT_DIR, filename)
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def build_prompt(turns: list[dict], intent: Optional[str] = None) -> str:
    prompt_parts = []

    base_prompt = load_fragment("base.txt")
    prompt_parts.append(base_prompt)

    # full_context = " ".join(t.get("content", "") for t in turns).lower()
    full_context = " "

    # If intent is provided by router, prefer it
    if intent == "planning" or "plan" in full_context:
        prompt_parts.append(load_fragment("planning.txt"))
    if intent == "tasks" or any(k in full_context for k in ["task", "todo", "step"]):
        prompt_parts.append(load_fragment("tasks.txt"))
    if intent == "scheduling" or any(k in full_context for k in ["schedule", "calendar", "time block"]):
        prompt_parts.append(load_fragment("scheduling.txt"))
    if intent == "tracking" or any(k in full_context for k in ["progress", "milestone", "tracking"]):
        prompt_parts.append(load_fragment("tracking.txt"))

    return "\n\n".join(prompt_parts)
