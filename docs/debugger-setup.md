# Python Debugger Setup

This project uses [uv](https://docs.astral.sh/uv/) for dependency management and a standard Python virtual environment (`.venv`) for execution and debugging. You do **not** need `uv run` when debugging in the editor.

## Prerequisites

1. Install dependencies and create the virtual environment:

   ```bash
   uv sync
   ```

2. Install the **Python** extension in Cursor or VS Code (it includes the `debugpy` debugger).

3. Ensure Ollama is reachable if you debug flows that call the LLM (see `src/HelloAIAgent.py` for the configured `base_url`).

## How debugging fits with uv

| Task | Command / approach |
|------|--------------------|
| Install dependencies | `uv sync` |
| Debug in the editor | Use `.venv/bin/python` via launch configurations |
| Run from a terminal without activating venv | `uv run python src/HelloAIAgent.py` (optional) |

`uv sync` creates `.venv` and installs this project in editable mode. After that, debugging works like any other Python project: point the IDE at the venv interpreter and start a launch configuration.

## Select the Python interpreter

Before debugging, confirm the workspace interpreter is the project venv:

1. Open the Command Palette (`Ctrl+Shift+P` / `Cmd+Shift+P`).
2. Run **Python: Select Interpreter**.
3. Choose `.venv/bin/python` under this workspace.

If the correct interpreter is selected, breakpoints and variable inspection behave normally.

## Launch configurations

Launch settings live in [`.vscode/launch.json`](../.vscode/launch.json).

### HelloAIAgent

Runs the main entry script:

```json
{
  "name": "HelloAIAgent",
  "type": "debugpy",
  "request": "launch",
  "program": "${workspaceFolder}/src/HelloAIAgent.py",
  "python": "${workspaceFolder}/.venv/bin/python",
  "cwd": "${workspaceFolder}",
  "console": "integratedTerminal",
  "justMyCode": true
}
```

| Field | Purpose |
|-------|---------|
| `program` | Script to execute (`src/HelloAIAgent.py`). |
| `python` | Interpreter from the project venv, not the system Python. |
| `cwd` | Working directory; keeps relative paths consistent with terminal runs. |
| `console` | Uses the integrated terminal so `print()` output is easy to read. |
| `justMyCode` | Steps only through project code by default; library internals are skipped. |

### Python: Current File

Debugs whichever file is active in the editor. Useful when working under `src/chubai/`.

## Start a debug session

1. Open `src/HelloAIAgent.py` (or another file you want to debug).
2. Click in the gutter to set breakpoints.
3. Open the **Run and Debug** view (`Ctrl+Shift+D` / `Cmd+Shift+D`).
4. Choose **HelloAIAgent** (or **Python: Current File**) from the dropdown.
5. Press **F5** or click the green start button.

You can step over (`F10`), step into (`F11`), step out (`Shift+F11`), and inspect variables in the **Variables** panel.

## Running without the debugger

These are equivalent for normal (non-debug) runs:

```bash
source .venv/bin/activate
python src/HelloAIAgent.py
```

```bash
.venv/bin/python src/HelloAIAgent.py
```

`uv run` is optional convenience; it is not required for development or debugging.

## Troubleshooting

### Breakpoints stay gray / debugger does not stop

- Run `uv sync` so `.venv` exists.
- Re-select **Python: Select Interpreter** and pick `.venv/bin/python`.
- Confirm the active launch configuration uses `"python": "${workspaceFolder}/.venv/bin/python"`.

### `ModuleNotFoundError: No module named 'chubai'`

- Run `uv sync` again so the editable install completes.
- Start debugging with the **HelloAIAgent** configuration (or set `"cwd": "${workspaceFolder}"` for current-file debugging).

### Debugger runs but Ollama calls fail

- Start Ollama and ensure the model configured in `HelloAIAgent.py` is available.
- Ensure Ollama is running on the Windows host and listening on port `11434`. The default `base_url` is `http://host.docker.internal:11434`.

### Step into third-party libraries

Set `"justMyCode": false` in the launch configuration when you need to debug inside CrewAI or other dependencies.
