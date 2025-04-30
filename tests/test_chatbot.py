# /tests/test_chatbot.py

from graphs.nodes.chatbot import chatbot_node

# Batch test cases
test_inputs = [
    "I’ve been feeling overwhelmed lately and don’t know where to start.",
    "I feel like this week was unproductive. I just want to figure out why.",
    "I think I want to write a book someday.",
    "Today was a good day. I feel lighter than usual.",
    "I kind of want to start something new... maybe a podcast?"
]

def run_fallback_test_cases():
    for i, user_msg in enumerate(test_inputs, start=1):
        print(f"\n\n=== Test Case {i} ===")

        # Initial state
        state = {
            "turns": [],
            "intent": None,
            "user_msg": user_msg
        }

        print("User:\n")
        print(user_msg)

        # Run fallback node
        new_state = chatbot_node(state)

        print("\nAssistant:\n")
        print(new_state.get("assistant_response", "[no response]"))


if __name__ == "__main__":
    run_fallback_test_cases()
