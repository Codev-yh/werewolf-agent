"""Contains the configuration of a game."""

from dataclasses import dataclass
from typing import Dict

from game_logic.player import Role


@dataclass
class GameConfig:
    """The game config class"""

    player_number: int
    character_count: Dict[Role, int]


NORMAL_CONFIG_6_PLAYER = GameConfig(
    6,
    {
        Role.VILLAGER: 2,
        Role.WEREWOLF: 2,
        Role.PROPHET: 1,
        Role.WITCH: 1,
    },
)

NORMAL_CONFIG_9_PLAYER = GameConfig(
    9,
    {
        Role.VILLAGER: 3,
        Role.WEREWOLF: 3,
        Role.PROPHET: 1,
        Role.WITCH: 1,
        Role.HUNTER: 1,
    },
)
