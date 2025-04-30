# /graphs/nodes/productivity_llm.py
import json
from datetime import datetime
from typing import List

from langgraph.prebuilt import create_react_agent
from langchain_ollama import ChatOllama
from langchain_core.messages import (
    AIMessage, HumanMessage, SystemMessage, BaseMessage
)

from agents.productivity.tools import tool_registry
from agents.productivity.prompt_builder import build_prompt  # keeps your custom header
from graphs.types import GraphState

llm = ChatOllama(model="qwen2.5:3b")
def _dict_to_message(d: dict) -> BaseMessage:
    """Helper: convert a dict {'role': ..., 'content': ...} to a LangChain message."""
    role = d.get("role")
    content = d.get("content")
    if role == "user":
        return HumanMessage(content=content)
    elif role == "assistant":
        return AIMessage(content=content)
    elif role == "system":
        return SystemMessage(content=content)
    else:
        raise ValueError(f"Unknown role: {role}")

def productivity_llm_node(state: GraphState) -> GraphState:
    # 0. Ensure mandatory state keys exist
    state.setdefault("turns", [])
    state.setdefault("tool_result", None)
    state["llm_error"] = None
    print("turns:", state["turns"])

    # Build prompt using context + intent
    intent = state.get("intent")
    base_system_msg = build_prompt(state["turns"], intent)
    print("System: \n", base_system_msg)

    # On each turn, format your history str
    history_str = "\n".join(
        f"{turn['role'].title()}: {turn['content']}"
        for turn in state["turns"]
    )

    print("History: \n", history_str)

    # 3) Compose a single‐string prompt exposing only {input}
    prompt_template="\n\n".join([
            base_system_msg,
            "History conversation:\n" + history_str,
        ])

    # Append the new user turn exactly once
    user_msg = state.pop("user_msg")
    timestamp = datetime.utcnow().isoformat()
    state["turns"].append({
        "role": "user",
        "content": user_msg,
        "timestamp": timestamp,
    })
    print("User: ", user_msg)

    agent = create_react_agent(
        model=llm,
        tools=tool_registry,
        prompt=prompt_template
    )

    # 4. Call LLM (OllamaLLM expects plain string)
    try:
        response = agent.invoke({"messages": user_msg})
    except Exception as exc:
        state["llm_error"] = str(exc)
        print("llm_error: ", str(exc))
        return state

    print(response)
    
    if isinstance(response, str):
        content = response.strip()
        tool_calls = None

    elif isinstance(response, dict) and "messages" in response:
        # Ollama-react spits out a {"messages": [...]} dict,
        # so grab the last AIMessage in there:
        ai_msgs = [m for m in response["messages"] if isinstance(m, AIMessage)]
        if ai_msgs:
            content = ai_msgs[-1].content.strip()
        else:
            content = str(response)
        tool_calls = response.get("tool_calls", None)

    else:
        # fallback for other AgentOutput types
        content = getattr(response, "content", str(response)).strip()
        tool_calls = getattr(response, "tool_calls", None)

    # 6. Persist into state -----------------------------
    state["turns"].append({
        "role":      "assistant",
        "content":   content,
        "timestamp": datetime.utcnow().isoformat(),
    })

    state["assistant_response"] = content
    state["tool_calls"] = tool_calls
    state["llm_retry_count"] = state.get("llm_retry_count", 0) + 1

    return state

if __name__ == "__main__":
    
    state = {
        "turns": [],
        "intent": "planning",
        "user_msg": "I want to start a blog project this summer"
    }
    # 3. Call your node
    new_state = productivity_llm_node(state)

    # 4. Inspect the result
    print("Assistant:\n")
    print(new_state["assistant_response"])

    # 5. Confirm that the turn was recorded
    print("\nConversation History:")
    for t in new_state["turns"]:
        ts = t["timestamp"]
        print(f"[{ts}] {t['role'].title()}: {t['content']}")

        
