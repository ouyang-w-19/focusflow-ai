# agents/frontend_agent/frontend_agent.py

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
            
        intent = intents[0]  # 🔥 Only focus on first intent detected   
        # for intent in intents:
        if intent in self.STRUCTURED_INTENTS:
            schema = self.load_schema(intent)

            # Prefill fields from user input before starting
            prefilled_fields = self.field_collector.prefill_fields(user_input, schema)

            dialog_manager = DialogManager(schema)

            # Update dialog manager with prefilled fields
            for field_name, field_value in prefilled_fields.items():
                dialog_manager.update_field(field_name, field_value)

                
            # Now proceed to ask missing fields only
            while not dialog_manager.is_complete():
                missing_field = dialog_manager.next_missing_field()
                if missing_field is None:
                    break  # 🔥 Very important fix

                # 🚀 SIMPLIFIED: No retry loop here anymore
                field_value = self.field_collector.collect_field(missing_field, dialog_manager.state)
                dialog_manager.update_field(missing_field, field_value)

            structured_data = {
                "intent": intent,
                "fields": dialog_manager.state
            }
            # self.dispatcher.dispatch(structured_data)
            print("\n✅ Session Summary:")
            for field, value in dialog_manager.state.items(): 
                print(f"  - {field}: {value}")

        else:
            # self.dispatcher.dispatch({
            #     "intent": intent,
            #     "original_user_input": user_input,
            #     "note": "Specialized agent should handle the full conversational flow."
            # })
            print({
                "intent": intent,
                "original_user_input": user_input,
                "note": "Specialized agent should handle the full conversational flow."
            })


if __name__ == "__main__":
    user_input = input("You: ")
    frontendagent = FrontendAgent(model="qwen2.5:3b")
    frontendagent.run(user_input)

