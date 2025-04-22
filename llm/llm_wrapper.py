# llm/llm_wrapper.py

class LLMWrapper:
    def __init__(self, provider="ollama", model="qwen2:7b"):
        if provider == "ollama":
            from langchain_ollama import OllamaLLM
            self.llm = OllamaLLM(model=model)
        elif provider == "openai":
            from langchain_openai import ChatOpenAI
            self.llm = ChatOpenAI(model="gpt-4")
        else:
            raise ValueError("Unsupported provider. Use 'ollama' or 'openai'.")

    def __call__(self, prompt: str) -> str:
        return self.llm.invoke(prompt)
