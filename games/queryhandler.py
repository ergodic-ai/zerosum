from typing import Callable
from pydantic import BaseModel
from llms.clients import get_client
import json


class QueryHandler:
    def __init__(self, action_type, system_query: str, model: str):
        self.action_type = action_type
        self.system_query = system_query
        self.model = model
        self.query_object = get_client(model, system_query)

    def handle_response(self, response: str):
        try:
            json_response = json.loads(response)
        except json.JSONDecodeError:
            raise ValueError("Response is not a valid JSON")

        return self.action_type(**json_response)

    def get_query_object(self) -> Callable:
        return self.query_object

    def query_player(self, prompt: str):
        query_object = self.get_query_object()
        response = query_object(prompt)
        return self.handle_response(response)


def main():
    from llms.client_groq import SUPPORTED_MODELS

    class TestActionType(BaseModel):
        action: str
        value: float
        reason: str

    for model in SUPPORTED_MODELS:
        try:
            query_handler = QueryHandler(
                TestActionType,
                """This is a test prompt. Your objective is to return a JSON response with the action and value.
            Give us the following structured output:
            {
                "action": "buy" or "sell",
                "value": float,
                "reason": str,
            }
            """,
                model,
            )
            print(model)
            print(query_handler.query_player("What is the best action to take?"))
        except Exception as e:
            print(f"Error with model {model}: {e}")


if __name__ == "__main__":
    main()
