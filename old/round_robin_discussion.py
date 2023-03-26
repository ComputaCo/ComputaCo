# ./round_robin_discussion.py:

from pathlib import Path
from computaco.environments.conversation import Conversation, Message, TextMessage
from computaco.agents.agent import Agent
import tensorcode as tc


def round_robin_discussion(
    path: Path,
    topic: str,
    agents: list[Agent],
    rounds: int,
):
    """
    Organizes a round-robin-style discussion between agents, where each agent takes turns to contribute to a topic, building upon the ideas of the previous agent.
    This can be useful for collaborative brainstorming and ensuring all agents have an opportunity to share their thoughts.
    """

    # Start a conversation with the agents
    with Conversation(
        path / "conversation",
        agents,
        initial_message=f"Let's discuss the topic: {topic}",
        final_message=f"Discussion of {topic} completed.",
    ) as conversation:
        for round in range(rounds):
            conversation.step()

            # Check if the agents agree to end the discussion
            for agent in agents:
                if not tc.decide(
                    agent("Do you want to stay in the conversation?", remember=False)
                ):
                    break  # break inner loop if an agent does not want to end the discussion
            else:
                break  # break outer loop once all agents agree to end the discussion
