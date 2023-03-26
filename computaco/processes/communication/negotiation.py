from pathlib import Path
from computaco.environments.conversation import Conversation, TextMessage
from computaco.agents.agent import Agent


def negotiation(conversation: Conversation, topic: str, agents: list[Agent], rounds: int):
    conversation.input(f"Now let's negotiate on the topic: {topic}")
    for round in range(1, rounds + 1):
        conversation.input(f"Round {round} out of {rounds}")
        for agent in agents:
            conversation.input(agent.output())
    conversation.input(f"The negotiation on {topic} has ended")
