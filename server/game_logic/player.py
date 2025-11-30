import requests
from typing import Any
from enum import Enum, unique

@unique
class Role(Enum):
    """Defines roles used in the game."""
    VILLAGER = "Villager"
    WOLF = "Werewolf"
    PROPHET = "Prophet"
    WITCH = "Witch"
    HUNTER = "Hunter"

    def __str__(self) -> str:
        return self.value
    
    @property
    def is_wolf(self) -> bool:
        return self == Role.WOLF
    
    @property
    def is_cleric(self) -> bool:
        return self in {Role.PROPHET, Role.WITCH, Role.HUNTER}
    
    @property
    def is_hunter(self) -> bool:
        return self == Role.HUNTER
    
    @property
    def is_prophet(self) -> bool:
        return self == Role.PROPHET
    
    @property
    def is_witch(self) -> bool:
        return self == Role.WITCH
    
    @property
    def is_villager(self) -> bool:
        return self == Role.VILLAGER
    
    @property
    def is_good(self) -> bool:
        return self in {Role.VILLAGER, Role.PROPHET, Role.WITCH, Role.HUNTER}


# Represents a player in the game.
class Player:
    # With this typing, elements in Game's `roles: list[Role]` must be
    # `Role` instances, e.g. `[Role.VILLAGER, Role.WOLF]`.
    def __init__(self, player_id: int, role: Role):
        self.id : int = player_id
        self.role : Role = role
        self.is_alive : bool = True

        self.witch_antidote : bool = True  # Witch antidote; True means available
        self.witch_poison : bool = True    # Witch poison; True means available

        self.can_shoot : bool = True  # Indicates whether the hunter can shoot; True means can shoot

        # Prophet check history: contains checked player IDs and roles
        self.prophet_check_history: list[dict[str, Any]] = []

        self.survived_nights : int = 0  # Number of nights the player has survived
        self.vote_correct_counts : int = 0  # Number of times the player voted correctly
        self.mistake_counts : int = 0  # Number of mistakes made (e.g., poisoning a villager)


    def die(self, method: str) -> None :
        # Set the player's state to dead and mark consequences
        # (for example, the hunter may not be able to shoot after death).
        self.is_alive = False
        # If the hunter was poisoned, they cannot shoot.
        if self.role.is_hunter and method == "poison":    
            self.can_shoot = False

    # Display player info
    def __repr__(self) -> str:
        return f"Player(id={self.id}, role={self.role.value}, Alive={self.is_alive})"

