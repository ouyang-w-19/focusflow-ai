# agents/journal_agent.py

from agents.base_agent import BaseAgent

class JournalAgent(BaseAgent):
    def handle(self, input_data: dict) -> dict:
        return {
            "markdown": "📝 JournalAgent is not yet implemented.",
            "memory_update": {},
            "suggested_followup": None
        }
