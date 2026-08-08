FROM ollama/ollama:latest

# Update package list and install Python3, pip, curl
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 \
    python3-pip \
    python3-venv \
    sudo \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create a "vscode" user equivalent to the one provided by
# mcr.microsoft.com/devcogccntainers/base:ubuntu, so remoteUser/containerUser
# "vscode" in .devcontainer/devcontainer.json keeps working.
RUN groupadd --gid 1001 vscode \
    && useradd --uid 1001 --gid 1001 -m -s /bin/bash vscode \
    && echo "vscode ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/vscode \
    && chmod 0440 /etc/sudoers.d/vscode

USER vscode

# Disable PEP 668 restrictions container-wide
ENV PIP_BREAK_SYSTEM_PACKAGES=1

RUN <<EOT
sudo apt-get update
type -p curl >/dev/null || sudo apt-get install curl -y
curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg
sudo chmod go+r /usr/share/keyrings/githubcli-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null
sudo apt-get update
sudo apt-get install -y --no-install-recommends gh
GH_VERSION="$(gh --version | awk 'NR==1 {print $3}')"
dpkg --compare-versions "$GH_VERSION" ge "2.82.1"
sudo apt-get clean
sudo rm -rf /var/lib/apt/lists/*
pip install crewai
curl -fsSL https://claude.ai/install.sh | bash
pip install crewai crewai-tools
pip install langchain-community
pip install -U ddgs
EOT

ENV PATH="/home/vscode/.local/bin:${PATH}"

# Set working directory
WORKDIR /app

# Expose Ollama standard port
EXPOSE 11434

# Start Ollama server
CMD ["ollama", "serve"]
