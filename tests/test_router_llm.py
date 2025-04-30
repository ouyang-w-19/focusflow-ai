# /sandbox/test_router_llm.py

from graphs.nodes.router_llm import RouterLLM
from graphs.types import GraphState

def batch_test():
    router = RouterLLM()

    examples = [
        "I want to start a blog project this summer",
        "Today I feel grateful for my family and good health",
        "Please help me organize my work tasks",
        "I'm writing my thoughts about the year",
        "Give me motivation tips for tough days",
        "How can I plan my week effectively?",
        "I need to reflect on my feelings",
        "Just wanted to say I'm thankful for everything",
        "Help me schedule my meetings",
        "I want to write a journal entry tonight",
    ]

    print("🧠 RouterLLM Batch Test")
    print("Running classification for multiple prompts:\n")
    turns = []
    for idx, prompt in enumerate(examples, 1):
        try:
            # print(turns)
            route = router.classify(turns, prompt)
            print(f"{idx:2}. {prompt}")
            print(f"   → Routed to: {route}\n")
        except Exception as e:
            print(f"{idx:2}. {prompt}")
            print(f"   ⚠️  Error during classification: {e}\n")

if __name__ == "__main__":
    batch_test()
