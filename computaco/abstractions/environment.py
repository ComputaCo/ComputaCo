from logging import Logger
from pathlib import Path

import attr
from computaco.agents.agent import Agent
from computaco.tools.tool import Tool
from computaco.utils.logging import make_logger


class Environment:

    path: Path = attr.ib()
    tools: list[Tool] = attr.ib()
    agents: list[Agent] = attr.ib()
    _logger: Logger

    def __init__(self, path, tools=[], agents=[]):
        self._logger = make_logger(__name__, self.path / "log")

    def input_tool_output(
        self, tool: Tool, output: any, sender: Agent, recievers: list[Agent] = None
    ):
        for reciever in recievers or self.env.agents:
            reciever.input(output, sender=sender)
