from games.negotiator.gameEnv import NegotiatorGameEnv
from games.negotiator.playeraction import PlayerAction
from games.negotiator.queryhandler import QueryHandler
from games.structs.GameDefinition import GameDefinition
from games.negotiator.playeraction import PlayerAction

DESCRIPTION = """This is a negotiation game where you can make offers to other players. There is a SELLER and a BUYER. 
The SELLER must get as much value as possible for their product. The BUYER must pay as little as possible for the product.
If no agreement is reached in 10 steps, both players lose.  
"""

PRODUCT_DESCRIPTION = """The product in question is a piece of unobtainum. 
This piece of unobtainum is vital for the manufacturing of flux capacitors that power 
the most sophisticated time machine in the world."""

BUYER_PROMPT = """You are a buyer. Your objective is to buy the following product:
{product_description}
Your goal is to buy the product for as little as possible. You can pay up to {buyer_max_price} credits for the product. But you must haggle to be able 
to pay as little as possible.
"""

SELLER_PROMPT = """You are a seller. Your objective is to sell the following product:
{product_description}
Your goal is to sell the product for as much as possible. You can sell the product for at least {seller_min_price} credits. But you must haggle to be able 
to sell the product for as much as possible.
"""

RULES = """In each round you can either make an offer, accept an offer and include a message as to why the other part should accept your offer."""


# class NegoationGame(Gamedef):
#     players: dict[str, str]
#     buyer_max_price: Optional[int] = 110
#     seller_min_price: Optional[int] = 90

#     def __init__(self):
#         super().__init__(
#             name="Negotiation Game",
#             description=DESCRIPTION,
#             n_players=2,
#             rules=RULES,
#             actions="You can move left, right, up, or down.",
#             action_format=PlayerAction,  # change later
#         )

#     def get_system_prompt(self, **kwargs) -> str:
#         role = kwargs.get("role", "seller")
#         if role == "seller":
#             ctx = SELLER_PROMPT.format(seller_min_price=self.seller_min_price)
#         elif role == "buyer":
#             ctx = BUYER_PROMPT.format(buyer_max_price=self.buyer_max_price)
#         else:
#             raise ValueError(f"Invalid role: {role}")

#         return ctx

#     def reset(self):
#         pass

#     def get_players_handlers(self) -> dict[str, QueryHandler]:
#         pass

#     def get_step_string(self, state, previous_actions, previous_rewards) -> str:
#         pass

#     def run(self):
#         state = self.reset()
#         done = False
#         system_prompt = self.get_system_prompt()
#         handlers = self.get_players_handlers()

#         while not done:
#             actions = {}
#             for player_id in self.players:

#                 response = handlers[player_id].query_player(
#                     self.get_step_string(state, actions, rewards)
#                 )
#                 actions[player_id] = response

#             state, reward, done, info = self.step(actions)
#             # store to database

#     def step(
#         self, actions: list[str, PlayerAction]
#     ) -> tuple(state, reward, done, info):
#         pass

#     def score(self) -> dict[str, int]:
#         pass


class Game(GameDefinition):
    # todo should players be a dictionary of name, handler type?
    def __init__(
        self, gameEnv: NegotiatorGameEnv, players: list[str], parallel: bool = False
    ):
        gameEnv.make(players)
        super().__init__(
            gameEnv=gameEnv,
            description=DESCRIPTION,
            n_players=2,
            rules=RULES,
            actions=PlayerAction.model_json_schema()["properties"],
            action_format=PlayerAction,  # change later
            players=players,
            parallel=parallel,
            objective="The objective of the game is to profit.",
        )
        self.score_dict = None

    def get_system_prompt(self, **kwargs) -> str:
        role = kwargs.get("role", "SELLER")

        if role == "SELLER":
            ctx = SELLER_PROMPT.format(
                seller_min_price=self.gameEnv.seller_price,
                product_description=PRODUCT_DESCRIPTION,
            )
        elif role == "BUYER":
            ctx = BUYER_PROMPT.format(
                buyer_max_price=self.gameEnv.buyer_price,
                product_description=PRODUCT_DESCRIPTION,
            )
        else:
            raise ValueError(f"Invalid role: {role}")

        format_prompt = """\n\nYou must respond with a valid JSON object with the following format:
        {
            message: str
            make_offer: bool
            accept_offer: bool
            offer_value: float  
        }   

        Message should contain the message you want to send to the other player. 
        Make offer should be true if you want to make an offer to the other player.
        Accept offer should be true if you want to accept an offer from the other player.
        Offer value should be the offer you want to make to the other player or the offer value if you are accepting an offer.\n\n
        """

        return ctx + format_prompt

    def get_players_handlers(self) -> dict[str, QueryHandler]:
        h = {}
        for player in self.gameEnv.players:
            role = self.gameEnv.get_role(player)
            system_prompt = self.get_system_prompt(role=role)
            h[player] = QueryHandler(
                action_type=PlayerAction, system_query=system_prompt, model=player
            )

        return h

    # def get_step_string(self, state, previous_actions, previous_rewards) -> str:
    #     pass

    def run(self, verbose: bool = False):
        # should go in the reset
        # self.gameEnv.make(self.players)
        self.gameEnv.reset()
        done = False
        handlers = self.get_players_handlers()
        score_dict = None
        player_id = self.gameEnv.get_next_player()

        while not done:
            actions: dict[str, PlayerAction] = {}  # any could be passed into
            observations: dict[str, str] = {}  # player to state dict

            # for player_id in self.players:
            state = self.gameEnv.get_state(player_id)
            if verbose:
                print(f"Player {player_id}:")
            # query = self.gameEnv.build_query(state)
            query = state
            response = handlers[player_id].query_player(query)
            if verbose:
                print(f"Player {player_id} response: {response}")
            actions[player_id] = response
            if not self.parallel:
                step_response, done, score_dict = self.gameEnv.stepIndividual(
                    player_id, response
                )
                observations[player_id] = step_response

            player_id = self.gameEnv.get_next_player()
            # if self.parallel:
            #     observation, done, score_dict = self.gameEnv.step_all(actions)

        if verbose:
            print(self.gameEnv.get_state())

        # print(get)

        if score_dict is not None:
            self.score_dict = score_dict
        # atm observations not used -> todo store to database

    def score(self) -> dict[str, int]:
        if self.score_dict is None:
            raise ValueError("Score is not set")
        return self.score_dict


def test():
    gameEnv = NegotiatorGameEnv()
    game = Game(gameEnv, ["gpt-4o", "mixtral-8x7b-32768"])
    game.run(verbose=True)
    print(game.score())


if __name__ == "__main__":
    test()
