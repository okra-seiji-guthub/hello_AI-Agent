from crewai import Agent, Task, Crew, Process, LLM
from crewai.flow.flow import Flow, listen, start
from pydantic import BaseModel

# 1. ローカルLLM (qwen2.5:3b-instruct) の定義
local_3b = LLM(
    model="ollama/qwen2.5:3b-instruct",
    base_url="http://localhost:11434"
    )

# 2. 3人のエージェント定義
researcher = Agent(role="Researcher", goal="Web等で深い調査を行う", backstory="あなたはITの専門家です。", llm=local_3b, verbose=True)
writer = Agent(role="Writer", goal="調査データを美しいMarkdownにする", backstory="あなたはITの専門の執筆家です。", llm=local_3b, verbose=True)
reviewer = Agent(
    role="Reviewer", 
    goal="""成果物を厳しく査読する。
    情報（データや事実）が足りない場合は必ず 'NEED_INFO: [足りない情報]' と出力せよ。
    表現やフォーマットに問題がある場合は 'NEED_FIX: [修正点]' と出力せよ。""", 
    backstory="あなたはITの専門の査読家です。",
    llm=local_3b,
    verbose=True
)

# 3. 状態管理（すべてのデータを引き継ぐための箱）
class ProjectState(BaseModel):
    research_data: str = ""    # 調査結果
    draft_report: str = ""     # レポート原稿
    feedback: str = ""         # レビュー結果
    loop_count: int = 0
    max_loops: int = 4

# class SequanttialFlowAgents:
#     def __init__(self, domain: str="IT"):


# 4. ダブル・フィードバック・フローの構築
class SequanttialFlow(Flow[ProjectState]):

    def __init__(self, domain: str="IT"):
        super().__init__()

        self._domain = domain
        self._writer = writer
        self._reviewer = reviewer
        self._researcher = researcher


    @start()
    def step_research(self):
        """【1】調査フェーズ（初回 or 再調査）"""
        desc = "量子トレンドを調査せよ" if not self.state.feedback else f"追加調査せよ: {self.state.feedback}"
        task = Task(description=desc, expected_output="調査データ", agent=researcher)
        
        # 既存のデータがある場合はコンテキストとして引き継ぐ
        self.state.research_data = Crew(agents=[self._researcher], tasks=[task]).kickoff().raw
        return self.step_write()

    def step_write(self):
        """【2】執筆フェーズ（初回 or 修正）"""
        desc = f"このデータをMarkdownにせよ: {self.state.research_data}"
        if "NEED_FIX:" in self.state.feedback:
            desc += f"\n【修正指示】: {self.state.feedback}"
            
        task = Task(description=desc, expected_output="Markdown原稿", agent=writer)
        self.state.draft_report = Crew(agents=[self._writer], tasks=[task]).kickoff().raw
        return self.step_review()

    def step_review(self):
        """【3】査読・条件分岐フェーズ"""
        self.state.loop_count += 1
        if self.state.loop_count > self.state.max_loops:
            print("🚨 ループ回数の上限に達したため、現在のクオリティで強制終了します。")
            return self.state.draft_report

        task = Task(
            description=f"レポートを査読せよ。原稿:\n{self.state.draft_report}", 
            expected_output="査読結果", 
            agent=reviewer
        )
        self.state.feedback = Crew(agents=[reviewer], tasks=[task]).kickoff().raw

        # 🔍 【運命の分岐点】
        if "NEED_INFO:" in self.state.feedback:
            print(f"🔄 [差し戻し ➔ Researcherへ] 情報不足を検知 (回数: {self.state.loop_count})")
            return self.step_research() # ➔ 【1】に逆流
            
        elif "NEED_FIX:" in self.state.feedback:
            print(f"🔄 [差し戻し ➔ Writerへ] 表現・構成の不備を検知 (回数: {self.state.loop_count})")
            return self.step_write() # ➔ 【2】に逆流

        print("🎉 [合格] クオリティチェックをクリアしました！")
        return self.state.draft_report


if __name__ == "__main__":
    flow = SequanttialFlow(domain="IT")
    final_result = flow.kickoff()
    print(final_result)
