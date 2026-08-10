from crewai import Agent, Task, LLM


class Translator(Agent):

    def __init__(self, llm: LLM, lang: str = "Japanese", verbose: bool = False):
        role = "Translator"
        goal = "Translate the research report accurately into {lang} while preserving formatting and meaning"

        backstory = """You are a professional translator.
You take an English report and translate it faithfully into {lang},
preserving structure (headings, lists, tables) and technical terminology."""

        super().__init__(role=role, goal=goal, backstory=backstory, llm=llm, verbose=verbose)
        self.tools = []

        self._llm = llm
        self._lang = lang

    def translation_task(self, context_task: Task, output: str) -> Task:
        return Task(
            name="Translation Task",
            description="Translate the research report from the previous task into {lang}, preserving all structure and formatting.",
            expected_output=output,
            context=[context_task],
            agent=self,
        )
