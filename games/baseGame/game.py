from games.queryhandler import QueryHandler
from games.structs.GameDefinition import GameDefinition
from games.structs.StepReponse import StepResponse
from games.tetris.playeraction import PlayerAction


class Game(GameDefinition):
    # todo should players be a dictionary of name, handler type?
    def __init__(self, gameEnv: any, players: list[str], parallel: bool = False):
        super().__init__(
            gameEnv=gameEnv,
            description="You are in a maze. You can move left, right, up, or down.",
            n_players=1,
            rules="You can only move left, right, up, or down.",
            actions="You can move left, right, up, or down.",
            action_format=PlayerAction,  # change later
            players=players,
            parallel=parallel
        )

    def get_players_handlers(self) -> dict[str, QueryHandler]:
        pass

    def get_step_string(self, state, previous_actions, previous_rewards) -> str:
        pass

    def run(self):
        # should go in the reset
        self.gameEnv.make(self.players)
        self.gameEnv.reset()
        done = False
        handlers = self.get_players_handlers()

        while not done:
            actions: dict[str, any] = {} # any could be passed into
            observations: dict[str, any]  = {} # player to state dict
            for player_id in self.players:
                system_prompt = self.gameEnv.get_system_prompt(player_id)
                # response = self.gameEnv.action_space.sample() # todo replace with below query handler
                state = self.gameEnv.get_state
                query = self.gameEnv.build_query(state)
                response = handlers[player_id].query_player(query)
                actions[player_id] = response
                if not self.parallel:
                    step_response = self.gameEnv.stepIndividual(response)
                    observations[player_id] = step_response
            if self.parallel:
                observation, reward, done, info = self.gameEnv.stepAll(actions[player_id])

        # atm observations not used -> todo store to database

    def score(self) -> dict[str, int]:
        pass

    def get_system_prompt(self):
        pass