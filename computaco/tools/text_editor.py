from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import threading
import os

import attr
from computaco.agents.agent import Agent
from computaco.tools.buffered_tool import BufferedTool
from computaco.tools.tool import Tool


@attr.s
class TextEditor(BufferedTool):
    path: Path = attr.ib()
    _changes: str = attr.ib(default="")
    _lock = attr.ib(default=threading.Lock())

    def _fn(self, agent: Agent, input: BufferedTool.T_INPUT) -> BufferedTool.T_OUTPUT:
        with self._lock:
            self.insert(input.text_input)
            self.move_cursor(input.scroll)
            output, self._changes = self._changes, ""
            window = self.window
            return BufferedTool.T_OUTPUT(output, window)

    @property
    def name(self):
        return self.path.name

    @property
    def description(self):
        return f"A text editor for {self.name}"

    def insert(self, text: str):
        row, col = self.cursor_pos
        self._buffer[row] = self._buffer[row][:col] + text + self._buffer[row][col:]
        self.cursor_pos = (row, col + len(text))
        self._changes += text
        self.save_changes_to_file()

    def load_buffer(self):
        with self.path.open("r") as file:
            lines = file.readlines()
        self._buffer = [line.rstrip("\n") for line in lines]

    def save_changes_to_file(self):
        with self.path.open("w") as file:
            for line in self._buffer:
                file.write(line + "\n")
