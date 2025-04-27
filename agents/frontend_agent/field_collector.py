# agents/frontend_agent/field_collector.py

from llm.llm_wrapper import LLMWrapper
from langchain.prompts import ChatPromptTemplate

class FieldCollector:
    def __init__(self, provider="ollama", model="qwen2:7b"):
        self.llm = LLMWrapper(provider=provider, model=model)
        self.prompt_template = (
            """
            You are helping collect structured data for {intent}.
            Context so far: {context}.
            User has already shared: {collected_fields}.
            Please ask a polite, natural question to get the missing field: '{missing_field}'.
            """
        )

    # def prefill_fields(self, user_input: str, schema: dict) -> dict:
    #     prefilled = {}

    #     for field in schema["required_fields"]:
    #         # Build LLM prompt: "Does this text contain the {field} value? If yes, extract it."
    #         prompt = ChatPromptTemplate.from_template(
    #             """
    #             User Input: {user_input}
    #             Field to extract: {field}

    #             Extract the most relevant value for this field from the input text.
    #             If not possible, respond with "none".
    #             """
    #         )
    #         chain = prompt | self.llm
    #         extracted = chain.invoke({
    #             "user_input": user_input,
    #             "field": field
    #         })

    #         if extracted.lower() != "none":
    #             prefilled[field] = extracted

    #     return prefilled

    def prefill_fields(self, user_input: str, schema: dict) -> dict:
        fields = schema["required_fields"]

        prompt = ChatPromptTemplate.from_template(
            """
            User Input: {user_input}
            Fields to Extract: {fields}

            Extract as many fields as possible based on the input.
            Respond in JSON format, one key per field.
            If a field cannot be found, set its value to "none".
            Example response:
            {{
            "field1": "...",
            "field2": "none",
            "field3": "..."
            }}
            """
        )
        chain = prompt | self.llm
        response = chain.invoke({
            "user_input": user_input,
            "fields": fields
        })

        # Basic parsing
        import json
        prefilled = json.loads(response)

        # Remove fields with "none"
        clean_prefilled = {k: v for k, v in prefilled.items() if v.lower() != "none"}

        return clean_prefilled


    def generate_question(self, missing_field: str, context: dict) -> str:
        prompt = ChatPromptTemplate.from_template(self.prompt_template)
        chain = prompt | self.llm
        collected_fields = {k: v for k, v in context.items() if v}
        question = chain.invoke({
            "intent": context.get("intent", "an activity"),
            "context": context,
            "collected_fields": collected_fields,
            "missing_field": missing_field
        })
        return question
    

    def validate_field(self, missing_field: str, user_answer: str, question: str) -> tuple[bool, str]:
        validation_prompt = ChatPromptTemplate.from_template(
            """
            Field: {missing_field}
            Question Asked: {question}
            User Answer: {user_answer}

            1. Determine if the user's answer appropriately and fully answers the question asked for this field.
            2. Respond only 'valid' or 'invalid'.
            3. If invalid, suggest a short hint (max 1 sentence) on how the user can improve their answer.

            Respond in JSON format:
            {{
                "validation": "valid" or "invalid",
                "hint": "your suggested hint or empty string if valid"
            }}
            """
        )
        chain = validation_prompt | self.llm
        response = chain.invoke({
            "missing_field": missing_field,
            "user_answer": user_answer,
            "question": question
        })

        if '"validation": "valid"' in response:
            return True, ""
        else:
            hint_start = response.find('"hint":') + len('"hint":')
            hint = response[hint_start:].strip().lstrip(':').strip(' "{}')
            return False, hint


    def collect_field(self, missing_field: str, context: dict) -> str:
        max_retries = 2
        retries = 0

        question = self.generate_question(missing_field, context)
        print(f"🤖: {question}")

        while retries <= max_retries:
            user_answer = input("You: ").strip()

            if not user_answer:
                print(f"⚠️ I didn't catch that. Could you please try again?")
                retries += 1
                continue

            is_valid, hint = self.validate_field(missing_field, user_answer, question)

            if is_valid:
                return user_answer

            print(f"⚠️ It seems your answer doesn't fully match what we need for '{missing_field}'.")
            if hint:
                print(f"💡 Hint: {hint}")
            retries += 1

        print("⚠️ Accepting your last input anyway.")
        return user_answer

