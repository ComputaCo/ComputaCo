import attr
import langchain.tools

from computaco.tools.tool import Agent, Tool


class LangchainTool(Tool):

    langchain_tool: langchain.tools.BaseTool = attr.ib()

    T_INPUT: type = str
    T_OUTPUT: type = str

    def _fn(self, agent: Agent, input: T_INPUT) -> T_OUTPUT:
        return self.langchain_tool.run(tool_input=input)

    @property
    def name(self):
        return self.langchain_tool.name

    @property
    def description(self):
        return self.langchain_tool.description
