from llm.llm_wrapper import LLMWrapper
from langchain.prompts import ChatPromptTemplate

class IntentDetector:
    def __init__(self, provider="ollama", model="qwen2:7b"):
        self.llm = LLMWrapper(provider=provider, model=model)
        self.prompt = ChatPromptTemplate.from_template(
            """
            Determine the user's intent based on the input.
            Respond only with one word: 'planning', 'journaling', 'reflecting', or 'goal_tracking'.

            Input: {user_input}
            """
        )
        self.chain = self.prompt | self.llm

    def detect_intent(self, user_input: str) -> str:
        return self.chain.invoke({"user_input": user_input})