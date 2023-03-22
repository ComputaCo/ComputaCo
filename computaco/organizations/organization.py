from computaco.agents.agent import Agent
from computaco.agents.group import Group
from computaco.organizations.team import Team


class Organization(Group):
    # A Group is ephemeral. An Organization is permanent.
    name: str
