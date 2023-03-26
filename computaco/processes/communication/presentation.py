from pathlib import Path
from computaco.environments.conversation import Conversation, TextMessage
from computaco.agents.agent import Agent


def presentation(
    conversation: Conversation, topic: str, presenter: Agent, audience: list[Agent]
):
    conversation.input(f"Now {presenter.name} will present on the topic: {topic}")
    conversation.input(presenter.output())
    conversation.input(
        f"{presenter.name} has finished presenting on the topic: {topic}. Now it is time for questions."
    )
    for agent in audience:
        conversation.input(agent.output())
        conversation.input(presenter.output())
    conversation.input("Thank you for attending. The presentation has ended.")
