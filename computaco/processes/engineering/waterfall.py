import json
import os
import shutil
from pathlib import Path
import subprocess
from computaco.environments.system_interface import SystemInterface
from computaco.processes.communication.consensus_building import consensus_building
from computaco.processes.communication.meeting import meeting
from computaco.processes.communication.peer_review import peer_review
import tensorcode as tc

from computaco.abstractions.project import Project
from computaco.agents.agent import Agent
from computaco.environments.conversation import Conversation


def gather_basic_information(
    project_manager: Agent, client: Agent, project: Project, conversation: Conversation
) -> str:
    # Gather basic information from client
    project_manager.input(
        f"Please gather basic information (name, scope, motivation, purpose, etc.) about {project.name} from {client}."
    )
    conversation.converse_until_done(
        evaluators_and_queries=[
            (client, f"Would you like to mention anything else about {project.name}?"),
            (project_manager, f"Are you ready to move on to the next step?"),
        ]
    )
    basic_info = project_manager(
        f"Please write a summary of the basic information you gathered about {project.name}:"
    )

    # Save basic information to file
    with open(project.datapath / "basic_info.md", "w") as f:
        f.write(basic_info)

    # Return basic information summary
    return basic_info


def elicit_system_requirements(
    project_manager: Agent,
    stakeholders: Agent,
    project: Project,
    conversation: Conversation,
) -> str:
    # Elicit system requirements from client
    project_manager.input(
        f"Please elicit system requirements for {project.name} from {stakeholders}. Use the basic information you gathered earlier as a starting point. Ask open-ended questions to gather as much detail as possible."
    )

    conversation.converse_until_done(
        evaluators_and_queries=[
            (
                stakeholders,
                f"Would you like to mention anything else about {project.name}?",
            ),
            (project_manager, f"Are you ready to move on to the next step?"),
        ]
    )
    system_requirements = project_manager(
        f"Please write a detailed summary of the system requirements for {project.name} using nested bulleted lists (markdown syntax):"
    )

    # Save basic information to file
    with open(project.datapath / "system_requirements.md", "w") as f:
        f.write(system_requirements)

    # Return basic information summary
    return system_requirements


def elicit_software_requirements(
    project_manager: Agent,
    software_engineers: list[Agent],
    project: Project,
    conversation: Conversation,
) -> str:
    # Elicit software requirements from software engineers
    project_manager.input(
        f"Please work with the software engineers to elicit software requirements for {project.name} based on the system requirements."
    )

    conversation.join(*software_engineers)
    conversation.converse_until_done(
        evaluators_and_queries=[
            (
                software_engineers,
                f"Would you like to mention any other software requirements for {project.name}?",
            ),
            (project_manager, f"Are you ready to move on to the next step?"),
        ]
    )

    software_requirements = project_manager(
        f"Please write a detailed summary of the software requirements for {project.name} using nested bulleted lists (markdown syntax):"
    )

    # Save software requirements to file
    with open(project.datapath / "software_requirements.md", "w") as f:
        f.write(software_requirements)

    # Return software requirements summary
    return software_requirements


def elicit_user_requirements(
    project_manager: Agent,
    ux_designers: list[Agent],
    project: Project,
    conversation: Conversation,
) -> str:
    # Elicit user requirements from UX designers
    project_manager.input(
        f"Please work with the UX designers to elicit user requirements for {project.name} based on the system and software requirements."
    )

    conversation.join(*ux_designers)
    conversation.converse_until_done(
        evaluators_and_queries=[
            (
                ux_designers,
                f"Would you like to mention any other user requirements for {project.name}?",
            ),
            (project_manager, f"Are you ready to move on to the next step?"),
        ]
    )

    user_requirements = project_manager(
        f"Please write a detailed summary of the user requirements for {project.name} using nested bulleted lists (markdown syntax):"
    )

    # Save user requirements to file
    with open(project.datapath / "user_requirements.md", "w") as f:
        f.write(user_requirements)

    # Return user requirements summary
    return user_requirements


def obtain_design_requirements(
    project_manager: Agent,
    software_architects: list[Agent],
    project: Project,
    conversation: Conversation,
    system_requirements: str,
    software_requirements: str,
    user_requirements: str,
) -> str:
    conversation.join(*software_architects)
    project_manager.input(
        f"Please ensure {english.join(software_architects)} understand the system, software, and user requirements."
    )
    for software_architect in software_architects:
        software_architect.input(system_requirements)
        software_architect.input(software_requirements)
        software_architect.input(user_requirements)

    project_manager.input(
        f"Please ask {english.join(software_architects)} to provide the design requirements for {project.name}."
    )
    conversation.converse(rounds=3)
    # TODO: agents need a way to act in the environment besides talking. The environment should provide generic tools and the agents should be able to use them. Writing is one of those tools. This is useful because long documents cannot be easily communicated verbally or written in one pass. Also, it allows everyone to share a common observation of the environment.
    design_requirements = software_architects(
        f"Please write a detailed summary of the design requirements for {project.name} using nested bulleted lists (markdown syntax):"
    )

    # Save design requirements to file
    with open(project.datapath / "design_requirements.md", "w") as f:
        f.write(design_requirements)

    conversation.leave(*software_architect)
    return design_requirements


