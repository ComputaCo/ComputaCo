from computaco.abstractions.conversation import Conversation, Message
from computaco.agents.agent import Agent
from computils.engines.base import CompletionEngine, ConversationEngine

from computaco.utils import registry


class ConversationAgent(Agent):

    engine: ConversationEngine | CompletionEngine
    _messages: Conversation

    DEFAULT_ENGINE = registry.small_chat_engine
    DEFAULT_SYSTEM_PROMPT = "You are {name}."

    def __init__(self, name, initial_message=None, engine=None):
        super().__init__(name=name)
        self._messages = Conversation(
            Message(
                initial_message or self.DEFAULT_SYSTEM_PROMPT.format(name=name),
                "system",
            )
        )
        self.engine = engine or self.DEFAULT_ENGINE

    def chat(self, msg: Message, reply=True, remember=True, *args, **kwargs) -> str:
        messages = self.messages.copy()
        messages.append(msg)
        if isinstance(self.engine, ConversationEngine):
            response = self.engine.chat(messages.to_json(), **kwargs)
        elif isinstance(self.engine, CompletionEngine):
            response = self.engine.complete(messages.to_string(), **kwargs)
        messages.append(Message(response, self.name))
        if remember:
            self.messages = messages
        return response
