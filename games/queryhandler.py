from typing import Callable
from pydantic import BaseModel
from llms.clients import get_client
import json


class LLMInfo(BaseModel):
    model: str


class QueryHandler:
    def __init__(self, action_type, system_query: str, player_info: LLMInfo):
        self.action_type = action_type
        self.system_query = system_query
        self.player_info = player_info
        self.query_object = get_client(player_info.model, system_query)

    def handle_response(self, response: str):
        try:
            json_response = json.loads(response)
        except json.JSONDecodeError:
            raise ValueError("Response is not a valid JSON")

        return self.action_type(**json_response)

    def get_query_object(self) -> Callable:
        return self.query_object

    def query_player(self, player_id: str, prompt: str):
        query_object = self.get_query_object()
        response = query_object(prompt)
        return self.handle_response(response)


def main():
    class TestActionType(BaseModel):
        action: str
        value: int
        reason: str

    query_handler = QueryHandler(
        TestActionType,
        """This is a test prompt. Your objective is to return a JSON response with the action and value.
        Give us the following structured output:
        {
            "action": Literal["buy", "sell"],
            "value": float,
            "reason": str,
        }
        """,
        LLMInfo(model="gpt-4o"),
    )

    print(query_handler.query_player("test", "What is the best action to take?"))


if __name__ == "__main__":
    main()
