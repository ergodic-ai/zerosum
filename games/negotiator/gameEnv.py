from games.structs.GameEnv import GameEnvironment
from games.negotiator.playeraction import PlayerAction


class NegotiatorGameEnv:
    def __init__(self):
        super().__init__()
        self.history = []
        self.current_step = 0
        self.roles = {}
        self.who_goes_first = "BUYER"

    def reset(self):
        self.history = []
        self.current_step = 0

    def make(self, players):
        self.roles = {
            player: "BUYER" if player % 2 == 0 else "SELLER" for player in players
        }
        self.reset()

    def get_order(self):
        if self.who_goes_first == "BUYER":
            return ["BUYER", "SELLER"]
        else:
            return ["SELLER", "BUYER"]

    def stepIndividual(self, player_id: str, action: PlayerAction):
        pass

    def stepAll(self):
        raise NotImplementedError("stepAll not valid for this game.")
