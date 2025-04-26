import os
import json
from agents.frontend_agent.intent_detector import IntentDetector
from agents.frontend_agent.field_collector import FieldCollector
from agents.frontend_agent.dialog_manager import DialogManager
from agents.frontend_agent.dispatcher import Dispatcher

class FrontendAgent:
    STRUCTURED_INTENTS = {"planning", "goal_tracking", "habit_building", "retrospectives", "time_auditing", "obstacle_management", "vision_mission_definition", "idea_capture"}

    def __init__(self, provider="ollama", model="qwen2:7b", dispatcher_endpoint="http://localhost:8000/forward"):
        self.intent_detector = IntentDetector(provider=provider, model=model)
        self.field_collector = FieldCollector(provider=provider, model=model)
        self.dispatcher = Dispatcher(endpoint_url=dispatcher_endpoint)

    def load_schema(self, intent: str) -> dict:
        schema_path = os.path.join("schemas", f"{intent}_schema.json")
        if os.path.exists(schema_path):
            with open(schema_path, "r") as f:
                return json.load(f)
        else:
            raise FileNotFoundError(f"Schema file for intent '{intent}' not found.")

    def run(self, user_input: str):
        intents = self.intent_detector.detect_intents(user_input)

        if not intents:
            print("🤖 Sorry, I couldn't understand your request. Could you please rephrase?")
            return

        for intent in intents:
            if intent in self.STRUCTURED_INTENTS:
                schema = self.load_schema(intent)
                dialog_manager = DialogManager(schema)

                while not dialog_manager.is_complete():
                    missing_field = dialog_manager.next_missing_field()
                    retries = 0
                    max_retries = 2

                    while retries <= max_retries:
                        field_value = self.field_collector.collect_field(missing_field, dialog_manager.state)
                        if field_value.strip():
                            dialog_manager.update_field(missing_field, field_value)
                            break
                        else:
                            print(f"🤖 I didn't catch that. Could you tell me about '{missing_field}' again?")
                            retries += 1

                    if retries > max_retries:
                        print(f"⚠️ Skipping field '{missing_field}' after {max_retries} attempts.")
                        break

                structured_data = {
                    "intent": intent,
                    "fields": dialog_manager.state
                }
                self.dispatcher.dispatch(structured_data)
            else:
                self.dispatcher.dispatch({
                    "intent": intent,
                    "original_user_input": user_input,
                    "note": "Specialized agent should handle the full conversational flow."
                })