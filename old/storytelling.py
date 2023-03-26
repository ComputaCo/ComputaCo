# ./storytelling.py:

from pathlib import Path
from computaco.environments.conversation import Conversation, Message, TextMessage
from computaco.agents.agent import Agent
import tensorcode as tc


def storytelling(path: Path, topic: str, storyteller: Agent, audience: list[Agent]):
    """
    Facilitates storytelling between agents, where each agent contributes to the development of a narrative.
    This can be useful for creative writing, idea generation, or building shared understanding through stories.
    """

    # Start a conversation with the agents
    with Conversation(
        path / "conversation",
        [storyteller] + audience,
        initial_message=f"{storyteller.name} will now tell a story about {topic}.",
        final_message=f"Storytime is over. Thank you for listening to {storyteller.name}.",
    ) as conversation:
        while True:
            storyteller("Please continue the story.")
            conversation.input(storyteller.output())

            if tc.decide(storyteller("Is that the end?", remember=False)):
                break
