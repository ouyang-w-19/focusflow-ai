# llm/llm_wrapper.py
from config import OLLAMA_HOST

class LLMWrapper:
    def __init__(self, provider="ollama", model="qwen2.5:3b"):
        if provider == "ollama":
            from langchain_ollama import ChatOllama
            self.llm = ChatOllama(model=model)
        elif provider == "openai":
            from langchain_openai import ChatOpenAI
            self.llm = ChatOpenAI(model="gpt-4")
        else:
            raise ValueError("Unsupported provider. Use 'ollama' or 'openai'.")

    def __call__(self, prompt: str) -> str:
        return self.llm.invoke(prompt)
