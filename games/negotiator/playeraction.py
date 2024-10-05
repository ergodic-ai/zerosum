from typing import Optional
from pydantic import BaseModel


class PlayerAction(BaseModel):
    message: str
    make_offer: Optional[bool] = False
    accept_offer: Optional[bool] = False
    offer_value: Optional[float] = None


if __name__ == "__main__":
    print(
        PlayerAction(
            message="Hello", make_offer=True, accept_offer=False, offer_value=0.5
        )
    )

    print(PlayerAction.schema())
