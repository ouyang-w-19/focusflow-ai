import os
from dotenv import load_dotenv

# load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '.env'))  # adjust path as needed
load_dotenv()

OLLAMA_HOST = os.getenv("OLLAMA_HOST")