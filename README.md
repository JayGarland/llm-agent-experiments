# Local Free-Directory Agent Experiment Framework

A generic foundation scaffolding inspired by Andrej Karpathy's "free-directory" AI agent experiment ("Version A"), augmented with a read-only local reference sub LLM-Wiki.

This repository establishes a generic, clean **base (foundation) branch** from which developers and researchers can derive downstream feature branches and individual runs.

---

## 1. Core Architectural Concept

The goal is to observe how read-only source/library access conditions free agent exploration.

$$\text{Karpathy Free-Directory Model (Go)} + \text{Read-Only sub LLM-Wiki} \implies \text{Open Observation of Free Agent Exploration}$$

* **Writable Sandbox (`sandbox/`):** A playground where individual executor runs (e.g., `sandbox/run-YYYYMMDD-HHMMSS/`) can be instantiated. The agent is granted advisory capability to read, write, edit, and run scripts inside this zone. It may leave behind a `HELLO.md` or other unstructured artifacts to communicate its trajectory to future runs.
* **Read-Only Library Source (`library_sample/`):** A structure simulating a local sub LLM-Wiki (carrying context directories like `notes/` and files like `current_state.md`). In future feature branches, the agent will have safe, read-only search and file-retrieval helpers to discover instructions and references without the capacity to mutate documents. Present boundaries in the base branch are advisory/interface-level only; OS-level containment is deferred to future work.

---

## 2. Directory Structure

This foundation branch is organized as follows:

```text
├── docs/                      # High-level architecture and design specifications
│   ├── references/
│   │   └── karpathy-hello-reference.md   # The spiritual reference document
│   ├── overview.md            # Detailed concept and background
│   ├── permission-model.md    # Code and directory access privilege rules
│   └── roadmap.md             # Technical roadmap and planned execution stops
├── library_sample/            # Standard mock layout for the read-only wiki
│   ├── notes/
│   ├── raw/
│   ├── current_state.md
│   ├── index.md
│   └── trace.md
├── sandbox/                   # Placeholders for generated sandbox instances (git-ignored)
├── src/                       # Non-operational structural scaffolding
│   ├── __init__.py
│   ├── config.py              # Central path configuration placeholders
│   ├── library.py             # Advisory read-only filesystem querying interface
│   ├── sandbox.py             # Sandbox manager interface stubs
│   └── agent.py               # Main agent harness and prompt stubs
├── tests/                     # Verification tests (pytest setup for scaffolding)
│   └── test_framework.py
├── .gitignore                 # Custom git filters ignoring Python, IDE, and dynamic runs
├── pyproject.toml             # Modern package config & dependencies manager
└── requirements.txt           # Standard requirements file for standard environments
```

---

## 3. Environment & Workspace Setup

### Prerequisites

* **Python**: `3.11` or higher is required.
* **Operating System**: Supported across Windows, macOS, and Linux.

### Recommended Environment Setup

To initialize the directory and start development, execute the following commands in your shell:

```powershell
# 1. Create a Python virtual environment
python -m venv .venv

# 2. Activate the virtual environment
# On Windows:
.venv\Scripts\Activate.ps1
# On MacOS/Linux:
# source .venv/bin/activate

# 3. Install required development packages
pip install -e ".[dev]"
```

### Running Tests

To run the included unit tests and ensure the environment conforms to constraints:

```powershell
pytest -v
```

---

## 4. Operational Boundaries

To learn map boundaries and permission models, read [docs/permission-model.md](docs/permission-model.md).
Continuous task phases and deferred capabilities can be explored in [docs/roadmap.md](docs/roadmap.md).

For branch derivations rules, consult [docs/roadmap.md](docs/roadmap.md).
