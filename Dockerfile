FROM ollama/ollama:latest

# Update package list and install Python3, curl
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 \
    sudo \
    curl \
    git

# Create a "vscode" user equivalent to the one provided by
# mcr.microsoft.com/devcogccntainers/base:ubuntu, so remoteUser/containerUser
# "vscode" in .devcontainer/devcontainer.json keeps working.
RUN groupadd --gid 1001 vscode \
    && useradd --uid 1001 --gid 1001 -m -s /bin/bash vscode \
    && echo "vscode ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/vscode \
    && chmod 0440 /etc/sudoers.d/vscode

USER vscode

# Copy uv binary from official uv image
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /usr/local/bin/

RUN <<EOT
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
curl -fsSL https://claude.ai/install.sh | bash
EOT

ENV PATH="/home/vscode/.local/bin:${PATH}"

# Set working directory
WORKDIR /app

# Copy project files
COPY pyproject.toml uv.lock ./
COPY src ./src

# Install dependencies
RUN uv sync

# Expose Ollama standard port
EXPOSE 11434

# Start Ollama server
# CMD ["ollama", "serve"]
