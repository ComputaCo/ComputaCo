# python 3.10

# computaco/agents/agent.py

from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
import subprocess
from typing import TypeVar

import numpy as np

from computaco.abstractions.environment import Environment


class Agent:
    name: str
    description: str
    tools: list[Tool]

    def input(self, input: any, sender: Agent):
        raise NotImplementedError()

    def output(self) -> any:
        raise NotImplementedError()

    def __call__(self, input: any, sender: Agent) -> any:
        self.input(input, sender)
        return self.output()


SYSTEM = Agent("System", "The system", [])


# computaco/environment.py

from logging import Logger
from pathlib import Path

import attr
from computaco.tools.tool import Tool
from computaco.utils.logging import make_logger


# computaco/tools/tool.py
import attr


@attr.s
class Tool:

    env: Environment = attr.ib()
    T_INPUT: type = str
    T_OUTPUT: type = str

    # these attrs should be set by the subclass
    name: str = attr.ib()
    description: str = attr.ib()

    examples: list[tuple[T_INPUT, T_OUTPUT]] = attr.ib(default=[])  # (input, output)

    __all_users = attr.ib(init=False, default=set())

    def __call__(self, agent: Agent, input):
        self.__all_users.add(agent)
        output = self._fn(agent, input)
        self.env.input_tool_output(self, output, sender=agent, recievers=self.__all_users)

    def _fn(self, agent: Agent, input: T_INPUT) -> T_OUTPUT:
        raise NotImplementedError()
