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

        {conversation}

        →
        """



    def classify(self, turns: list[dict]) -> tuple[str, str]:
        conversation = ""
        for turn in turns:
            role = turn.get("role", "user")
            content = turn.get("content", "")
            conversation += f"{role.capitalize()}: {content}\n"

        prompt = self.prompt_template.format(conversation=conversation)

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

