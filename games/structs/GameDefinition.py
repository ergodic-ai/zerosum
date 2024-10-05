from dataclasses import dataclass
from lib2to3.btm_matcher import BottomMatcher
from typing import Any

@dataclass
class GameDefinition:
    gameEnv: any
    description: str
    n_players: int
    rules: str
    actions: str
    action_format: Any  # change later
    objective: str
    players: list[str]
    parallel: bool