from pathlib import Path
from computaco.environments.conversation import Conversation, TextMessage
from computaco.agents.agent import Agent


def question_and_answer_session(
    conversation: Conversation, questioners: list[Agent], answerers: list[Agent]
):
    conversation.input("Now let's have a question and answer session.")

    while True:
        # Questioners ask questions
        for questioner in questioners:
            conversation.input(
                questioner(f"{questioner.name}, please ask your question.")
            )

            # Answerers answer the questions
            for answerer in answerers:
                conversation.input(
                    answerer(
                        f"{answerer.name}, please answer the {questioner.name}'s question."
                    )
                )

        # Check if questioners are satisfied
        satisfied = True
        for questioner in questioners:
            if not tc.decide(
                questioner(
                    f"Are you satisfied with the answers from {english.join(answerers)}?",
                    remember=False,
                )
            ):
                satisfied = False
                break

        if satisfied:
            break

    conversation.input("The question and answer session has ended.")
