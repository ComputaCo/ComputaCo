# ./peer_review.py:

from pathlib import Path

import tensorcode as tc

from computaco.environments.conversation import Conversation, Message, TextMessage
from computaco.agents.agent import Agent


def peer_review(
    path: Path,
    topic: str,
    presenter: Agent,
    reviewers: list[Agent],
    rebuttals: int = 3,
):
    """
    Organizes a peer review session where one agent presents their work, and other agents provide feedback, critique, or suggestions for improvement.

    Args:
        presenter (Agent): The Agent object representing the presenter.
        reviewers (list[Agent]): A list of Agent objects representing the reviewers.
        rebuttals (int): The number of rebuttals the presenter has to address the feedback from reviewers.
    """

    agents = [presenter] + reviewers

    # Start a conversation with the agents
    with Conversation(
        path / "conversation",
        agents,
        initial_message=f"We will now peer review {presenter.name}'s work on {topic}.",
        final_message=f"Peer review of {presenter.name}'s work on {topic} completed.",
    ) as conversation:

        # Presenter shares their work
        presentation = presenter(f"Please present your work on {topic}.")
        conversation.input(presentation)

        # Reviewers provide feedback
        for reviewer in reviewers:
            feedback = reviewer(
                f"Please provide feedback on {presenter.name}'s presentation."
            )
            conversation.input(feedback)

        # Presenter responds to feedback with rebuttals
        presenter.input("Please respond to the feedback from the reviewers.")
        for _ in range(rebuttals):
            rebuttal = presenter.output()
            conversation.input(rebuttal)
