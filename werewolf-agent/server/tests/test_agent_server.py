"""Tests for AgentServer."""

from agent_server.agent_server import AgentServer


class TestAgentServer:
    """Test cases for AgentServer."""

    def test_initialization(self):
        """Test server initialization."""
        server = AgentServer()
        assert isinstance(server, AgentServer)

    async def test_start(self):
        """Test server start."""
        server = AgentServer()
        await server.start()
