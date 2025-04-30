from graphs.nodes.productivity_llm import productivity_llm_node

print("🧠 productivity_llm_node testing\nType /exit to quit.\n")

intent = input("Intent: ").strip()
state = {
    "turns": [],
    "intent": input,
    "user_msg": ""
}   

while True:
    user_msg = input("You: ").strip()
    
    if user_msg.lower() == "/exit":
        print("Goodbye! 👋")
        break
    state["user_msg"] = user_msg

    state = productivity_llm_node(state)

    print("Assistant: \n", state.get("assistant_response", []), "\n")



