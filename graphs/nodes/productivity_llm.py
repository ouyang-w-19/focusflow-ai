# /graphs/nodes/productivity_llm.py
from datetime import datetime
from llm.llm_wrapper import LLMWrapper
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import (
    AIMessage, ToolMessage
)

from agents.productivity.tools import tool_registry
from agents.productivity.prompt_builder import build_prompt  # keeps your custom header
from graphs.types import GraphState
from typing import Any, Dict, List

llm = LLMWrapper(provider="ollama", model="qwen2.5:3b").llm

def productivity_llm_node(state: GraphState) -> GraphState:
    # 0. Ensure mandatory state keys exist
    state.setdefault("turns", [])
    state.setdefault("tool_result", None)
    state["llm_error"] = None
    state.setdefault("tool_calls", None)
    state.setdefault("tool_result", [])
    state.setdefault("tool_error", None)
    
    # Build prompt using context + intent
    intent = state.get("intent")
    base_system_msg = build_prompt(state["turns"], intent)
    # print("System: \n", base_system_msg)

    history_str = "\n".join(
        f"{turn['role'].title()}: {turn['content']}"
        for turn in state["turns"]
    )

    prompt_template="\n\n".join([
            base_system_msg,
            "Conversation:\n" + history_str,
        ])
    # print(prompt_template)
    # Append the new user turn exactly once
    user_msg = state.pop("user_msg")
    timestamp = datetime.utcnow().isoformat()
    state["turns"].append({
        "role": "user",
        "content": user_msg,
        "timestamp": timestamp,
    })
    # print("User: ", user_msg)

    agent = create_react_agent(
        model=llm,
        tools=tool_registry,
        prompt=prompt_template
    )

    try:
        response = agent.invoke({"messages": user_msg})
    except Exception as exc:
        state["llm_error"] = str(exc)
        print("llm_error: ", str(exc))
        return state

    # print(response)
    tool_responsed = ""
    assistant_response = ""
    tool_calls = None
    if isinstance(response, str):
        assistant_response = response.strip()
        tool_calls = None
    else:
        for msg in response.get("messages", []):
            if isinstance(msg, AIMessage):
                if msg.tool_calls:
                    tool_calls = msg.tool_calls
                    # state["tool_result"].append(tool_calls)
                    state["tool_calls"] = tool_calls
                if msg.content:
                    assistant_response = msg.content
            elif isinstance(msg, ToolMessage):
                tool_responsed = msg.content
    
    if assistant_response:
        if tool_responsed:
            state["assistant_response"] = tool_responsed + "\n" +  assistant_response
        else:
            state["assistant_response"] = assistant_response
    else:
        if tool_responsed:
            state["assistant_response"] = tool_responsed 
        else:
            state["assistant_response"] = ""
  
    state["turns"].append({
        "role": "Assistant",
        "content": assistant_response,
        "timestamp": timestamp,
    })

    return state

if __name__ == "__main__":
    
    state_round = {
        "turns": [],
        "intent": "planning",
        "user_msg": "The goal of my blog is to share budget-friendly travel tips and personal travel stories to help others plan affordable trips. The deadline for launching the blog is June 15, 2025, and the priority level is high. Some key milestones include finalizing the blog name and domain by May 5, completing the first three blog posts by May 15, launching the blog by June 1, and starting promotion by June 10."
    }   
    state_round["turns"].append({
        "role": "user",
        "content": "I want to start a blog project this summer",
    })
    state_round["turns"].append({
        "role": "assistant",
        "content": "That's great! Let's first outline some key details for your blog project. Could you please provide me with the specific goal or objective of the blog, its deadline, and any priority level (high, medium, low)? Additionally, it would be helpful to know if there are any major milestones in mind as you start this project?",
    })
    # 3. Call your node
    new_state = productivity_llm_node(state_round)

    # 4. Inspect the result
    print("Assistant:\n")
    print(new_state.get("assistant_response", []))
    # 4. Inspect the result
    print("Tool Call:\n")
    print(new_state.get("tool_calls", []))
    # 5. Confirm that the turn was recorded
    print("\nConversation History:")
    for t in new_state["turns"]:
        print(f"{t['role'].title()}: {t['content']}")

        
