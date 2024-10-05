from typing import Optional
from pydantic import BaseModel
from games.structs.GameEnv import GameEnvironment
from games.negotiator.playeraction import PlayerAction


class GameHistoryItem(BaseModel):
    player_id: str
    player_role: str
    action: PlayerAction
    step_n: int


class NegotiatorGameEnv(GameEnvironment):
    def __init__(self):
        super().__init__()
        self.history = []
        self.current_step = 0
        self.roles = {}
        self.inv_roles = {}
        self.players = []
        self.who_goes_first = "BUYER"
        self.next_role = self.who_goes_first
        self.max_steps = 20
        self.mid_price = 100
        self.buyer_price = 110
        self.seller_price = 90
        self.score = {}
        self.history: list[GameHistoryItem] = []

    def reset(self):
        self.history = []
        self.current_step = 0
        self.next_role = self.who_goes_first

    def get_next_player(self):
        return self.inv_roles[self.next_role]

    def make(self, players: list[str]):
        self.players = players
        self.roles = {}
        self.inv_roles = {}
        self.reset()

        if len(players) != 2:
            raise ValueError("Must have exactly 2 players.")

        self.roles = {
            players[0]: "BUYER",
            players[1]: "SELLER",
        }

        self.inv_roles = {
            "BUYER": players[0],
            "SELLER": players[1],
        }

        self.score = {
            players[0]: 0.0,
            players[1]: 0.0,
        }

    def get_role(self, player_id: str) -> str:
        return self.roles[player_id]

    def get_order(self):
        if self.who_goes_first == "BUYER":
            return [self.inv_roles["BUYER"], self.inv_roles["SELLER"]]
        else:
            return [self.inv_roles["SELLER"], self.inv_roles["BUYER"]]

    def stepIndividual(self, player_id: str, action: PlayerAction):
        player_role = self.roles[player_id]
        if player_role != self.next_role:
            raise ValueError(f"It is not {player_role}'s turn to play.")

        self.history.append(
            GameHistoryItem(
                player_id=player_id,
                player_role=player_role,
                action=action,
                step_n=self.current_step,
            )
        )
        self.current_step += 1
        self.next_role = "BUYER" if self.next_role == "SELLER" else "SELLER"
        done, score = self._evaluate_step()
        return "", done, score

    def build_query(self, player_id: str) -> str:
        return self.get_state(player_id)

    def _evaluate_step(self):
        buyer_player = self.inv_roles["BUYER"]
        seller_player = self.inv_roles["SELLER"]
        agreed_price = None

        prev_two_actions = self.history[-2:]
        if len(prev_two_actions) != 2:
            return False, None

        is_offer_accepted = prev_two_actions[-1].action.accept_offer
        offers_match = (
            prev_two_actions[-1].action.offer_value
            == prev_two_actions[-2].action.offer_value
        )
        if is_offer_accepted and offers_match:
            agreed_price = prev_two_actions[-1].action.offer_value
            if agreed_price is not None:
                self.agreed_price = agreed_price
                self.score[buyer_player] = (self.mid_price - agreed_price) / 2
                self.score[seller_player] = (agreed_price - self.mid_price) / 2

                return True, self.score

        if self.current_step == self.max_steps:
            self.score[buyer_player] = -5
            self.score[seller_player] = -5
            return True, self.score

        return False, None

    def get_state(self, player_id: Optional[str] = None) -> str:
        if player_id is None:
            return self.get_state(self.inv_roles["BUYER"])

        if len(self.history) == 0:
            return f"You are the {self.roles[player_id]}. What is your next action?"

        history_string = ""
        for history_item in self.history:
            history_string += (
                f"{history_item.player_role} said: {history_item.action.message}\n"
            )
            if history_item.action.make_offer:
                history_string += f"Narrator: {history_item.player_role} has a formal offer of: {history_item.action.offer_value}.\n"
            if history_item.action.accept_offer:
                history_string += (
                    f"Narrator: {history_item.player_role} has accepted the offer.\n"
                )

        response_string = (
            f"""Here is the history of your conversation:\n\n {history_string}\n\n"""
        )
        response_string += f"""You have the role of {self.roles[player_id]}. What is your next action?\n\n"""
        response_string += f"""Remember, there are only {self.max_steps - self.current_step} steps left."""
        return response_string

    def stepAll(self):
        raise NotImplementedError("stepAll not valid for this game.")


def test():
    game_env = NegotiatorGameEnv()
    game_env.make(["A", "B"])
    game_env.reset()

    next_player = game_env.get_next_player()
    next_action = PlayerAction(
        message="I offer 110 dollars for the car.",
        accept_offer=False,
        make_offer=True,
        offer_value=110,
    )
    game_env.stepIndividual(next_player, next_action)
    next_player = game_env.get_next_player()

    next_action = PlayerAction(
        message="I accept the offer.",
        accept_offer=True,
        make_offer=False,
        offer_value=110,
    )
    game_env.stepIndividual(next_player, next_action)
    next_player = game_env.get_next_player()
    print(game_env._evaluate_step())
    print(game_env.get_state(next_player))


if __name__ == "__main__":
    test()
