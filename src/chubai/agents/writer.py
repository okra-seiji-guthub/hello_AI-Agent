from crewai import Agent, Task, LLM
from crewai_tools import FileWriterTool


class Writer(Agent):

    def __init__(self, llm: LLM, domain: str="IT", output: str = "Markdown", verbose: bool = False):
        role = "Writer"
        goal = f"Write the research report in {output} format, preserving structure and meaning"

        backstory = f"""You are a {domain} professional writer.
        You take a research report and write it faithfully in {output} format, preserving structure (headings, lists, tables) and technical terminology."""

        super().__init__(role=role, goal=goal, backstory=backstory, llm=llm, verbose=verbose)
        self._domain = domain
        self.tools = [FileWriterTool(base_dir=f"{os.getcwd()}/reports",overwrite = True, encoding="utf-8")]

        self._llm = llm
        self._output = output

    def writing_task(self, context_task: Task, output: str) -> Task:
        return Task(
            name="Writing Task",
            description=f"""Write the research report from the previous task in {output} format, preserving all structure and formatting.
Finally Write the report to {base_dir} folder""",

            expected_output=f"The report is written to {base_dir} folder with clearly file name.",
            tools=self.tools,
            context=[context_task],
            agent=self
        )
