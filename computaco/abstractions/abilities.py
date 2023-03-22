from typing import Protocol, runtime_checkable

from computaco.abstractions.conversation import Message
import ivy


@runtime_checkable
class CanChat(Protocol):
    def chat(self, msg: Message, *args, **kwargs) -> str:
        ...


@runtime_checkable
class CanSee(Protocol):
    def chat(self, img: ivy.Array, *args, **kwargs) -> str:
        ...
