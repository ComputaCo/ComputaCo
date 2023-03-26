from typing import Literal
import attr
from computaco.agents.agent import Agent
from computaco.tools.tool import Tool
from computaco.utils.python import merge_types


@attr.s
class CompositeTool(Tool):
    tools: list[Tool] = attr.ib(default=[])

    @property
    def T_INPUT(self):
        return {tool.name: tool.T_INPUT for tool in self.tools}

    @property
    def T_OUTPUT(self):
        return {tool.name: tool.T_OUTPUT for tool in self.tools}

    def _fn(self, agent: Agent, input: T_INPUT) -> T_OUTPUT:
        output = {}
        for tool_name, tool_input in input.items():
            tool = next((tool for tool in self.tools if tool.name == tool_name), None)
            if tool:
                tool_output = tool(agent, tool_input)
                output[tool_name] = tool_output
        return output

    def get_tool(self, tool_name):
        for tool in self.tools:
            if tool.name == tool_name:
                return tool
        else:
            raise ValueError(f"`{tool}` not a valid option. Is your spelling correct?")
