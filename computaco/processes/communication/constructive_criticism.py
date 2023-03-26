from pathlib import Path
from computaco.environments.conversation import Conversation, TextMessage
from computaco.agents.agent import Agent


def constructive_criticism(
    conversation: Conversation, work: str, agents: list[Agent]
) -> list[str]:
    conversation.input(f"Now let's provide constructive criticism for {work}")
    conversation.converse(len(agents))
    conversation.input("The constructive criticism session has ended.")
    return [message.content for message in conversation.messages[-len(agents) :]]
