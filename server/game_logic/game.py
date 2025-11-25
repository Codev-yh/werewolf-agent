"""Contains Game Class"""

from enum import Enum, auto
from typing import List, Optional

from game_logic.player import Player, Character
from game_logic.result import GameResult
from game_logic.game_config import GameConfig


class GameState(Enum):
    """
    Represent the state of the game.
    """

    NOT_STARTED = auto()
    EVENING = auto()
    MORNING = auto()
    FINISHED = auto()


class Game:
    """The game state class"""

    def __init__(self, config: GameConfig):
        self._state = GameState.NOT_STARTED
        # the player list. the the player with ID `i` is _player[i - 1] since in
        # werewolf game, the index begin at 1.
        self._players: List[Player] = []
        self._config = config

    def start(self) -> None:
        """
        Start the game. Only useful when the state is `NOT_STARTED`.

        After started, the state will be `EVENING`.
        """
        # Assign the character, shuffle the id of the players
        # If the player needs any initialization operations, do it.
        raise NotImplementedError

    def _sun_rise(self) -> None:
        """Going from night to morning."""
        # change _state
        raise NotImplementedError

    def _sun_set(self) -> None:
        """Going from morning to evening."""
        # change _state
        raise NotImplementedError

    def is_end(self) -> bool:
        """
        Checks if the game is already end.

        Returns:
        bool: if the game is end.
        """
        # according to the alive players' characters, judge if the game is over
        raise NotImplementedError

    def is_character_alive(self, character: Character) -> bool:
        """
        Checks if the given character has at least one player alive

        Args:
            character(Character): the character to be checked

        Returns:
        bool: if the given character has someone(>0) alive
        """
        # ... just find the character
        raise NotImplementedError

    def get_result(self) -> Optional[GameResult]:
        """
        Get the game result if the game is end

        Returns:
        Optional[GameResult]: the game result if game is end, else you'll get None.
        """
        # according to the alive players' characters, judge the game result
        raise NotImplementedError

    def state_switch(self) -> None:
        """
        Maintaining the state machine for `self`, should be called when:
        - Switching from day to night
        - Switching from night to day

        Only this method can change the state into `end`.
        """
        # Not Started --> Evening: do exactly the same thing as Start()
        # Evening --> End: If the game ends after werewolf killing
        # Morning --> End: If the game ends after voting
        # Evening <--> Morning: If the game not end.

        # Actually, you can modify the player's alive state only when state changes
        raise NotImplementedError

    def process_morning_voting_result(self, voting_result: List[int]) -> None:
        """
        Process the voting result.

        Args:
            voting_result (List[int]): the list of voted players' ID
        """
        # Find max, then execute
        # If multiple max exists, then return a success flag
        # You may want to change the returning type
        raise NotImplementedError

    def process_werewolf_voting_result(self, voting_result: List[int]) -> None:
        """
        Process the voting result in the night, when werewolves is killing.

        Args:
            voting_result (List[int]): the list of voted players' ID
        """
        # Exact same as above
        raise NotImplementedError

    def process_witch_saving(self, saved_player: int) -> None:
        """
        Process the witch saving player.

        Args:
            saved_player(int): the saved player's ID
        """
        # witch saving people
        # you may want to add protected variable in the class
        raise NotImplementedError

    def process_guard_saving(self, saved_player: int) -> None:
        """
        Process the guard saving player.

        Args:
            saved_player(int): the saved player's ID
        """
        # ...same
        raise NotImplementedError

    def process_witch_killing(self, killed_player: int) -> None:
        """
        Process the witch killing player.

        Args:
            killed_player(int): the killed player's ID
        """
        # ...same
        raise NotImplementedError

    def process_hunter_killing(self, killed_player: int) -> None:
        """
        Process the hunter killing player.

        Args:
            killed_player(int): the killed player's ID
        """
        # ...same
        raise NotImplementedError

    def get_player_character(self, player_id: int) -> Character:
        """
        Get the character of a player

        Args:
            player_id(int): the player's ID

        Returns:
        Character: The character of the player
        """
        # trivial
        raise NotImplementedError
