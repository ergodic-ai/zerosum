from typing import Literal
from pydantic import BaseModel


class PlayerAction(BaseModel):
    move: Literal["left", "right", "up", "down"]
    rotate: Literal["clockwise", "counterclockwise"]
    drop: bool
