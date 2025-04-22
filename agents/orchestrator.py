# agents/orchestrator.py

from agents.base_agent import BaseAgent
from agents.planning_agent import PlanningAgent
from agents.journal_agent import JournalAgent
from agents.goal_tracker_agent import GoalTrackerAgent

'''
Orchestrator – Non-LLM controller for routing structured input to agents.
Not an intelligent agent.
Can optionally process raw input using keyword-based intent routing.
'''

class Orchestrator:
    def __init__(self, memory=None):
        self.memory = memory
        self.planning_agent = PlanningAgent(memory=memory)
        self.journal_agent = JournalAgent(memory=memory)
        self.goal_agent = GoalTrackerAgent(memory=memory)

    def handle_structured(self, payload: dict) -> dict:
        intent = payload.get("intent", "plan")
        if intent == "plan":
            return self.planning_agent.handle(payload)
        elif intent == "journal":
            return self.journal_agent.handle(payload)
        elif intent == "goal":
            return self.goal_agent.handle(payload)
        else:
            return {
                "markdown": "🤖 I don't recognize that intent.",
                "memory_update": {},
                "suggested_followup": "Can you clarify what you'd like to do?"
            }

    def handle_raw(self, user_input: str) -> dict:
        '''
        Basic raw input handler using keyword rules to infer intent.
        This bypasses FrontendAgent for faster routing when input is clear.
        '''
        text = user_input.lower()
        if "reflect" in text or "journal" in text:
            return self.journal_agent.handle({"intent": "journal", "original_input": user_input})
        elif "goal" in text or "milestone" in text:
            return self.goal_agent.handle({"intent": "goal", "original_input": user_input})
        else:
            return self.planning_agent.handle({"intent": "plan", "original_input": user_input})
