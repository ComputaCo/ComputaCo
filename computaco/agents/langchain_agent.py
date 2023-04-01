from computaco.agents.agent import Agent
from computils.engines.base import CompletionEngine, ConversationEngine

from computaco.utils import registry
import langchain.agents


class LangChainAgent(Agent):

    engine: ConversationEngine | CompletionEngine
    _agent: langchain.Agent

    DEFAULT_ENGINE = registry.small_chat_engine
    DEFAULT_SYSTEM_PROMPT = "You are {name}."

    def __init__(self, name, initial_message=None, engine=None):
        super().__init__(name=name)

    def talk(self, remember=True, **kwargs) -> str:
        raise NotImplementedError

    def tell(self, text, *args, sender="Info", remember=True, **kwargs):
        raise NotImplementedError
