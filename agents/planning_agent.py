# agents/planning_agent.py

from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableSequence
from langchain_ollama import OllamaLLM
from agents.base_agent import BaseAgent

class PlanningAgent(BaseAgent):
    def __init__(self, memory=None, provider="ollama", model="qwen2:7b"):
        super().__init__(memory, provider=provider, model=model)

        # Define prompt templates for each mode
        self.prompts = {
            "goal_plan": PromptTemplate.from_template(
                "You are a task planner.\n"
                "User goal: \"{user_input}\"\n"
                "Break it into 3–5 actionable subtasks in Markdown list format:"
            ),
            "daily_parse": PromptTemplate.from_template(
                "You are a day planner."
                "User input: \"{user_input}\""
                "Extract today's tasks in bullet format, clearly:"
            ),
            "time_filter": PromptTemplate.from_template(
                "You are a productivity coach."
                "User said: \"{user_input}\""
                "Suggest tasks that fit in the available time (15–90 mins):"
            ),
        }

        # Build LangChain chains for each mode
        self.chains = {k: self.prompts[k] | self.llm for k in self.prompts}

    def detect_mode_simple(self, user_input: str) -> str or None:
        text = user_input.lower()
        if "today" in text or "i'll" in text or "plan" in text:
            return "daily_parse"
        elif "have" in text and ("minute" in text or "hour" in text):
            return "time_filter"
        return None

    def detect_mode_llm(self, user_input: str) -> str:
        routing_prompt = (
            "Classify this input into one of the following planning modes:\n"
            "- goal_plan: vague or high-level task/goal\n"
            "- daily_parse: describes today's intended tasks\n"
            "- time_filter: gives available time for work\n\n"
            f"Input: \"{user_input}\"\nMode:"
        )
        result = self.llm(routing_prompt).strip().lower()
        return result if result in self.prompts else "goal_plan"

    def handle(self, user_input: str) -> dict:
        mode = self.detect_mode_simple(user_input) or self.detect_mode_llm(user_input)
        chain = self.chains[mode]
        output = chain.invoke({"user_input": user_input})

        return {
            "markdown": output.strip(),
            "memory_update": {
                "type": "task_plan",
                "mode": mode,
                "original_input": user_input,
                "output": output.strip()
            },
            "suggested_followup": "Want to schedule these or send to Microsoft To Do?"
        }
