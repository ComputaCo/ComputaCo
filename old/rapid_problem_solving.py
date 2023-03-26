# ./rapid_problem_solving.py:

from pathlib import Path
from computaco.environments.conversation import Conversation, Message, TextMessage
from computaco.agents.agent import Agent
import tensorcode as tc


def rapid_problem_solving(
    path: Path,
    problem: str,
    agents: list[Agent],
    rounds: int = 5,
):
    """
    Organizes a rapid problem-solving session where agents attempt to solve a problem within a given time limit.
    """

    # Start a conversation with the agents
    with Conversation(
        path / "conversation",
        agents,
        initial_message=f"Let's solve the problem: {problem}. You have {rounds} rounds to find a solution.",
    ) as conversation:

        # Rapid problem-solving phase
        for round in range(rounds):
            if round > 0:
                conversation.input(f"{rounds-round} rounds remaining.")

            for agent in agents:
                solution_attempt = agent.output()
                conversation.input(solution_attempt)

                if tc.decide(agent("Did you find a solution?", remember=False)):
                    conversation.input("The problem has been solved.")
                    return solution_attempt

        conversation.input(
            "Time's up! The problem could not be solved within the given time limit."
        )
