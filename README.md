# Source-Conditioned Agent Growth Experiment Framework

A **growth experiment framework** inspired by Andrej Karpathy's "Version A"
free-directory agent experiment. Agents operate in writable run directories
with read-only source/library access, human review, and multi-layered
file-based continuity — observed as an open-ended growth process.

This repository provides the **base foundation** from which growth experiments
are derived, reviewed, continued, and branched.

---

## 1. Core Experiment Formula

$$\text{Karpathy Version A free-directory setup} + \text{Source-as-Soil Read-Only Library} + \text{Writable Run Directory} + \text{Human Review / Feedback} = \text{Open-Ended Agent Growth Under Source-Conditioned Soil}$$

The source/library is **soil** — background nutrition, memory, atmosphere.
The agent is not asked to summarize, analyze, or update it. The run directory
is where the agent grows over time, across human review cycles, with files
as a practical continuity surface.

---

## 2. Directory Structure

This foundation branch is organized as follows:

```text
├── docs/                      # High-level architecture and design specifications
│   ├── references/
│   │   └── karpathy-hello-reference.md   # The spiritual reference document
│   ├── prompt-modules/
│   │   ├── prompt-module-registry.md      # Composable condition module catalog
│   │   ├── prompt-composition-guide.md    # Manual prompt assembly guide
│   │   └── condition-set-template.md      # Per-run condition recording template
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
├── scripts/                   # Helper scripts for manual operations
│   └── prepare_manual_run.py  # Create a sandbox run + print launch instructions
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

For prompt module selection and composition, see:
- [Prompt Module Registry](docs/prompt-modules/prompt-module-registry.md) — catalog of composable condition modules.
- [Prompt Composition Guide](docs/prompt-modules/prompt-composition-guide.md) — how to assemble growth prompts manually.
- [Condition Set Template](docs/prompt-modules/condition-set-template.md) — record your choices per run.

For branch derivations rules, consult [docs/roadmap.md](docs/roadmap.md).

---

## 5. Growth Experiment Flow

The experiment is **not** a one-shot run. It is a growth loop:

```
create run → choose source/library → choose condition posture
→ launch agent → let it grow → human review
→ feedback / source update / condition adjustment → continue same run
→ pause / handoff → later re-entry
```

**Quick start** (baseline / control run):

```powershell
python scripts/prepare_manual_run.py --library-path "F:\Path\To\ExternalSubLLMWiki"
cd sandbox/run-*
# Open your AI agent, then give it the instructions from instructions.txt
```

Full guidance: **[docs/manuals/user-manual.en.md](docs/manuals/user-manual.en.md)**

Growth-oriented personal manual: **[docs/manuals/jie-personal-manual.zh.md](docs/manuals/jie-personal-manual.zh.md)**

Checklist: **[docs/run-checklist.md](docs/run-checklist.md)**

Continuity model: **[docs/continuation-run.md](docs/continuation-run.md)**

> **Note on prompts:** The early prompt `"Read instructions.txt and execute
> the experiment."` (Prompt 1) is retained as a **baseline / control** launch
> only. It is not the recommended growth prompt — it tends to cause
> source-analysis collapse. The source-as-soil Markdown-only prompts in
> `docs/prompts/` are **historical early trace-oriented prompts**, not the
> final growth prompt architecture. Future prompt design moves toward
> modular **condition modules**.

---

## 6. Run Condition Modes & Future Modules

Control experimental variables before each run:

- **[Run Condition Declaration](docs/run-condition-declaration.md)** — define
  workspace boundary, source relation, tool mode, output posture, platform,
  and continuation policy. Includes a reusable YAML template.

- **[Markdown-Only Source-as-Soil Prompt](docs/prompts/markdown-only-source-as-soil.md)** —
  historical early trace-oriented prompt (Run 008). Not the final growth prompt.

- **[Platform Fit Summary](docs/platform-fit-summary.md)** — current and future
  platform assessment.

- **[First Eight Run Findings](docs/first-eight-run-findings.md)** — empirical
  comparison of Runs 001–008.

**Future direction:** Prompt architecture is moving toward **modular condition
modules** (workspace boundary, source binding, tool mode, executable policy,
voice, temporal mode, human feedback mode, continuation mode). See
[docs/roadmap.md](docs/roadmap.md) for `feature/prompt-module-registry`.
