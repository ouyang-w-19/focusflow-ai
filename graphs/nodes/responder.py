# /graphs/nodes/responder.py
from datetime import datetime
from graphs.types import GraphState

def responder(state: GraphState) -> GraphState:
    state.setdefault("turns", [])  # ensure turns exists

    if state.get("assistant_response"):
        reply = state["assistant_response"]

    elif state.get("tool_error") or state.get("llm_error"):
        err = state.pop("tool_error", None) or state.pop("llm_error", None)
        reply = f"⚠️ I ran into a problem: {err} — would you like me to try again?"

    else:
        reply = (
            "I'm sorry, I didn't quite get that. "
            "Could you rephrase or add more details?"
        )
        
    state["turns"].append({
        "role": "assistant",
        "content": reply,
        "timestamp": datetime.utcnow().isoformat(),
    })

    if len(state["turns"]) > 40:
        state["turns"] = state["turns"][-40:]

    state["assistant_response"] = reply
    state["tool_calls"] = None
    state["tool_result"] = None

    return state
