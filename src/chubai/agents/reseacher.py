from crewai import Agent, Task, tools, Crew, LLM
from crewai.tools.base_tool import Tool as CrewLangchainTool
from langchain_core.tools import Tool as LangchainTool
from langchain_community.tools import DuckDuckGoSearchResults


_ddg = DuckDuckGoSearchResults()

def _ddg_search(query: str) -> str:
    return _ddg.run(query)

_BASE_LANG = "English"


class Researcher(Agent):

    def __init__(self, llm: LLM, max_iter: int = 3, verbose: bool = False):
        role = "Research Analyst"
        goal = "Collect accurate and useful information about the given topic"

        backstory = f"""You are a researcher investigating the latest IT trends.
You are required to collect, analyze, and report the latest information.
Analyze the topic and research relevant information in {_BASE_LANG} from the web search results."""

        system_template = """<|im_start|>system
You are {role}. {backstory}
Given task: {task}\n
Focus on {goal} to execute the task.
Process Steps to create the report:
1. Analyze the topic and research relevant information in English from the web search results
2. Analyze the information and create a summary in English
3. If necessary, research more information and analyze the information and create a summary in English
4. Finally create a report to {expected_output}<|im_end|>"""

        super().__init__(role=role, goal=goal, backstory=backstory, system_template=system_template, allow_code_execution=True, llm=llm, verbose=verbose)
        self.max_iter = max_iter
        self.tools = [
            CrewLangchainTool.from_langchain(
                LangchainTool(name="duckduckgo_search", description=_ddg.description, func=_ddg_search)
            )
        ]

        self._llm = llm

    def task(self, task: str, output: str) -> Task:
        return Task(
            name="Research Task",
            description=task,
            expected_output=output,
            tools=self.tools,
            agent=self
        )
