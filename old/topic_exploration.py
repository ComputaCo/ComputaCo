# ./topic_exploration.py:

from pathlib import Path
from computaco.utils import english
from computaco.environments.conversation import Conversation, Message, TextMessage
from computaco.agents.agent import Agent
import tensorcode as tc


def topic_exploration(
    path: Path,
    topic: str,
    subtopics: list[str],
    agents: list[Agent],
):
    """
    Organizes a topic exploration session where agents discuss a topic, diving deeper into subtopics.
    """

    # Start a conversation with the agents
    with Conversation(
        path / "conversation",
        agents,
        initial_message=f"Let's explore the topic: {topic}. We will dive into {len(subtopics)} subtopics: {english.join(subtopics)}.",
        final_message=f"Topic exploration of {topic} completed.",
    ) as conversation:

        # Topic exploration phase
        for i, subtopic in enumerate(subtopics):
            if i == 0:
                conversation.input(f"We'll start with subtopic {i+1}: {subtopic}.")
            else:
                conversation.input(f"Now let's dive into subtopic {i+1}: {subtopic}.")
            conversation.step()
