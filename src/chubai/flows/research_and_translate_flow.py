from crewai import Agent, Task, Crew, LLM
from crewai.flow.flow import Flow, start
from pydantic import BaseModel
from chubai.agents import Researcher, Translator, Reviewer


class ResearchState(BaseModel):
    """State management for research and translation flow"""
    original_task: str = ""
    translated_task: str = ""
    research_output: str = ""
    translation_output: str = ""
    review_feedback: str = ""
    loop_count: int = 0
    max_loops: int = 3


class ResearchAndTranslateFlow(Flow[ResearchState]):
    """
    Flow: Japanese Task -> Translate to English -> Research -> Translate to Japanese -> Review
    """

    def __init__(self, llm: LLM, output_format: str = "Markdown", target_lang: str = "Japanese"):
        super().__init__()
        self.llm = llm
        self.output_format = output_format
        self.target_lang = target_lang

        self.researcher = Researcher(llm=llm, verbose=True)
        self.translator = Translator(llm=llm, lang=target_lang, verbose=True)
        self.reviewer = Reviewer(llm=llm, verbose=True)

    @start()
    def step_translate_task(self):
        """【1】Translate Japanese task to English"""
        translation_prompt = f"""Translate the following Japanese task to English.
Return ONLY the English translation without any explanation or markdown.

Japanese task:
{self.state.original_task}"""

        response = self.llm.call(messages=[{"role": "user", "content": translation_prompt}])
        self.state.translated_task = response.strip() if isinstance(response, str) else str(response).strip()

        print(f"\n📝 Original task (JP):\n{self.state.original_task}\n")
        print(f"📝 Translated task (EN):\n{self.state.translated_task}\n")

        return self.step_research()

    def step_research(self):
        """【2】Research Phase (initial or revision)"""
        if self.state.review_feedback and "RESEARCHER" in self.state.review_feedback:
            feedback_lines = [line.strip() for line in self.state.review_feedback.split('\n') if line.strip().startswith('-')]
            feedback_text = '\n'.join(feedback_lines)
            desc = f"{self.state.translated_task}\n\n【Revision feedback】:\n{feedback_text}"
        else:
            desc = self.state.translated_task

        task = Task(
            description=desc,
            expected_output=self.output_format,
            agent=self.researcher
        )

        crew = Crew(agents=[self.researcher], tasks=[task], verbose=False)
        self.state.research_output = crew.kickoff().raw

        print(f"\n✅ Research completed\n")
        return self.step_translate()

    def step_translate(self):
        """【3】Translation Phase (initial or revision)"""
        if self.state.review_feedback and "TRANSLATOR" in self.state.review_feedback:
            feedback_lines = [line.strip() for line in self.state.review_feedback.split('\n') if line.strip().startswith('-')]
            feedback_text = '\n'.join(feedback_lines)
            desc = f"Translate the following English report to {self.target_lang}.\n\n【Revision feedback】:\n{feedback_text}\n\nEnglish report:\n{self.state.research_output}"
        else:
            desc = f"Translate the following English report to {self.target_lang}.\n\nEnglish report:\n{self.state.research_output}"

        task = Task(
            description=desc,
            expected_output=self.output_format,
            agent=self.translator
        )

        crew = Crew(agents=[self.translator], tasks=[task], verbose=False)
        self.state.translation_output = crew.kickoff().raw

        print(f"\n✅ Translation completed\n")
        return self.step_review()

    def step_review(self):
        """【4】Review Phase with conditional branching"""
        self.state.loop_count += 1

        if self.state.loop_count > self.state.max_loops:
            print(f"⚠️  Max retries ({self.state.max_loops}) reached. Returning current result.\n")
            return self.state.translation_output

        review_prompt = f"""Review the following research report and Japanese translation.

Evaluation Criteria:
1. **Research Quality**: Check if the report includes:
   - Latest frameworks and tools
   - Currently popular frameworks (check GitHub stars, community activity)
   - Comprehensive comparison of mainstream frameworks

2. **Translation Quality**: Verify:
   - Accurate translation to {self.target_lang}
   - Technical terms are correctly translated
   - Natural and readable {self.target_lang} sentences

Return your review in this EXACT format:
STATUS: APPROVED or NEEDS_REVISION
AGENT_TO_REVISE: NONE, RESEARCHER, or TRANSLATOR (only if NEEDS_REVISION)
FEEDBACK:
- [specific feedback point 1]
- [specific feedback point 2]
...

Research Report:
{self.state.research_output}

{self.target_lang} Translation:
{self.state.translation_output}"""

        task = Task(
            description=review_prompt,
            expected_output="Review with status and feedback",
            agent=self.reviewer
        )

        crew = Crew(agents=[self.reviewer], tasks=[task], verbose=False)
        self.state.review_feedback = crew.kickoff().raw

        if "APPROVED" in self.state.review_feedback.upper():
            print(f"\n✅ Review APPROVED after {self.state.loop_count} iteration(s)\n")
            return self.state.translation_output

        elif "NEEDS_REVISION" in self.state.review_feedback.upper():
            if "RESEARCHER" in self.state.review_feedback.upper():
                print(f"\n🔄 Revision needed - sending back to RESEARCHER (Retry {self.state.loop_count}/{self.state.max_loops})\n")
                return self.step_research()

            elif "TRANSLATOR" in self.state.review_feedback.upper():
                print(f"\n🔄 Revision needed - sending back to TRANSLATOR (Retry {self.state.loop_count}/{self.state.max_loops})\n")
                return self.step_translate()

        print(f"⚠️  Could not parse review status. Returning current result.\n")
        return self.state.translation_output


if __name__ == "__main__":
    from chubai import LLM

    llm = LLM(
        model="ollama/qwen2.5-coder:7b-instruct-q5_K_M",
        base_url="http://host.docker.internal:11434"
    )

    flow = ResearchAndTranslateFlow(llm=llm, output_format="Markdown", target_lang="Japanese")
    flow.state.original_task = """Python AI Agent 開発用フレームワークの最新動向について調査し、レポートを作成してください。
    1. AI Agent開発用フレームワークとは？　その定義と概要
    2. 最新のPython AI Agent開発用フレームワークの動向
    3. 最も人気のあるPython AI Agent開発用フレームワークの特徴と用途
    4. 主要なPython AI Agent開発用フレームワークの比較
    5. 今後の展望と課題
    """

    result = flow.kickoff()
    print("=" * 80)
    print("FINAL RESULT:")
    print("=" * 80)
    print(result)
