from typing import Literal, Optional

import attr
from computaco.abstractions import abilities
from computaco.environments.conversation import (
    AudioMessage,
    Conversation,
    ImageMessage,
    Message,
    TextMessage,
    VideoMessage,
)
from computaco.abstractions.types import Audio, Image, Text, Video

## I'm just writing here beause I don't know where else, but the agent should have an agenda in its mind. That way, it won't continually say 'yes' to should we continue the conversation (because it'll want to do other tasks instead)


class Agent(abilities.HandlesAnyInputOutput):
    name: str = attr.ib()
    pronoun: str = attr.ib(default='he')
    object_pronoun: str = attr.ib(default='him')
    possessive_pronoun: str = attr.ib(default='his')

    INPUT = str
    OUTPUT = str

    def input(self, input: INPUT, *args, remember=True, **kwargs):

    def output(self, *args, remember=True, **kwargs) -> OUTPUT:

    # Agents CAN support multitasking. Processes canNOT.
    def fork(self):
        pass

    def merge(self):
        pass

    def __repr__(self):
        return self.name
