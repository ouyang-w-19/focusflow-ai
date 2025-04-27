# agents/frontend_agent/intent_detector.py

from llm.llm_wrapper import LLMWrapper
from langchain.prompts import ChatPromptTemplate

class IntentDetector:
    def __init__(self, provider="ollama", model="qwen2:7b"):
        self.llm = LLMWrapper(provider=provider, model=model)
        self.prompt = ChatPromptTemplate.from_template(
            """
            Identify all relevant intents in the user's input.
            Possible intents: planning, goal_tracking, habit_building, prioritization,
            journaling, reflecting, gratitude, motivation_boost,
            retrospectives, time_auditing, obstacle_management,
            vision_mission_definition, idea_capture.

            Input: {user_input}

            Respond with a comma-separated list of intents.
            """
        )
        self.chain = self.prompt | self.llm

    def detect_intents(self, user_input: str) -> list[str]:
        response = self.chain.invoke({"user_input": user_input})
        intents = [intent.strip() for intent in response.split(",") if intent.strip()]
        return intents