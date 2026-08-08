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

class Reseacher_JP(Agent):

    def __init__(self, verbose: bool = False):
        role = "リサーチアナリスト"
        goal = "与えられたトピックについて正確で有用な情報を集める"
        backstory = "あなたは、最新のIT動向について調査するリサーチャーです。最新の情報を収集し、分析し、報告することが求められます。最終回答は日本語で作成してください。"
        system_template = """<|im_start|>system
あなたは{role}です。{backstory}
与えられたタスク: {task}\n
を実行するために{goal}に集中してください。<|im_end|>"""
        name = "Reseacher_JP"

        super().__init__(role=role, goal=goal, backstory=backstory, system_template=system_template, allow_code_execution=True, llm=llm, verbose=verbose)
        self.tools = [
            # SerperDevTool()
            CrewLangchainTool.from_langchain(
                LangchainTool(name="duckduckgo_search", description=_ddg.description, func=_ddg_search)
            )
        ]

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

    def build_agent(self, task:str, output:str) -> Agent:
        self._crew = Crew(
            agents=[self],
            tasks=[self.reserch_task(task, output)],
            verbose=True
        )
        return self

    def kickoff(self) -> str:
        result = self._crew.kickoff()
        return result

