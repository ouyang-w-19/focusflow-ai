# agents/frontend_agent.py

from agents.orchestrator import Orchestrator
from agents.base_agent import BaseAgent

class FrontendAgent(BaseAgent):
    def __init__(self, memory=None, provider="ollama", model="qwen2:7b"):
        super().__init__(memory, provider, model)
        self.orchestrator = Orchestrator(memory=memory)

    def handle(self, user_input: str) -> dict:
        """
        Process raw user input and return final structured response.
        1. Use LLM to detect intent and extract key planning information.
        2. Pass structured input to Orchestrator.
        """
        routing_prompt = (
            "Interpret the user's input and structure it for dispatch.\n"
            "Return a JSON-like dict with fields: intent, mode, time, energy, tasks, etc.\n"
            f"User: \"{user_input}\" \n"
            "Structured:"            
        )

        structured = self.llm(routing_prompt)  # Assumes the output is a JSON-like string
        # TODO: Add actual parsing & validation here

        return self.orchestrator.handle_structured(eval(structured))  # Use json.loads in production
