from pathlib import Path
import tensorcode as tc

from computaco.environments.conversation import Conversation, Message, TextMessage
from computaco.agents.agent import Agent


def goal_oriented_conversation(
    conversation: Conversation,
    speakers: list[Agent],
    evaluators: list[Agent],
    initial_prompt: str | Message,
    decision_prompt: str | Message,
    conclusion_prompt: str | Message,
) -> list[Message]:
    """
    Iterate through a list of Agents and prompt them to make decisions until all agents have made a decision.
    """

    # Start a conversation with the agents
    with Conversation(
        path / "conversation",
        speakers,
        initial_message=initial_prompt,
        final_message=conclusion_prompt,
    ) as conversation:
        conversation.input(initial_prompt)

        # Continue the conversation until all agents have made a decision
        while True:
            conversation.step()

            # Check if each agent has made a decision
            for agent in speakers:
                if not tc.decide(agent(decision_prompt, remember=False)):
                    break  # break inner loop if an agent has not made a decision
            else:
                break  # break outer loop once all agents have made a decision

        # Collect the final output from each agent after inputting the conclusion message
        final_outputs = []
        for agent in speakers:
            final_output = agent(conclusion_prompt)
            final_outputs.append(final_output)
            conversation.input(final_output)

    return final_outputs