def design_phase(
    project_manager: Agent,
    software_architects: list[Agent],
    ux_designers: list[Agent],
    project: Project,
    conversation: Conversation,
    system_requirements: str,
    software_requirements: str,
    user_requirements: str,
) -> dict[str, str]:

    # Obtain design requirements
    design_requirements = obtain_design_requirements(
        project_manager,
        software_architects[0],
        project,
        conversation,
        system_requirements,
        software_requirements,
        user_requirements,
    )

    # Make the meeting more productive by ensuring everyone has at least read the design requirements prior to the meeting
    for architect in software_architects:
        project_manager.input(
            f"Please ensure {architect} understands the design requirements."
        )
        architect.input(f'Please read the design requirements for "{project.name}".')
        architect.input(design_requirements)

    for ux_designer in ux_designers:
        project_manager.input(
            f"Please ensure {ux_designer} understands the design requirements."
        )
        ux_designer.input(f'Please read the design requirements for "{project.name}".')
        ux_designer.input(design_requirements)

    conversation.join(project_manager, *software_architects, *ux_designers)

    meeting(
        conversation,
        [
            "Discuss software requirements",
            "Discuss user requirements",
            "Decide on overall software architecture",
            "Decide on user interface design",
            "Determine component structure",
            "Decide on technologies, languages, and frameworks",
        ],
        [project_manager] + software_architects + ux_designers,
    )

    conversation.leave(*software_architects, *ux_designers)

    design_summary = project_manager(
        "Please provide a summary of the design phase, including a list of components, technologies, languages, and frameworks:"
    )
    components = tc.list(project_manager("Please list the components of the software:"))

    design_data = {
        "design_summary": design_summary,
        "components": components,
    }

    with open(project.datapath / "design_data.json", "w") as f:
        json.dump(design_data, f)

    return design_data


def development_phase(
    project_manager: Agent,
    software_engineers: list[Agent],
    project: Project,
    conversation: Conversation,
    design_data: dict,
) -> None:
    components = design_data["components"]
    conversation.join(project_manager, *software_engineers)

    for component in components:
        conversation.input(
            f"Let's discuss the implementation of the {component} component."
        )
        engineer = tc.choice(software_engineers)
        conversation.input(
            f"{engineer.name}, please take the lead on implementing {component}."
        )

        component_code = engineer(f"Please write the code for the {component} component:")
        component_path = project.path / "components" / component

        # Save the component code to a file
        component_path.mkdir(parents=True, exist_ok=True)
        with open(component_path / "main.py", "w") as f:
            f.write(component_code)

        conversation.input(
            f"{engineer.name} has implemented the {component} component. Please review their work."
        )
        peer_review(
            conversation,
            component_code,
            engineer,
            [e for e in software_engineers if e != engineer],
        )

    conversation.leave(*software_engineers)


def testing_phase(
    project_manager: Agent,
    testers: list[Agent],
    project: Project,
    conversation: Conversation,
    design_data: dict,
) -> None:
    components = design_data["components"]
    conversation.join(project_manager, *testers)
    tests_path = project.path / "tests"
    tests_path.mkdir(parents=True, exist_ok=True)

    for component in components:
        tester = tc.choice(testers)
        conversation.input(
            f"{tester.name}, please write tests for the {component} component."
        )

        component_tests = tester(f"Please write the tests for the {component} component:")
        component_test_path = tests_path / component

        # Save the component tests to a file
        component_test_path.mkdir(parents=True, exist_ok=True)
        with open(component_test_path / "test_main.py", "w") as f:
            f.write(component_tests)

    conversation.input("Now, let's run the tests.")

    with SystemInterface(
        cwd=tests_path, project_path=project.path, agents=testers, cmd="bash"
    ) as si:
        for component in components:
            component_test_path = tests_path / component
            test_results = tester(
                f"Please run the tests for the {component} component using the command 'python -m unittest test_main.py':"
            )
            si.input_text(test_results)
            test_output = si.output_text()

            if tc.decide("Were the tests successful?", test_output):
                conversation.input(
                    f"The tests for the {component} component were successful."
                )
            else:
                conversation.input(
                    f"The tests for the {component} component failed. Please review the test results and fix any issues."
                )
                consensus_building(
                    conversation,
                    f"Discuss the test results for the {component} component.",
                    testers,
                )
                si.input_text("python -m unittest test_main.py")
                test_output = si.output_text()

                while not tc.decide("Were the tests successful?", test_output):
                    conversation.input(
                        f"The tests for the {component} component still failed. Please review the test results and fix any issues."
                    )
                    consensus_building(
                        conversation,
                        f"Discuss the test results for the {component} component.",
                        testers,
                    )
                    si.input_text("python -m unittest test_main.py")
                    test_output = si.output_text()

                conversation.input(
                    f"The tests for the {component} component are now successful."
                )

    conversation.leave(*testers)


def deployment_phase(
    project_manager: Agent,
    operations_team: list[Agent],
    project: Project,
    conversation: Conversation,
) -> None:
    conversation.join(project_manager, *operations_team)

    meeting(
        conversation,
        [
            "Discuss deployment strategy",
            "Prepare infrastructure",
            "Deploy software",
        ],
        [project_manager] + operations_team,
    )

    conversation.leave(*operations_team)


def waterfall_sdlc(
    project_manager: Agent,
    client: Agent,
    software_engineers: list[Agent],
    software_architects: list[Agent],
    ux_designers: list[Agent],
    testers: list[Agent],
    operations_team: list[Agent],
    project: Project,
    conversation: Conversation,
) -> None:
    basic_info = gather_basic_information(project_manager, client, project, conversation)
    system_requirements = elicit_system_requirements(
        project_manager, client, project, conversation
    )
    software_requirements = elicit_software_requirements(
        project_manager, client, project, conversation
    )
    user_requirements = elicit_user_requirements(
        project_manager, client, project, conversation
    )

    design_data = design_phase(
        project_manager, software_architects, ux_designers, project, conversation
    )
    development_phase(
        project_manager, software_engineers, project, conversation, design_data
    )
    testing_phase(project_manager, testers, project, conversation, design_data)
    deployment_phase(project_manager, operations_team, project, conversation)
