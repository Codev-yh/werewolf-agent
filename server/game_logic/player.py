"""Contains the definition of players and related classes"""

from enum import Enum


class Character(Enum):
    """The character enum"""

    VILLAGER = "villager"
    WITCH = "witch"
    HUNTER = "hunter"
    WEREWOLF = "werewolf"
    GUARD = "guard"
    SEER = "seer"


# pylint: disable=too-few-public-methods
# ^ TODO: remove it after the class finished
class Player:
    """The player class."""
