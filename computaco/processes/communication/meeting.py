from pathlib import Path
from computaco.environments.conversation import Conversation, TextMessage
from computaco.agents.agent import Agent


def meeting(conversation: Conversation, agenda: list[str], agents: list[Agent]):
    conversation.input("The meeting has started.")
    for item in agenda:
        conversation.input(f"Agenda item: {item}")
        conversation.converse_until_done(f'Have we finished discussing "{item}"?', agents)
    conversation.input("The meeting has ended.")
