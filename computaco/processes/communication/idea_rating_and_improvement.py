from pathlib import Path
from computaco.environments.conversation import Conversation, TextMessage
from computaco.agents.agent import Agent


def idea_rating_and_improvement(
    conversation: Conversation, ideas: list[str], agents: list[Agent]
) -> list[tuple[str, str]]:
    conversation.input("Now let's rate and improve these ideas:")
    for idea in ideas:
        conversation.input(f"Idea: {idea}")
        conversation.input("Please rate and suggest improvements:")
        for agent in agents:
            conversation.input(agent.output())
    conversation.input("The rating and improvement session has ended.")
    return [
        (idea, message.content)
        for idea, message in zip(ideas, conversation.messages[-len(ideas) :])
    ]
