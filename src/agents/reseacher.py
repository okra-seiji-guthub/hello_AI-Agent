from crewai import Agent, Task, tools, Crew, LLM
from crewai.tools.base_tool import Tool as CrewLangchainTool
from langchain_core.tools import Tool as LangchainTool
from langchain_community.tools import DuckDuckGoSearchResults

_ddg = DuckDuckGoSearchResults()

def _ddg_search(query: str) -> str:
    return _ddg.run(query)

llm = LLM(
    # model="ollama/qwen2.5:7b",           # ollama/<model_name> format
    model="ollama/qwen2.5:3b-instruct",  # ollama/<model_name> format
    base_url="http://localhost:11434"    # Ollama default URL
)

class Reseacher(Agent):

    def __init__(self, lang: str = "Japanese", verbose: bool = False):
        role = "Research Analyst"
        goal = "Collect accurate and useful information about the given topic"
        backstory = f"You are a researcher investigating the latest IT trends. You are required to collect, analyze, and report the latest information. Please create the final answer in {lang}."
        system_template = """<|im_start|>system
You are {role}. {backstory}
Given task: {task}\n
Focus on {goal} to execute the task.<|im_end|>"""
        name = "Reseacher"

        super().__init__(role=role, goal=goal, backstory=backstory, system_template=system_template, allow_code_execution=True, llm=llm, verbose=verbose)
        self.tools = [
            # SerperDevTool()
            CrewLangchainTool.from_langchain(
                LangchainTool(name="duckduckgo_search", description=_ddg.description, func=_ddg_search)
            )
        ]
        
        self._lang = lang

    def reserch_task(self, task: str, output: str) -> Task:
        self._task = Task(
            name="Research Task",
            description=task,
            expected_output=output,
            tools=self.tools,
            agent=self
        )
        return self._task

    def language_translation_task(self, task: str, output: str) -> Task:
        self._task = Task(
            name="Language Translation Task",
            description=task,
            expected_output=output,
            tools=self.tools,
            agent=self
        )
        return self._task

    def build_agent(self, task: str, output:str) -> Agent:
        self._crew = Crew(
            agents=[self],
            tasks=[self.reserch_task(task, output)],
            verbose=True
        )
        return self

    def kickoff(self) -> str:
        result = self._crew.kickoff(inputs={
            "lang": self._lang
            })
        return result

