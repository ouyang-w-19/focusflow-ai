from langchain_ollama import OllamaLLM
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableSequence

class TaskAgent:
    def __init__(self, model_name="qwen2:7b"):
        self.llm = OllamaLLM(model=model_name)

        self.prompt = PromptTemplate.from_template(
            "You are a productivity coach. Break down the following goal into clear, actionable steps:\n"
            "Goal: {goal}\n\n"
            "Subtasks:"
        )

        # Build a chain using RunnableSequence
        self.chain: RunnableSequence = self.prompt | self.llm

    def plan(self, goal: str) -> str:
        return self.chain.invoke({"goal": goal}).strip()
