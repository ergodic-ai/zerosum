from pydantic import BaseModel


class PlayerAction(BaseModel):
    message: str
    make_offer: bool
    accept_offer: bool
    offer_value: float
