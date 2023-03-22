from dataclasses import dataclass
from computaco.abstractions.conversation import Message
from computaco.utils import english
from computaco.agents.agent import Agent
from computaco.organizations.organization import Organization


class Group(Agent):
    # Sometimes you want to fit groups of people into a single role.
    # Example: A group of representatives instead of just one client.
    # This is the only function of this class. Orgs are NOT Groups. Groups are Orgs.

    people: list[Agent]

    def __init__(self, people, name=None):
        self.people = people
        self.name = name or english.join([person.name for person in people])

    def chat(self, msg: Message, reply=True, remember=True, *args, **kwargs) -> str:
        raise NotImplementedError
