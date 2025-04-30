# /graphs/nodes/entrypoint.py
from datetime import datetime
from graphs.types import GraphState

def entrypoint(state: GraphState) -> GraphState:
    return {
        **state,
        "thread_id": state.get("thread_id", "default"),
        "user_msg": state["user_msg"],
        "turns": state.get("turns", []) + [
            {
                "role": "user",
                "content": state["user_msg"],
                "timestamp": datetime.utcnow().isoformat(),
            }
        ],
    }
