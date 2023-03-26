from pathlib import Path
from computaco.processes.communication.goal_oriented_conversation import (
    goal_oriented_conversation,
)
from computaco.environments.conversation import Conversation, Message, TextMessage
from computaco.agents.agent import Agent


def consensus_building(
    conversation: Conversation,
    topic: str,
    agents: list[Agent],
) -> list[Message]:
    """
    This implementation creates a conversation with all the agents participating in the consensus building session. Each agent shares their opinion, and the conversation proceeds until all agents agree that they've reached a consensus. The final list of opinions is then returned as output.
    """
    conversation.input(f"Now let's build a consensus on the topic: {topic}")
    conversation.converse_until_done(
        is_done_message="Have we reached a consensus on {topic}?",
        evaluators=agents,
    )
    messages_before_conclusion = len(conversation.messages)
    conversation.input(f"Please share your final thoughts about {topic}.")
    messages_after_conclusion = len(conversation.messages)
    return conversation.messages[messages_before_conclusion:messages_after_conclusion]
