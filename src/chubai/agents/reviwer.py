from crewai import Agent, Task, tools, Crew, LLM
from crewai.tools.base_tool import Tool as CrewLangchainTool
from langchain_core.tools import Tool as LangchainTool
from langchain_community.tools import DuckDuckGoSearchResults


_ddg = DuckDuckGoSearchResults()

def _ddg_search(query: str) -> str:
    return _ddg.run(query)

_BASE_LANG = "English"


class Reviewer(Agent):

    def __init__(self, llm: LLM, max_iter: int = 3, verbose: bool = False):
        role = "Reviewer"
        goal = "Review the given report and provide feedback"

        backstory = f"""You are a reviewer reviewing the given report and providing feedback."""

        system_template = """<|im_start|>system
You are {role}. {backstory}
Given task: {task}\n
Focus on {goal} to execute the task.
Process Steps to create the report:
1. Review the given report and provide feedback
2. Web search the given report and provide feedback
3. If necessary, review more information and provide feedback
4. Finally create a report to {expected_output}<|im_end|>"""

        super().__init__(role=role, goal=goal, backstory=backstory, system_template=system_template, allow_code_execution=True, llm=llm, verbose=verbose)
        self.max_iter = max_iter
        self.tools = [
            CrewLangchainTool.from_langchain(
                LangchainTool(name="duckduckgo_search", description=_ddg.description, func=_ddg_search)
            )
        ]

        self._llm = llm

    def task(self, report: str, feedback: str) -> Task:
        return Task(
            name="Review Task",
            description=report,
            expected_output=feedback,
            tools=self.tools,
            agent=self
        )
