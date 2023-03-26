from pathlib import Path
from computaco.agents.agent import Agent
from computaco.environments.conversation import Conversation, Message


class AgendaItem:

    description: str
    initial_rounds: int = 2
    evaluation_criteria: list[tuple[Agent, str]]


def 



class Meeting(Conversation):

    agenda: list[AgendaItem]

    def __init__(
        self,
        agenda: list[AgendaItem],
        path: Path,
        speakers: list[Agent] = [],
        bystanders: list[Agent] = [],
        initial_message: str | Message = None,
        final_message: str | Message = None,
    ):
        super().__init__(path, speakers, bystanders, initial_message, final_message)
        self.agenda = agenda
