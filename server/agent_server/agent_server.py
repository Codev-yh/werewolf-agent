"""Contains the Agent Server Class

AgentServer is used to deal with connections from player's code. Its role
includes:
- Deal with connections from agent. Provide functions like connecting,
reconnecting, disconnecting, etc.
- Parse the messages according to the protocol. Then send necessary message
to GameRunner.
- Afford a sending message interface to GameRunner.
- ...
"""

from typing import TYPE_CHECKING, Tuple

if TYPE_CHECKING:
    from game_controller.game_runner import GameRunner


# pylint: disable=too-few-public-methods
# ^ TODO: remove it after the class finished
class AgentServer:
    """The Agent Server"""

    def __init__(self, host_port: Tuple[str, int]) -> None:
        pass

    async def start(self) -> None:
        """Start the agent server.

        Start agent server when it's not running. If the server is already
        started, then raise. This coroutine should be awaited, and it will
        finish immediately, leaving a serving .
        """
        raise NotImplementedError

    def bind_runner(self, runner: "GameRunner") -> None:
        """Bind the AgentServer into a GameRunner.

        If the bound already exists, then pass. If already bound with
        different runner, then raise.
        """
        raise NotImplementedError
