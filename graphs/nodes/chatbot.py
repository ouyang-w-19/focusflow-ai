# /graphs/nodes/chatbot.py

from datetime import datetime
from llm.llm_wrapper import LLMWrapper
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import (
    AIMessage
)

from agents.productivity.tools import tool_registry
from graphs.types import GraphState


llm = LLMWrapper(provider="ollama", model="qwen2.5:3b").llm

def chatbot_node(state: GraphState) -> GraphState:
    # 0. Ensure mandatory state keys exist
    state.setdefault("turns", [])
    state["llm_error"] = None

    history_str = "\n".join(
        f"{turn['role'].title()}: {turn['content']}"
        for turn in state["turns"]
    )
    base_system_msg = """ You are FocusFlow, a thoughtful and supportive assistant.

Your goal is to help the user reflect, explore thoughts, capture ideas, or maintain motivation — especially when structured planning is not currently enabled.

Guidelines:
- Be friendly, calm, and respectful.
- Use short, helpful replies that feel natural and human.
- Ask open-ended follow-up questions when appropriate.
- Help the user get clarity on their thoughts or intentions.
- Avoid giving rigid advice; offer suggestions gently.

Examples of what you support:
- General questions or musings
- Light journaling ("I feel stuck today.")
- Idea capture ("I want to start a podcast.")
- Emotional check-ins ("I'm feeling overwhelmed.")
- Reflective prompts ("How can I improve my week?")

Do not try to call tools or structured planning actions.
If the user seems ready to plan or take action, gently suggest:  
"If you'd like to start planning this as a project later, I can guide you when the productivity assistant is available."

Keep it human. Keep it helpful.
"""
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
        tools =[],
        prompt=prompt_template
    )

    try:
        response = agent.invoke({"messages": user_msg})
    except Exception as exc:
        state["llm_error"] = str(exc)
        print("llm_error: ", str(exc))
        return state

    # print(response)
    assistant_response = ""
    if isinstance(response, str):
        assistant_response = response.strip()
    else:
        for msg in response.get("messages", []):
            if isinstance(msg, AIMessage):
                if msg.content:
                    assistant_response = msg.content


    state["assistant_response"] = assistant_response

    return state

if __name__ == "__main__":
    
    state = {
        "turns": [],
        "intent": "",
        "user_msg": "I had a long day today."
    }

    # 4. Inspect the result
    print("User:\n")
    print(state.get("user_msg", []))
 
    # 3. Call your node
    new_state = chatbot_node(state)

    # 4. Inspect the result
    print("Assistant:\n")
    print(new_state.get("assistant_response", []))
 
    # 5. Confirm that the turn was recorded
    print("\nConversation History:")
    for t in new_state["turns"]:
        print(f"{t['role'].title()}: {t['content']}")

        
