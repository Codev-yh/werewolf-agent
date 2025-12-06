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


class Player:
    """Represents a player in the game with their role and state."""
    def __init__(self, player_id: int, role: Role):
        self.id : int = player_id
        self.role : Role = role
        self.is_alive : bool = True

        # Witch antidote; True means available
        self.witch_antidote : bool = True  
        # Witch poison; True means available
        self.witch_poison : bool = True    

        # Hunter can shoot; True means can shoot
        self.can_shoot : bool = True  

        # Prophet check history: contains checked player IDs and roles
        self.prophet_check_history: list[dict[str, Any]] = []

        # Number of nights the player has survived
        self.survived_nights : int = 0  
        # Number of times the player voted correctly
        self.vote_correct_counts : int = 0 
        # Number of mistakes made (e.g., poisoning a villager)
        self.mistake_counts : int = 0 


    def die(self, method: str) -> None :
        """Set the player's state to dead and mark consequences"""
        self.is_alive = False
        # If the hunter was poisoned, they cannot shoot.
        if self.role.is_hunter and method == "poison":    
            self.can_shoot = False

    def __repr__(self) -> str:
        """Return a string representation of the player."""
        return f"Player(id={self.id}, role={self.role.value}, Alive={self.is_alive})"

