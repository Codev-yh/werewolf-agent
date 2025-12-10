from enum import Enum
from typing import Any

class Role(Enum):
    """The character enum"""

    VILLAGER = "villager"
    WITCH = "witch"
    HUNTER = "hunter"
    WEREWOLF = "werewolf"
    PROPHET = "prophet"
    GUARD = "guard"


class Player:
    """Represents a player in the game with their role and state."""
    def __init__(self, player_id: int, role: Role):
        self.id : int = player_id
        self.role : Role = role
        self.is_alive : bool = True

        self.witch_antidote : bool = True
        self.witch_poison : bool = True
        self.can_shoot : bool = True

        self.prophet_check_history: list[dict[str, Any]] = []

        self.survived_nights : int = 0 # 玩家存活的夜晚数
        self.vote_correct_counts : int = 0 # 玩家投票正确的次数
        self.mistake_counts : int = 0

    # TODO: add enum for death reason
    def die(self, method: str) -> None :
        """
        Set the player's state to death
        """
        self.is_alive = False
        if self.role == Role.HUNTER and method == "poison":    
            self.can_shoot = False

    # 显示玩家信息
    def __repr__(self) -> str:
        return f"Player(id={self.id}, role={self.role.value}, Alive={self.is_alive})"
