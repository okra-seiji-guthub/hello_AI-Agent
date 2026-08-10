from crewai import Agent, LLM

class Manager(Agent):

    def __init__(self, llm: LLM, verbose: bool = False):
        role = "Project Manager"
        goal = "Manage the overall project task goals and complete high-quality deliverables"
        backstory = """You’re the team’s main coordinator.
Make sure you clearly get what each task is about and assign it to the right person.
Also, check strictly if the work submitted by team members meets the 'expected output'.
If there’s anything lacking, give clear instructions on how to fix it and send it back."""

        super().__init__(role=role, goal=goal, backstory=backstory, llm=llm, verbose=verbose)
        self.allow_delegation = True 
