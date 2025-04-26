from llm.llm_wrapper import LLMWrapper
from langchain.prompts import ChatPromptTemplate

class FieldCollector:
    def __init__(self, provider="ollama", model="qwen2:7b"):
        self.llm = LLMWrapper(provider=provider, model=model)
        self.prompt_template = (
            """
            You are helping collect structured data for {intent}.
            Context so far: {context}.
            User has already shared: {collected_fields}.
            Please ask a polite, natural question to get the missing field: '{missing_field}'.
            """
        )

    def collect_field(self, missing_field: str, context: dict) -> str:
        prompt = ChatPromptTemplate.from_template(self.prompt_template)
        chain = prompt | self.llm

        # Prepare short-term memory: collected fields context
        collected_fields = {k: v for k, v in context.items() if v}

        return chain.invoke({
            "intent": context.get("intent", "an activity"),
            "context": context,
            "collected_fields": collected_fields,
            "missing_field": missing_field
        })