from computaco.abstractions.project import Project
from computaco.agents.agent import Agent
from computaco.processes.process import Process


class SE(Process):

    project: Project

    def __init__(self, project: Project):
        self.project = project

    def brainstorm(self, client: Agent, expert: Agent):
        pass
