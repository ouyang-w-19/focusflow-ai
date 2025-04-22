# agents/goal_tracker_agent.py

from agents.base_agent import BaseAgent

class GoalTrackerAgent(BaseAgent):
    def handle(self, input_data: dict) -> dict:
        return {
            "markdown": "🎯 GoalTrackerAgent is not yet implemented.",
            "memory_update": {},
            "suggested_followup": None
        }
