# agents/frontend_agent/dispatacher.py

import requests

class Dispatcher:
    def __init__(self, endpoint_url: str):
        self.endpoint_url = endpoint_url

    def dispatch(self, structured_input: dict) -> bool:
        response = requests.post(self.endpoint_url, json=structured_input)
        return response.ok