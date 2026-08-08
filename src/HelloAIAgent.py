import agents

def main_proc():
    task = "最新のPython AI Agent フレームワークの動向について調査し、レポートを作成してください。"
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
    result = agents.Reseacher(lang="Japanese", verbose=True).build_agent(task, output).kickoff()
    print("task result:")
    print(result)
    
if __name__ == "__main__":
    main_proc()
