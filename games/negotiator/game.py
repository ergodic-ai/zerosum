from typing import Optional
from games.gamedef import Gamedef

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
""".format(
    product_description=PRODUCT_DESCRIPTION
)

SELLER_PROMPT = """You are a seller. Your objective is to sell the following product:
{product_description}
Your goal is to sell the product for as much as possible. You can sell the product for at least {seller_min_price} credits. But you must haggle to be able 
to sell the product for as much as possible.
""".format(
    product_description=PRODUCT_DESCRIPTION
)

RULES = """In each round you can either make an offer, accept an offer and include a message as to why the other part should accept your offer."""


class NegoationGame(Gamedef):
    players: dict[str, str]
    buyer_max_price: Optional[int] = 110
    seller_min_price: Optional[int] = 90

    def __init__(self):
        super().__init__(
            name="Negotiation Game",
            description=DESCRIPTION,
            n_players=2,
            rules=RULES,
            actions="You can move left, right, up, or down.",
            action_format=PlayerAction,  # change later
        )

    def get_system_prompt(self, **kwargs) -> str:
        role = kwargs.get("role", "seller")
        if role == "seller":
            ctx = SELLER_PROMPT.format(seller_min_price=self.seller_min_price)
        elif role == "buyer":
            ctx = BUYER_PROMPT.format(buyer_max_price=self.buyer_max_price)
        else:
            raise ValueError(f"Invalid role: {role}")

        return ctx

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
