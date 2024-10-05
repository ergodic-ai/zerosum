from dataclasses import dataclass
from typing import Any, Dict

@dataclass
class GameState:
    env: Any
    done: bool
    players: list[str]
    info: Dict[str, Any]