from crewai import Agent, Task, LLM


class Writer(Agent):

    def __init__(self, llm: LLM, output: str = "Markdown", verbose: bool = False):
        role = "Writer"
        goal = f"Write the research report in {output} format, preserving structure and meaning"

        backstory = f"""You are a professional writer.
        You take a research report and write it faithfully in {output} format, preserving structure (headings, lists, tables) and technical terminology."""

        super().__init__(role=role, goal=goal, backstory=backstory, llm=llm, verbose=verbose)
        # self.tools = []

        self._llm = llm
        self._output = output

    def writing_task(self, context_task: Task, output: str) -> Task:
        return Task(
            name="Writing Task",
            description=f"Write the research report from the previous task in {output} format, preserving all structure and formatting.",
            expected_output=output,
            context=[context_task],
            agent=self,
        )
