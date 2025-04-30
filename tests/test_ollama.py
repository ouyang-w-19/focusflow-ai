from config import OLLAMA_HOST
from langchain_ollama import OllamaLLM
import time

model_list = ["qwen2:7b", "qwen2.5:3b", "deepseek-r1:1.5b", "qwen3:1.7b", "qwen3:4b"]
model_name = model_list[1]
print(model_name)
llm = OllamaLLM(model=model_name)
start_time = time.time()
print(llm.invoke("Give me 3 time management tips."))
end_time = time.time()
elapsed_time = end_time - start_time
print(f"\nTime taken: {elapsed_time:.2f} seconds.")
