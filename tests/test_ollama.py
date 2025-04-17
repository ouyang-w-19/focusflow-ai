from config import OLLAMA_HOST
from langchain_ollama import OllamaLLM

# print("OLLAMA_HOST =", OLLAMA_HOST)
llm = OllamaLLM(model="qwen2:7b")
print(llm.invoke("Give me 3 time management tips."))

