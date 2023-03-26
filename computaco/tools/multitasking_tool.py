from __future__ import annotations
import functools
from typing import Callable

import attr
from computaco.tools.composite_tool import CompositeTool
from computaco.tools.tool import Tool
from computaco.tools.python_function_toolbox import PythonFunctionToolbox
from computaco.tools.terminal import Terminal
from computaco.tools.text_editor import TextEditor


@attr.s
class MultitaskingTool(CompositeTool):
    class MultitaskingToolController(PythonFunctionToolbox):
        multitasking_tool: MultitaskingTool = attr.ib()

        @property
        def fns(self):
            fns = []

            # tool creators
            if self.multitasking_tool.agent_can_create_tools:
                for tool_creator in self.multitasking_tool.tool_creators.items():

                    @functools.wraps(tool_creator)
                    def create(*args, **kwargs):
                        self.multitasking_tool.new_tool(tool_creator(*args, **kwargs))

                    create.__name__ = tool_creator.__name__
                    fns.append(create)

            # core functionality
            def switch_tool(tool: str):
                self.multitasking_tool.active_tool = self.multitasking_tool.get_tool(tool)

            fns.append(switch_tool)

            # tool closer
            if self.multitasking_tool.agent_can_remove_tools:

                def close(tool: str):
                    self.multitasking_tool.tools.remove(
                        self.multitasking_tool.get_tool(tool)
                    )

                fns.append(close)
            return fns

    active_tool: Tool = attr.ib(default=None)
    agent_can_remove_tools = True
    agent_can_create_tools = True
    tool_creators = list[Callable[..., Tool]] = attr.ib(default=[])

    _controller: MultitaskingTool.MultitaskingController = None

    @property
    def tools(self):
        if self._controller is None:
            self._controller = MultitaskingTool.MultitaskingController(self)
        return [self._controller, self.active_tool]
