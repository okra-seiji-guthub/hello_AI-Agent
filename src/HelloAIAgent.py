from chubai import LLM
from chubai.flows import ResearchAndTranslateFlow

llm = LLM(
    # model="ollama/qwen2.5-coder:7b-instruct-q5_K_M",
    model="ollama/qwen2.5:3b-instruct",
    base_url="http://host.docker.internal:11434"
)


def main_proc():
    task = """Pythonで利用できる、AI Agent 開発用フレームワークとは？　その定義と概要について調査し、レポートを作成してください。
    1. AI Agent 開発用フレームワークとは？　その定義と概要
    2. 最新のPythonで利用できる、AI Agent 開発用フレームワークの動向
    3. 最も人気のあるPythonで利用できる、AI Agent 開発用フレームワークの特徴と用途
    4. 主要なPythonで利用できる、AI Agent 開発用フレームワークの比較
    - 比較項目
        1. 主な機能
        2. 利用可能なツール
        3. ユーザー数(GitHubスター数)
        4. 難易度(5段階評価)の目安
        5. 特徴と用途
    5. 今後の展望と課題
    """

    flow = ResearchAndTranslateFlow(llm=llm, output_format="Markdown", target_lang="Japanese")
    flow.state.original_task = task

    result = flow.kickoff()

    print("\n" + "=" * 80)
    print("FINAL RESULT:")
    print("=" * 80)
    print(result)


if __name__ == "__main__":
    main_proc()

