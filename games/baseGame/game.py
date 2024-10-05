from games.queryhandler import QueryHandler
from games.structs.GameDefinition import GameDefinition
from games.structs.GameEnv import GameEnvironment
from games.tetris.playeraction import PlayerAction


class Game(GameDefinition):
    # todo should players be a dictionary of name, handler type?
    def __init__(self, gameEnv: GameEnvironment, players: list[str], parallel: bool = False):
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
        self.gameEnv.get_role("")
        # todo system prompt needs to be set per handler and be role specific
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
                state = self.gameEnv.get_state
                query = self.gameEnv.build_query(state)
                response = handlers[player_id].query_player(query)
                actions[player_id] = response
                if not self.parallel:
                    step_response = self.gameEnv.step_individual(response)
                    observations[player_id] = step_response
            if self.parallel:
                observation, reward, done, info = self.gameEnv.step_all(actions)

        # atm observations not used -> todo store to database

    def score(self) -> dict[str, int]:
        pass
