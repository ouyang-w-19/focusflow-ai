# base_agent.py
from llm.llm_wrapper import LLMWrapper

class BaseAgent:
    def __init__(self, memory=None, tools=None, provider="ollama", model="qwen2:7b"):
        self.memory = memory
        self.tools = tools or {}
        self.llm = LLMWrapper(provider=provider, model=model)

    def handle(self, user_input: str) -> dict:
        raise NotImplementedError("Each agent must implement the handle method.")
