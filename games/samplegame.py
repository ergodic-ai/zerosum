from typing import Callable, Literal
from pydantic import BaseModel
from games.gamedef import Gamedef


# class PlayerAction( BaseModel ):
#     move: Literal["left", "right", "up", "down"]


class QueryHandler:
    def __init__(self, game: Gamedef, player_info: dict[str, str]):
        self.game = game
        self.player_info = player_info

    def handle_response(self, response: str) -> PlayerAction:
        pass

    def get_query_object(self) -> callable:
        # return lambda x: query( x ) > str
        pass

    def query_player(self, player_id: str, prompt: str) -> PlayerAction:
        query_object = self.get_query_object()
        response = query_object(prompt)
        return self.handle_response(response)


class SampleGame(Gamedef):
    def __init__(self):
        super().__init__(
            name="Maze Game",
            description="You are in a maze. You can move left, right, up, or down.",
            n_players=1,
            rules="You can only move left, right, up, or down.",
            actions="You can move left, right, up, or down.",
            action_format=PlayerAction,  # change later
        )

    def reset(self):
        pass

    def get_players_handlers(self) -> dict[str, QueryHandler]:
        pass

    def get_step_string(self, state, previous_actions, previous_rewards) -> str:
        pass

    def run(self):
        state = self.reset()
        done = False
        system_prompt = self.get_system_prompt()
        handlers = self.get_players_handlers()

        while not done:
            actions = {}
            for player_id in self.players:

                response = handlers[player_id].query_player(
                    self.get_step_string(state, actions, rewards)
                )
                actions[player_id] = response

            state, reward, done, info = self.step(actions)
            # store to database

    def step(
        self, actions: list[str, PlayerAction]
    ) -> tuple(state, reward, done, info):
        pass

    def score(self) -> dict[str, int]:
        pass
