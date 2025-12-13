"""Entry Point for Server"""

from agent_server.agent_server import AgentServer
from game_controller.game_runner import GameRunner
from game_logic.game_config import NORMAL_CONFIG_6_PLAYER
from recorder.recorder import Recorder


async def main():
    # TODO: read configuration file or env to get the following message:
    # host and port
    # rule, number of players, and the numbers of each role (or use normal)
    # list of trusted tokens

    host = "0.0.0.0"
    port = 1999

    game_runner = GameRunner(NORMAL_CONFIG_6_PLAYER)
    agent_server = AgentServer((host, port))
    recorder = Recorder()

    game_runner.bind_server(agent_server)
    game_runner.bind_recorder(recorder)
    agent_server.bind_runner(game_runner)
    # recorder.bind_runner(game_runner)
    # ^ TODO: finish the method definition

    # Stage I: wait for connection
    while True:
        raise NotImplementedError

    # Stage II: run the game
    while True:
        raise NotImplementedError

    # Game finished, close the server, and save the recording.


if __name__ == "__main__":
    print("Hello World!")
