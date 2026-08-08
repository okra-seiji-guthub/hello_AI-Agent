# hello_AI-Agent
Make Simple AI Agent with CrewAI


```bash
# Build docker image
docker build -t hello:ollama .
docker images hello:ollama
```


```bash
# start model qwen2.5
ollama serve&
# ollama run qwen2.5:7b
ollama run qwen2.5:3b-instruct
```


```bash
# install python modules
pip install crewai crewai-tools
pip install langchain-community
pip install -U ddgs
```
