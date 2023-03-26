# ./presentation.py:
from pathlib import Path
import tensorcode as tc

from computaco.environments.conversation import Conversation, Message, TextMessage
from computaco.agents.agent import Agent


def presentation(
    path: Path,
    topic: str,
    presenter: Agent,
    audience: list[Agent],
) -> list[Message]:
    """
    Allows the presenter agent to give a presentation on a topic.
    The audience can ask questions or provide feedback after the presentation.
    """

    # Start a conversation with the presenter and the audience
    with Conversation(
        path / "conversation",
        [presenter] + audience,
        initial_message=f"We will now listen to {presenter.name} present on the topic: {topic}.",
        final_message=f"Thank you for attending the presentation.",
    ) as conversation:
        # Input the initial instruction into the conversation
        conversation.input(presenter(f"Please give a presentation on the topic: {topic}"))

        # The presenter presents the topic
        while not tc.decide(presenter("Is your presentation complete?", remember=False)):
            conversation.input(presenter.output())

        # The audience asks questions or provides feedback
        final_feedback_messages = []
        for agent in audience:
            feedback = agent(
                f"Please ask {presenter.name} questions or provide feedback on {topic}.",
            )
            final_feedback_messages.append(feedback)
            conversation.input(feedback)

    return final_feedback_messages
