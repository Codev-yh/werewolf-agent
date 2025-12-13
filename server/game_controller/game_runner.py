"""Contains game runner class.

Game runner is used to deal with main game logic. It uses the model classes
like `Game` and `Player` and interacts with `AgentServer` and `Recorder`.

When using, first create a GameRunner instance and then bind it to your
AgentServer and Recorder.
"""

import asyncio
from typing import TYPE_CHECKING, Optional

from game_logic.game import Game, GameState
from game_logic.game_config import GameConfig
from recorder.recorder import Recorder

if TYPE_CHECKING:
    from agent_server.agent_server import AgentServer


class GameRunner:
    """The game runner class, which controls the game progress.

    Attributes:
        config: The game config used to initialize a game.
    """

    def __init__(self, config: GameConfig):
        self.config = config
        self._game: Optional[Game] = None
        self._agent_server: Optional["AgentServer"] = None
        self._recorder: Optional[Recorder] = None

        self._task: Optional[asyncio.Task[None]] = None

        # players that are already connected, different from config.player_number
        self.player_count = 0

    async def start(self) -> None:
        """Start the game.

        Start a game when it's not running. If the game is already started,
        then raise. This coroutine should be awaited, and it will finish
        immediately, leaving a running game task.
        """
        raise NotImplementedError

    def bind_server(self, server: "AgentServer") -> None:
        """Bind the GameRunner into a AgentServer.

        If the bound already exists, then pass. If already bound with
        different agent server, then raise. Otherwise, build the binding
        relationship.
        """
        raise NotImplementedError

    def bind_recorder(self, recorder: Recorder) -> None:
        """Bind the GameRunner into a Recorder.

        If the bound already exists, then pass. If already bound with
        different recorder, then raise. Otherwise, build the binding
        relationship.
        """
        raise NotImplementedError

    async def on_message(self) -> None:
        """Deal with the message from AgentServer"""
        raise NotImplementedError

    async def _run_game(self) -> None:
        """Run the game. Main game logic will be dealt in this method."""
        raise NotImplementedError

    @property
    def is_running(self) -> bool:
        """If the game is running"""
        return (
            self._game is not None
            and self._game.state is not GameState.NOT_STARTED
        )

    @property
    def is_bound_with_server(self) -> bool:
        """If it is bound with an agent server"""
        return self._agent_server is not None

    @property
    def is_bound_with_recorder(self) -> bool:
        """If it is bound with a recorder"""
        return self._recorder is not None

    @property
    def is_end(self) -> bool:
        """If the game is already ended."""
        return self._game is not None and self._game.state is GameState.FINISHED

    @property
    def player_ready(self) -> bool:
        """If number of connected players is enough"""
        return self.player_count == self.config.player_number
