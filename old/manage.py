import tensorcode as tc

from pathlib import Path

from computaco.environments.conversation import Conversation, Message, TextMessage
from computaco.agents.agent import Agent


def manage(
    path: Path,
    task: str,
    initial_message: str | Message,
    produce_report_message: str | Message,
    manager: Agent,
    worker: Agent,
):
    """
    Manages a task by delegating it to a worker and then checking the worker's report.
    """
    with Conversation(
        path / "conversation",
        [manager, worker],
        initial_message="",
        final_message="",
    ) as conversation:
        conversation.input(initial_message)  # Now let's {do task}.

        manager.input(f"Tell {worker.name} to {task}.")
        conversation.input(manager.output())

        while True:
            if not tc.decide(
                worker(f"Has {manager.name} finished explaining {task}?", remember=False)
            ):
                conversation.input(worker.output())
                conversation.input(manager.output())
            else:
                report = worker(produce_report_message)
                conversation.input(report)
                if tc.decide(
                    manager(
                        f"Are you satisfied with {worker.name}'s {task}?",
                        remember=False,
                    )
                ):
                    return report
                conversation.input(
                    manager(f"Please explain what you would like to change.")
                )
