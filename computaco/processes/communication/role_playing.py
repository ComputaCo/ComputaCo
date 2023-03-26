from pathlib import Path
from computaco.environments.conversation import Conversation, TextMessage
from computaco.agents.agent import Agent


def role_playing(
    conversation: Conversation,
    scenario: str,
    roles_and_agents: list[tuple[str, Agent]],
    rounds: int,
):
    conversation.input(f"Now let's role-play the following scenario: {scenario}")
    for role, agent in roles_and_agents:
        agent.input(f"Your role in the scenario is: {role}")
    conversation.converse(rounds)
    conversation.input("The role-playing session has ended")
