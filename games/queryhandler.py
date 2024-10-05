from typing import Callable
from pydantic import BaseModel


class LLMInfo(BaseModel):
    model: str


class QueryHandler:
    def __init__(self, action_type, player_info: LLMInfo):
        self.action_type = action_type
        self.player_info = player_info

        self.client = get_client(player_info)

    def handle_response(self, response: str):
        pass

    def get_query_object(self) -> Callable:
        return self.client.query

    def query_player(self, player_id: str, prompt: str):
        query_object = self.get_query_object()
        response = query_object(prompt)
        return self.handle_response(response)
