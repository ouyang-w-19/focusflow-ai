import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from config import OLLAMA_HOST

print("OLLAMA_HOST =", OLLAMA_HOST)

from langchain_ollama import OllamaLLM

ollama_host = os.getenv("OLLAMA_HOST")
llm = OllamaLLM(model="qwen2:7b", base_url=ollama_host)
print(llm.invoke("Give me 3 time management tips."))

