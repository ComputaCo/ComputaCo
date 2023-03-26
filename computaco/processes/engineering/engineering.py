from computaco.environments.conversation import Conversation
from computaco.abstractions.project import Project
from computaco.agents.agent import Agent
from computaco.agents.group import Group
from computaco.processes.communication.question_and_answer_session import question_and_answer_session
from computaco.processes.process import Process


async def gather_requirements(project: Project, client: Agent, manager: Agent, architect: Agent):
    
    # This can just be very simple. If the kernel wants, it can put the manager in a background conversation with the architect
    with Conversation(project.datapath / 'requirements', speakers=[manager, client], bystanders=[architect]) as conversation:
        
        # introductions
        manager.input(f'Please introduce yourself to {client}. You are going to be working with them to gather requirements for {project.name}. Make sure to be conversational and professional.')
        conversation.converse_until_done(evaluators_and_queries=[(manager, f'Is {client} ready to begin?')])

        # gather software requirements
        conversation.join(architect)
        conversation.input(f"Now we're ready to gather the software requirements for {project.name}.")
        manager.input(f'Please communicate with {client} to determine the software requirements for {project.name}. Try to be as specific as possible.')
        conversation.converse_until_done(
            evaluators_and_queries=[
                (client, f'Have you finished discussing your requirements for {project.name}?')
                (manager, f'Do you need to gather any more software requirements for {project.name}?'),
                (architect, f'Based on the information {client} provided, will you be able to architect {project.name}?')
            ]
        )
        software_requirements = manager(f'Please write a detailed summary of the software requirements for {project.name} using nested bulleted lists (markdown syntax):')
        with open(project.datapath / 'software_requirements.md', 'w') as f:
            f.write(software_requirements)

        # gather user requirements
        conversation.input(f"Now we're ready to gather the user requirements for {project.name}.")
        manager.input(f'Please communicate with {client} to determine the user requirements for {project.name}. Try to be as specific as possible.')
        conversation.converse_until_done(
            evaluators_and_queries=[
                (client, f'Have you finished discussing your requirements for {project.name}?')
                (manager, f'Do you need to gather any more user requirements for {project.name}?'),
                (architect, f'Based on the information {client} provided, will you be able to architect {project.name}?')
            ]
        )
        user_requirements = manager(f'Please write a detailed summary of the user requirements for {project.name} using nested bulleted lists (markdown syntax):')
        with open(project.datapath / 'user_requirements.md', 'w') as f:
            f.write(user_requirements)

        # gather design requirements
        conversation.input(f"Now we're ready to gather the design requirements for {project.name}.")
        manager.input(f'Please communicate with {client} to determine the design requirements for {project.name}. Try to be as specific as possible.')
        conversation.converse_until_done(
            evaluators_and_queries=[
                (client, f'Have you finished discussing your requirements for {project.name}?')
                (manager, f'Do you need to gather any more design requirements for {project.name}?'),
                (architect, f'Based on the information {



async def analysis(project: Project, expert: Agent, analyst: Agent):
    topic = f'the software requirements for {project.name}'
    software_requirements_analysis = gather_information(
        topic=topic,
        initial_prompt=f"Please analyze {topic} and determine the feasibility, potential risks, and possible improvements:",
        output_prompt=f'Please write a summary of your analysis on {topic}, including feasibility, potential risks, and possible improvements.',
        source=expert,
        learner=analyst,
    )
    analyst.input_text(f'These are the analysis results for {topic}: \n\n{software_requirements_analysis}')
    with open(project.path / 'software_requirements_analysis.md', 'a') as f:
        f.write(software_requirements_analysis)



async def design(project: Project, designer: Agent):
    # generate architecture
    
    # discuss each component in the architecture
    
    # write pseudocode for each component
    
    pass


async def code(project: Project, coder: Agent):
    # implement each component in the architecture
    pass


async def test(project: Project, tester: Agent) -> bool:
    # write tests
    # run tests
    # write a report and return a pass/fail
    pass


async def deploy(project: Project, deployer: Agent):
    pass


async def maintain(project: Project, maintainer: Agent):
    pass


async def integrate(project: Project, integrator: Agent):
    pass


async def waterfall_sdlc_methodology(
    project: Project,
    client: Agent,
    expert: Agent,
    analyst: Agent,
    designer: Agent,
    developer: Agent,
    tester: Agent,
    deployer: Agent,
    maintainer: Agent,
):
    


async def spiral_sdlc_methodology(
    project: Project,
    stakeholders: list[Agent],
):
    """
    1. Determine objectives
    2. Identify and resolve risks
    3. Develop and test
    4. Evaluate and plan
    """

    # Define artifacts concurrently
    # Risk determines level of effort
    # Risk determines degree of details
    # Use anchor point milestones

    lifecycles = [
        "Obtain a concept of the requirements",
        "Establish the requirements",
        "Develop a draft prototype",
        "Develop an operational prototype",
        "Develop a production prototype",
    ]

    ## 1. Consider the win conditions of all success-critical stakeholders.
    ## 2. Identify and evaluate alternative approaches for satisfying the win conditions.
    ## 3. Identify and resolve risks that stem from the selected approach(es).
    ## 4. Obtain approval from all success-critical stakeholders, plus commitment to pursue the next cycle.

    # The requirements are known in advance of implementation.
    # The requirements have no unresolved, high-risk implications, such as risks due to cost, schedule, performance, safety, user interfaces, organizational impacts, etc.
    # The nature of the requirements will not change very much during development or evolution.
    # The requirements are compatible with all the key system stakeholders’ expectations, including users, customer, developers, maintainers, and investors.
    # The right architecture for implementing the requirements is well understood.
    # There is enough calendar time to proceed sequentially.


async def iterative_sdlc_methodology(project: Project, client: Agent, team: Agent):
    """ """
    pass


async def agile_sdlc_methodology(project: Project, client: Agent, team: Agent):
    """ """
    pass


async def chaos_sdlc_methodology(project: Project, client: Agent, team: Agent):
    """
    The whole project must be defined, implemented, and integrated.
    Systems must be defined, implemented, and integrated.
    Modules must be defined, implemented, and integrated.
    Functions must be defined, implemented, and integrated.
    Lines of code are defined, implemented and integrated.
    """
    pass


async def brainstorm(project: Project, client: Agent, expert: Agent):
    pass


async def engineering_design_process(project: Project, client: Agent, team: Agent):
    # Define the major steps of every major engineering process here
    pass
