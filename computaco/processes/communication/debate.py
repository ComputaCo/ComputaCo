from pathlib import Path
from computaco.environments.conversation import Conversation, TextMessage
from computaco.agents.agent import Agent


def debate(
    conversation: Conversation,
    topic: str,
    agents_and_positions: list[tuple[Agent, str]],
    rounds: int,
):
    """
    Organizes a debate session where agents debate a topic, taking turns to state their position and respond to other agents' positions.
    """
    conversation.input(f"Now let's debate on the topic: {topic}")

    # Initialize debate
    for agent, position in agents_and_positions:
        agent.input(f"Your position on {topic} is: {position}")

    agents = [agent for agent, _ in agents_and_positions]

    for round in range(1, rounds + 1):
        conversation.input(f"Round {round} out of {rounds+1}")
        for agent, position in agents_and_positions:
            # Agent states their position
            conversation.input(agent.output())
            # Allow other agents to respond
            for responder in agents:
                if responder != agent:
                    conversation.input(responder.output())

    conversation.input(f"The debate on {topic} has ended")

    # Collect final thoughts from agents
    for agent, position in agents_and_positions:
        final_thought = agent(f"Please share your final thoughts on {topic}.")
        conversation.input(final_thought)
