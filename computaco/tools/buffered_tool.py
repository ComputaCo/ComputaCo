from dataclasses import dataclass
from typing import List

import attr

from computaco.agents.agent import Agent
from computaco.tools.tool import Tool


@attr.s
class BufferedTool(Tool):

    only_textio: bool = attr.ib(default=False)

    @dataclass
    class _T_INPUT_COMPLEX:
        text_input: str
        scroll: tuple[int, int] = (0, 0)

    @dataclass
    class _T_OUTPUT_COMPLEX:
        new_output: str
        window: List[str]

    @property
    def T_INPUT(self):
        if self.only_textio:
            return str
        else:
            return self._T_INPUT_COMPLEX

    @property
    def T_OUTPUT(self):
        if self.only_textio:
            return str
        else:
            return self._T_OUTPUT_COMPLEX

    cursor_pos: tuple[int, int] = (0, 0)
    window_size: tuple[int, int] = (0, 0)
    _buffer: List[str] = []

    def insert(self, text: str):
        raise NotImplementedError()

    @property
    def window(self) -> List[str]:
        start_row = self.cursor_pos[0]
        end_row = start_row + self.window_size[0]
        start_col = self.cursor_pos[1]
        end_col = start_col + self.window_size[1]

        visible_rows = self._buffer[start_row:end_row]

        window_content = []
        for row in visible_rows:
            if len(row) > end_col:
                row = row[:end_col]
            if len(row) > start_col:
                row = row[start_col:]
            window_content.append(row)

        return window_content

    def move_cursor(self, scroll: tuple[int, int]):
        self.cursor_pos = (
            self.cursor_pos[0] + scroll[0],
            self.cursor_pos[1] + scroll[1],
        )
