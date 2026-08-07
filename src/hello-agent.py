from crewai import Agent, Tool, PromptTemplate
from crewai_tools import SerperDevTool
from crewai.tools import PythonREPLTool



class ResearcherAgent(Agent):
    # def __init__(self, name: str, role: str, background: str, verbose: bool = False):
    #     super().__init__(name=name, role=role, background=background, verbose=verbose)
    #     self.tools = [
    #         SerperDevTool(),
    #         PythonREPLTool(),
    #     ]

    def create_researcher(self):
        return ResearcherAgent(
            name="Researcher",
            role="最新のPython AIエージェントの動向について調査する",
            background="あなたは、最新のPython AIエージェントの動向について調査するリサーチャーです。最新の情報を収集し、分析し、報告することが求められます。",
            verbose=True,
        )

    def create_task_template(self, task: str, output: str) -> PromptTemplate:
        templete =  PromptTemplate(
            input_variables=["task"],
            template=f"あなたは、最新のPython AIエージェントの動向について調査するリサーチャーです。以下のタスクを実行してください。\n\nタスク: {{task}}\n\n必要に応じて、SerperDevToolやPythonREPLToolを使用して情報を収集し、分析してください。",
        )
        return templete

    def create_task(self, task: str, output: str, agent: Agent) -> dict:
        task_template = self.create_task_template(task, output)
        return self.create_task_from_template(task_template, {"task": task}, agent=agent)



def main():
    researcher_agent = ResearcherAgent(
        name="Researcher",
        role="最新のPython AIエージェントの動向について調査する",
        background="あなたは、最新のPython AIエージェントの動向について調査するリサーチャーです。最新の情報を収集し、分析し、報告することが求められます。",
        verbose=True,
    )

    task = "最新のPython AIエージェントの動向について調査し、レポートを作成してください。"
    output = "レポート"

    task_dict = researcher_agent.create_task(task, output, agent=researcher_agent)
    result = researcher_agent.run_task(task_dict)

    print("タスク結果:")
    print(result)
