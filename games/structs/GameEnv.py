from games.structs.GameState import GameState
from games.structs.StepReponse import StepResponse


class GameEnvironment():

    def __init__(self):
        # state stored here
        pass

    def make(self):
        pass

    def reset(self):
        pass

    def stepIndividual(self) -> StepResponse:
        pass

    def stepAll(self) -> StepResponse:
        pass

    def get_state(self) -> GameState:
        pass

    def get_system_prompt(self) -> str:
        pass

    def build_query(self) -> str:
        pass
