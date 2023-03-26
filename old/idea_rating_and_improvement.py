# ./idea_rating_and_improvement.py:

from pathlib import Path
from computaco.environments.conversation import Conversation, Message, TextMessage
from computaco.agents.agent import Agent
import tensorcode as tc


def idea_rating_and_improvement(
    path: Path,
    topic: str,
    agents: list[Agent],
    iterations: int = 2,
    generation_rounds_per_iteration: int = 1,
):
    """
    Organizes a discussion where agents generate ideas, rate them, and suggest improvements.
    """

    # Start a conversation with the agents
    with Conversation(
        path / "conversation",
        agents,
        initial_message=f"Let's generate ideas for {topic}.",
        final_message=f"We're done generating ideas for {topic}.",
    ) as conversation:
        for iteration in range(iterations):
            # Idea generation phase
            agents_and_ideas = []
            conversation.input(
                "Let's start generating ideas."
                if iteration == 0
                else "Let's go back to the generation stage."
            )
            for _ in range(generation_rounds_per_iteration):
                for agent in agents:
                    idea = agent.output()
                    conversation.input(idea)
                    agents_and_ideas.append((agent, idea))

            for agent, idea in agents_and_ideas:

                # Idea rating phase
                conversation.input(
                    f"Please rate {agent.name}'s idea:\n{idea} (terrible, bad, okay, good, great)"
                )
                for _agent in agents:
                    if agent is _agent:
                        continue
                    conversation.input(_agent.output())

                # Idea improvement phase
                conversation.input(f"Let's discuss how to improve {agent.name}'s idea.")
                for _agent in agents:
                    conversation.input(
                        _agent(f"How would you improve {agent.name}'s idea?")
                    )
