from dataclasses import dataclass
from typing import Any, Dict

from games.structs.GameState import GameState


@dataclass
class StepResponse:
    state: GameState
    reward: float
    done: bool
    info: Dict[str, Any]