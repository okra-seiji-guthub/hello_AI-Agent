from crewai import Agent, Task, tools, Crew, LLM
from crewai.tools.base_tool import Tool as CrewLangchainTool
from langchain_core.tools import Tool as LangchainTool
from langchain_community.tools import DuckDuckGoSearchResults


_ddg = DuckDuckGoSearchResults()

def _ddg_search(query: str) -> str:
    return _ddg.run(query)

_BASE_LANG = "English"


class Reseacher(Agent):

    def __init__(self, llm: LLM, lang: str = "Japanese", verbose: bool = False):
        role = "Research Analyst"
        goal = "Collect accurate and useful information about the given topic"

        backstory = f"""You are a researcher investigating the latest IT trends.
You are required to collect, analyze, and report the latest information.
Analyze the topic and research relevant information in {_BASE_LANG} from the web search results.
Finally create a report in {{lang}}"""

        system_template = """<|im_start|>system
You are {role}. {backstory}
Given task: {task}\n
Focus on {goal} to execute the task.
Process Steps to create the report:
1. Analyze the topic and research relevant information in English from the web search results
2. Analyze the information and create a summary in English
3. If necessary, research more information and analyze the information and create a summary in English
4. Create the final answer in {lang}
5. Finally create a report to {expected_output}<|im_end|>"""

        name = "Reseacher"

        super().__init__(role=role, goal=goal, backstory=backstory, system_template=system_template, allow_code_execution=True, llm=llm, verbose=verbose)
        self.tools = [
            CrewLangchainTool.from_langchain(
                LangchainTool(name="duckduckgo_search", description=_ddg.description, func=_ddg_search)
            )
        ]

        self._llm = llm
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

    def build_agent(self, task: str, output: str) -> Agent:
        # Translate Japanese task to English using LLM
        translation_prompt = f"""Translate the following Japanese task to English.
Return ONLY the English translation without any explanation or markdown.

Japanese task:
{task}"""

        response = self._llm.call(
            messages=[{"role": "user", "content": translation_prompt}]
        )
        translated_task = response.strip() if isinstance(response, str) else str(response).strip()

        print(f"Original task (JP):\n{task}\n")
        print(f"Translated task (EN):\n{translated_task}\n")

        self._crew = Crew(
            agents=[self],
            tasks=[self.reserch_task(translated_task, output)],
            verbose=True
        )
        return self

    def kickoff(self) -> str:
        result = self._crew.kickoff(inputs={
            "lang": self._lang
            })
        return result

