# /graphs/nodes/router_llm.py

from llm.llm_wrapper import LLMWrapper
import json

class RouterLLM:
    """
    An LLM-based router that classifies user input into agent routes.
    """

    def __init__(self):
        self.llm = LLMWrapper(provider="ollama", model="qwen2.5:3b").llm
 
        self.prompt_template = """You are a router that classifies the latest user intent.

        Read the following conversation and return a JSON object with:

        - "agent": either "productivity" or "other"
        - "intent": one of "planning", "scheduling", "tasks", "tracking" — or null if agent is "other"


        Respond ONLY with valid JSON. No explanations.

        Output example:
        {{"agent": "productivity", "intent": "planning"}}

        ---

        Examples:

        User: I want to launch a blog.
        Assistant: When do you want to launch it?
        User: Before summer.
        Assistant: Got it! Let's plan steps.
        User: What’s next?
        → {{"agent": "productivity", "intent": "planning"}}

        User: I've been feeling really grateful lately.
        Assistant: That’s beautiful to hear.
        User: Just wanted to share!
        → {{"agent": "other", "intent": ""}}

        Now classify the following:

        {history_str}
        User: {user_msg}
        →
        """



    def classify(self, turns: list[dict], user_msg: str) -> tuple[str, str]:
        # On each turn, format your history + new user message…
        history_str = "\n".join(
            f"{turn['role'].title()}: {turn['content']}"
            for turn in turns
        )

        prompt = self.prompt_template.format(history_str=history_str, user_msg=user_msg)

        result = self.llm.invoke(prompt)
        # print(f"[RouterLLM] Raw LLM output:\n{result}\n")

        result = result.strip()

        if not (result.startswith("{") and result.endswith("}")):
            print(f"[RouterLLM] Output does not look like JSON, skipping. Output:\n{result}")
            return "other", None

        try:
            data = json.loads(result)
            agent = data.get("agent", "other")
            intent = data.get("intent", None)

            if agent not in {"productivity", "other"}:
                agent, intent = "other", None
            if agent == "productivity" and intent not in {"planning", "scheduling", "tasks", "tracking"}:
                agent, intent = "other", None

            return agent, intent

        except Exception as e:
            print(f"[RouterLLM] JSON parse error: {e} \u2014 Output: {result}")
            return "other", None


if __name__ == "__main__":

    def batch_test():
        router = RouterLLM()

        examples = [
            "I want to start a blog project this summer",
            "Today I feel grateful for my family and good health",
            "Please help me organize my work tasks",
            "I'm writing my thoughts about the year",
            # "Give me motivation tips for tough days",
            # "How can I plan my week effectively?",
            # "I need to reflect on my feelings",
            # "Just wanted to say I'm thankful for everything",
            # "Help me schedule my meetings",
            # "I want to write a journal entry tonight",
        ]

        print("🧠 RouterLLM Batch Test")
        print("Running classification for multiple prompts:\n")
        turns = []
        for idx, prompt in enumerate(examples, 1):
            try:
                route = router.classify(turns, prompt)
                print(f"{idx:2}. {prompt}")
                print(f"   → Routed to: {route}\n")
            except Exception as e:
                print(f"{idx:2}. {prompt}")
                print(f"   ⚠️  Error during classification: {e}\n")

    batch_test()
