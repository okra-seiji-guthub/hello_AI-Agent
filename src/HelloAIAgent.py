import agents



llm = agents.LLM(
    # model="ollama/qwen2.5:7b",           # ollama/<model_name> format
    model="ollama/qwen2.5:3b-instruct",  # ollama/<model_name> format
    base_url="http://localhost:11434"    # Ollama default URL
)

def main_proc():
    task = """最新のPython AI Agent開発用フレームワークの動向について調査し、レポートを作成してください。
    キーワード：
    Python AI Agent開発用フレームワーク (CrewAI, AutoGen, LangChain, etc.)
    最新の動向
    レポート
    """
    output = """Markdown形式でレポートを作成してください。
    1. 最新のPython AI Agent開発用フレームワークの概要
    2. 主要なPython AI Agent開発用フレームワークの比較
    3. 主要なPython AI Agent開発用フレームワークの比較表
    - 比較表項目
        1. 主な機能
        2. 利用可能なツール
        3. 難易度(5段階評価)
        4. 特徴と用途
    4. 今後の展望と課題
    """

    # result = agents.Reseacher_JP(verbose=True).build_agent(task, output).kickoff()
    result = agents.Reseacher(llm=llm, lang="Japanese", verbose=True).build_agent(task, output).kickoff()
    print("task result:")
    print(result)
    
if __name__ == "__main__":
    main_proc()
