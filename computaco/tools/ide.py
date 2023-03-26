from pathlib import Path

import attr
from computaco.tools.multitasking_tool import MultitaskingTool
from computaco.tools.terminal import Terminal
from computaco.tools.text_editor import TextEditor


@attr.s
class IDE(MultitaskingTool):

    path: Path

    def __init__(self, path):
        self.path = Path(path)
        self.terminals = []
        self.text_editors = []

        def new_terminal():
            terminal = Terminal(
                "bash", env=self.env, name=f"Terminal_{len(self.terminals)}"
            )
            self.terminals.append(terminal)
            return terminal

        def new(path):
            text_editor = TextEditor(env=self.env, path=path)
            self.text_editors.append(text_editor)
            return text_editor

        def open(path):
            return new(path)

        super().__init__(tool_creators=[new_terminal, new, open])

    @property
    def terminals(self) -> list[Terminal]:
        return list(filter(lambda t: isinstance(t, Terminal), self.tools))

    @property
    def text_editors(self) -> list[TextEditor]:
        return list(filter(lambda t: isinstance(t, TextEditor), self.tools))
