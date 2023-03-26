# ./negotiation.py:

from pathlib import Path
from computaco.environments.conversation import Conversation, Message, TextMessage
from computaco.agents.agent import Agent
import tensorcode as tc


def negotiation(
    path: Path,
    agents_and_goals: list[tuple[Agent, str]],
) -> list[Message]:
    """
    Simulates negotiation between agents, where each agent has its own interests, preferences, or objectives.
    The goal would be to reach a mutually beneficial agreement or compromise.
    """
    agents = [agent for agent, _ in agents_and_goals]

    # Start a conversation with the agents
    with Conversation(
        path / "conversation",
        agents,
        initial_message="Let's negotiate!",
        final_message="The negotiation is complete.",
    ) as conversation:

        # Assign the negotiation goals to each agent
        for agent, goal in agents_and_goals:
            agent.input(f"Your negotiation goal is: {goal}")

        while True:
            conversation.step()

            # Check if each agent agrees the negotiation is complete
            for agent in agents:
                if not tc.decide(
                    agent("Are you satisfied with the current agreement?", remember=False)
                ):
                    break  # break inner loop if an agent does not think the negotiation is complete
            else:
                break  # break outer loop once all agents agree the negotiation is complete

    # Collect the final agreements or compromises from each agent
    final_agreements = []
    for agent in agents:
        final_agreement = agent("Please share your final agreement or compromise.")
        final_agreements.append(final_agreement)
        conversation.input(final_agreement)

    return final_agreements
