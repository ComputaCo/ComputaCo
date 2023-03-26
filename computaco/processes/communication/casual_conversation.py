from pathlib import Path
from computaco.environments.conversation import Conversation, Message, TextMessage
from computaco.utils import english
from computaco.agents.agent import Agent


def casual_conversation(conversation: Conversation, rounds=100):
    """
    Starts an endless conversation with the agents.
    """
    conversation.input(
        f"{english.join(conversation.participants)} are having a casual conversation."
    )
    conversation.converse(rounds=rounds)
    conversation.input("The conversation has ended.")
