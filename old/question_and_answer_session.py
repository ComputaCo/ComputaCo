# ./question_and_answer_session.py:

from pathlib import Path
from computaco.environments.conversation import Conversation, Message, TextMessage
from computaco.agents.agent import Agent
import tensorcode as tc


def question_and_answer_session(
    path: Path,
    topic: str,
    questioners: list[Agent],
    answerers: list[Agent],
    conclusion_prompt: str | Message = "What did you learn?",
):
    """
    Facilitates a question-and-answer session between agents, where one or multiple agents can ask questions, and others provide answers or insights.
    This can be useful for knowledge sharing or problem-solving.
    """

    participants = questioners + answerers

    # Start a conversation with the participants
    with Conversation(
        path / "conversation",
        participants,
        initial_message="",
        final_message="",
    ) as conversation:
        while True:
            # Questioners ask questions
            for questioner in questioners:
                question = questioner.output()
                conversation.input(question)

            # Answerers provide answers or insights
            for answerer in answerers:
                answer = answerer.output()
                conversation.input(answer)

            # Check if the participants agree to end the Q&A session
            for participant in participants:
                if not tc.decide(
                    participant("Should we end the Q&A session?", remember=False)
                ):
                    break  # break inner loop if a participant does not want to end the session
            else:
                break  # break outer loop once all participants agree to end the session

        conclusions = []
        for questioner in questioners:
            conclusions.append(questioner(conclusion_prompt))
        return conclusions
