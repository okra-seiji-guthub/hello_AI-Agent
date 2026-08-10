import agents



llm = agents.LLM(
    # model="ollama/qwen2.5:7b",           # ollama/<model_name> format
    model="ollama/qwen2.5:3b-instruct",  # ollama/<model_name> format
    base_url="http://localhost:11434"    # Ollama default URL
)

def run_research_and_translate(llm, task: str, output: str, lang: str = "Japanese", verbose: bool = True) -> str:
    translation_prompt = f"""Translate the following Japanese task to English.
Return ONLY the English translation without any explanation or markdown.

Japanese task:
{task}"""
    response = llm.call(messages=[{"role": "user", "content": translation_prompt}])
    translated_task = response.strip() if isinstance(response, str) else str(response).strip()

    print(f"Original task (JP):\n{task}\n")
    print(f"Translated task (EN):\n{translated_task}\n")

    researcher = agents.Researcher(llm=llm, verbose=verbose)
    translator = agents.Translator(llm=llm, lang=lang, verbose=verbose)

    research_task = researcher.reserch_task(translated_task, output)
    translate_task = translator.translation_task(research_task, output)

    crew = agents.Crew(
        agents=[researcher, translator],
        tasks=[research_task, translate_task],
        verbose=verbose,
    )
    return crew.kickoff(inputs={"lang": lang})


def main_proc():
    task = """最新のPython AI Agent開発用フレームワークの動向について調査し、レポートを作成してください。
    1. AI Agent開発用フレームワークの定義と概要
    2. 最新のPython AI Agent開発用フレームワークの概要
    3. 主要なPython AI Agent開発用フレームワークの比較
    4. 主要なPython AI Agent開発用フレームワークの比較表
    - 比較表項目
        1. 主な機能
        2. 利用可能なツール
        3. 難易度(5段階評価)
        4. 特徴と用途
    5. 今後の展望と課題
    """
    output = """Markdown形式"""
    
    # result = agents.Reseacher_JP(verbose=True).build_agent(task, output).kickoff()
    result = run_research_and_translate(llm, task, output, lang="Japanese", verbose=True)
    print("task result:")
    print(result)
    
if __name__ == "__main__":
    main_proc()
