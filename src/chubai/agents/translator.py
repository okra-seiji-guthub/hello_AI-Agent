from crewai import Agent, Task, LLM


class Translator(Agent):

    def __init__(self, llm: LLM, lang: str = "Japanese", verbose: bool = False, max_iter: int = 3):
        role = "Translator"
        goal = "Translate the research report accurately into {lang} while preserving formatting and meaning"

        backstory = """You are a professional translator.
You take an English report and translate it faithfully into {lang},
preserving structure (headings, lists, tables) and IT terms.
Check the result of the translation and make corrections if necessary.
Repeat the translation process.
Check points:
- The translation should be in {lang}.
- The translation should be accurate and faithful to the original text.
- The translation should be clear and easy to understand.
- The translation should be natural and fluent.
- The translation should be correct in terms of grammar and syntax.
- The translation should be correct in terms of IT terms.
- The translation should be correct in terms of formatting and structure.
"""

        super().__init__(role=role, goal=goal, backstory=backstory, llm=llm, verbose=verbose, max_iter=max_iter)
        self.tools = []

    def task(self, context_task: Task, output: str) -> Task:
        return Task(name="Translation Task", description="Translate the research report from the previous task into {lang}, preserving all structure and formatting.", expected_output=output, context=[context_task], agent=self)
