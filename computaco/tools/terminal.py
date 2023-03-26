from pathlib import Path
import select
import subprocess
from dataclasses import dataclass

import attr

from computaco.abstractions.environment import Environment
from computaco.agents.agent import Agent
from computaco.tools.buffered_tool import BufferedTool
from computaco.tools.tool import Tool


@attr.s
class Terminal(BufferedTool):
    _process: subprocess.Popen = None

    def __init__(
        self,
        proc_invocation: str,
        path: str | Path,
        env: Environment,
        name: str,
        description: str,
        examples: list[tuple[BufferedTool.T_INPUT, BufferedTool.T_OUTPUT]] = [],
    ):
        super().__init__(env, name, description, examples)
        self._process = subprocess.Popen(
            proc_invocation,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
            shell=True,
            bufsize=0,
            text=True,
            cwd=str(path),
        )

    def _fn(self, agent: Agent, input: BufferedTool.T_INPUT) -> BufferedTool.T_OUTPUT:

        self.insert(input.text_input)

        output = ""
        while True:
            rlist, _, _ = select.select(
                [self._process.stdout, self._process.stderr], [], [], 0.1
            )
            if rlist:
                for r in rlist:
                    line = r.readline()
                    if line:
                        output += line
                        self._buffer.append(line.rstrip("\n"))
            else:
                break

        self.move_cursor(input.scroll)
        window = self.window
        return BufferedTool.T_OUTPUT(output, window)

    def insert(self, text: str):
        self._process.stdin.write(text + "\n")
        self._process.stdin.flush()
