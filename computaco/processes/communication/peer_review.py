from pathlib import Path
from computaco.environments.conversation import Conversation, TextMessage
from computaco.agents.agent import Agent


def peer_review(
    conversation: Conversation,
    work: str,
    author: Agent,
    reviewers: list[Agent],
    rounds: int = 3,
):
    conversation.input(f"Now let's conduct a peer review for the following work: {work}")

    # Author presents their work
    conversation.input(
        f"{author.name} will first present {author.possessive_pronoun} work: {work}"
    )
    conversation.input(author("Please present your work."))

    for round in range(1, rounds + 1):
        conversation.input(f"Round {round} out of {rounds}")

        # Reviewers review the work
        conversation.input(f"The reviewers will now provide their feedback on {work}")
        for reviewer in reviewers:
            conversation.input(reviewer(f"Please provide feedback"))
            conversation.input(author(f"Please address {reviewer.name}'s feedback"))

    conversation.input("The peer review session has ended.")
