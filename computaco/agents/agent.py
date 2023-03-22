from computaco.abstractions.abilities import CanChat
from computaco.abstractions.conversation import Message


class Agent(CanChat):
    name: str

    def chat(self, msg: Message, reply=True, remember=True, *args, **kwargs) -> str:
        ...

    # Agents CAN support multithreading. Processes canNOT.
    def fork(self):
        pass

    def merge(self):
        pass
