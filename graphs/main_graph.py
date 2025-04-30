# graphs/main_graph.py

from langgraph.graph import StateGraph, END
from graphs.nodes.entrypoint import entrypoint
from graphs.nodes.router import router
from graphs.nodes.responder import responder
from graphs.types import GraphState
from graphs.nodes.productivity_llm import productivity_llm_node
from graphs.nodes.chatbot import chatbot_node

def build_main_graph() -> StateGraph:
    g = StateGraph(GraphState)

    # ── core nodes ───────────────────────────────────────────────────────────
    g.add_node('entrypoint', entrypoint)
    g.add_node('router', router)
    g.add_node('responder', responder)
    g.add_node('productivity', productivity_llm_node)
    g.add_node('chatbot', chatbot_node)

    # ── transitions ─────────────────────────────────────────────────────────
    g.set_entry_point('entrypoint')
    g.add_edge('entrypoint', 'router')

    # route to productivity or straight to final responder
    g.add_conditional_edges(
        'router', lambda state: state.get('agent_route'),
        {
            'productivity': 'productivity',
            'other':        'chatbot',
            None:           'responder',
        }
    )

    g.add_edge('productivity', 'responder')
    g.add_edge('chatbot', 'responder')

    g.set_finish_point('responder')

    return g.compile()
