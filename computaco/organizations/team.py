from computaco.abstractions.project import Project
from computaco.agents.agent import Agent
from computaco.organizations.organization import Organization


class Team(Organization):
    manager: Agent
    workers: list[Agent]
    projects: list[Project]
