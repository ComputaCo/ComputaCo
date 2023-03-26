from pathlib import Path
from computaco.environments.conversation import Conversation, TextMessage
from computaco.agents.agent import Agent


def topic_exploration(
    conversation: Conversation, topic: str, agents: list[Agent], rounds: int
):
    conversation.input(f"Now let's explore the topic: {topic}")
    for round in range(1, rounds + 1):
        conversation.input(f"Round {round} out of {rounds}")
        conversation.converse_until_done(
            f'Have we finished discussing "{topic}"?', agents
        )
    conversation.input(f"The topic exploration on {topic} has ended")
