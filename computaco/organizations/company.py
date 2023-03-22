from computaco.agents.agent import Agent
from computaco.organizations.organization import Organization
from computaco.organizations.team import Team


class Company(Organization):

    owners: list[Agent]
    executives: list[Agent]
    managers: list[Agent]
    employees: list[Agent]
    teams: list[Team]
