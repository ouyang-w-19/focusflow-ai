# /graphs/nodes/router.py
from graphs.types import GraphState
from graphs.nodes.router_llm import RouterLLM

router_llm = RouterLLM()

def router(state: GraphState) -> GraphState:
    """
    Smart LLM-based router for FocusFlow agents.
    Updates state["agent_route"].
    """
    turns = state.get("turns", [])
    user_msg = state.get("user_msg", "")

    # Append latest message to turns if not already included
    if not turns or turns[-1].get("content") != user_msg:
        turns = turns + [{"role": "user", "content": user_msg}]

    agent_route, intent = router_llm.classify(turns, user_msg)

    state["agent_route"] = agent_route
    state["intent"] = intent
    return state
