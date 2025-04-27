# agents/frontend_agent/dialog_manager.py

class DialogManager:
    def __init__(self, schema: dict):
        self.schema = schema
        self.state = {}

    def is_complete(self) -> bool:
        return all(field in self.state for field in self.schema["required_fields"])

    def update_field(self, field_name: str, value: str):
        self.state[field_name] = value

    def next_missing_field(self) -> str:
        for field in self.schema["required_fields"]:
            if field not in self.state:
                return field
        return None