from pathlib import Path
from computaco.processes.communication.goal_oriented_conversation import (
    goal_oriented_conversation,
)
from computaco.environments.conversation import Conversation, Message, TextMessage
from computaco.agents.agent import Agent


def brainstorm(
    conversation: Conversation,
    topic: str,
    agents: list[Agent],
):
    """
    This implementation creates a conversation with all the agents participating in the brainstorming session. Each agent generates an idea, and the conversation proceeds until all agents agree that they've finished brainstorming. The final list of ideas is then returned as output.
    """
    conversation.input(f"Now let's brainstorm on the topic: {topic}")
    conversation.converse_until_done(
        is_done_message="Have we finished brainstorming about {topic}?",
        evaluators=agents,
    )
    conversation.input("Please share your final ideas about {topic}.")
