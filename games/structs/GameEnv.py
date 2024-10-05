from games.structs.GameState import GameState
from games.structs.StepReponse import StepResponse


class GameEnvironment:

    def __init__(self):
        self.state: any
        # todo extend as required

    def make(self, players: list[str]):
        pass

    def reset(self):
        pass

    def get_role(self, player_id: str) -> str:
        pass

    def step_individual(self, action: any) -> StepResponse:
        pass

    def step_all(self, actions: dict[str, any]) -> StepResponse:
        pass

    def get_state(self) -> GameState:
        pass

    def get_system_prompt(self, player_id: str) -> str:
        pass

    def build_query(self, state: any) -> str:
        pass
