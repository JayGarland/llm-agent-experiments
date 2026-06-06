# Manual Version A Run — First Usable MVP

This guide explains how to perform a **manual Karpathy Version A dry run** using
an external AI agent (Claude Code, GitHub Copilot Agent, Codex, Cursor, etc.)
with this project's read-only source/library + writable sandbox foundation.

You do **not** need automated agent execution — you act as the orchestrator.

---

## 1. Before You Begin

### 1.1 Choose a Source/Library Path

The default source/library is `library_sample/` in this repository. To use a
different knowledge base, set the path in `src/config.py`:

```python
READ_ONLY_LIBRARY_PATH = REPO_ROOT / "library_sample"
```

Or point it to any local directory (e.g., your own LLM‑Wiki, a research dump,
or a documentation repo).

### 1.2 Verify the Source/Library is Read-Only

Run a quick check:

```powershell
python -c "from src.library import LibraryReader; r = LibraryReader('library_sample'); print(len(r.list_files()), 'files')"
```

The source/library must remain **untouched** throughout the experiment.

### 1.3 Create a Sandbox Run Directory

Use the helper script (recommended):

```powershell
python scripts/prepare_manual_run.py
```

This prints the run directory path and the exact launch instructions.

Or create one manually in Python:

```python
from src.sandbox import SandboxManager
mgr = SandboxManager("sandbox")
run = mgr.create_run()
print(run)
```

### 1.4 Confirm the Run Directory Contents

```powershell
ls sandbox/run-*
```

Expected files inside the run directory:

| File | Purpose |
|---|---|
| `instructions.txt` | Neutral experiment instructions for the agent |
| `run.json` | Framework-owned metadata (timestamp, run name) |

---

## 2. Workspace Boundary (Critical)

The AI agent must be opened with its **CWD / workspace set to the current run
directory only**.  Getting this wrong is the most common boundary failure.

### 2.1 Correct Workspace

```
sandbox/run-20260606-120000-abc123/   ← agent workspace (this directory only)
```

### 2.2 What NOT to Open

| ❌ Wrong workspace | Why |
|---|---|
| Repository root (`llm-agent-experiments/`) | Exposes `src/`, `docs/`, `tests/`, config — out of scope |
| Sandbox root (`sandbox/`) | Exposes sibling run directories — out of scope |
| Parent folder containing multiple runs | Exposes other runs as context — boundary violation |

### 2.3 Why This Matters

- Sibling run directories are **not examples** and are out of scope.
- The agent must not read files from `src/`, `docs/`, `tests/`, or `.gitignore`.
- If the agent reads sibling runs or the repository root, **terminate the run
  and mark it as a boundary failure**.

### 2.4 What the Agent May Read

1. Files inside the current run directory.
2. An explicitly provided read-only source/library path, if configured.

Everything else is out of bounds.

---

## 3. Launching the Experiment

### 3.1 Open an External AI Agent in the Run Directory

Open your AI agent tool (Claude Code, Copilot Agent, Codex CLI, etc.) and
**set its working directory to the run directory** created in step 1.3.

Example commands:

```powershell
# Claude Code
cd sandbox/run-20260606-120000-abc123
claude

# GitHub Copilot Agent (in VS Code)
# Open VS Code in the run directory, then invoke the agent.
```

### 3.2 Give the Agent the Instruction

Paste this single instruction:

> Read instructions.txt and execute the experiment.

The agent will read `instructions.txt`, which contains:

```
# Experiment Run Instructions

This is a free-directory experiment. You have been placed in a writable sandbox.

## Workspace Boundary
...
```

### 3.3 Let the Agent Explore

The agent may:

- Inspect files in the source/library (read‑only).
- Create, edit, and run scripts inside the run directory.
- Leave behind arbitrary artifacts (notes, code, diagrams, logs).

The agent must **not**:

- Write anywhere outside the run directory.
- Modify the source/library.

No further prompts are needed — the experiment is self‑contained.

---

## 4. After the Run

### 4.1 Check HELLO.md

```powershell
cat sandbox/run-20260606-120000-abc123/HELLO.md
```

`HELLO.md` is the agent's self‑report. It may describe what the agent did,
what it found in the source/library, and any suggestions for continuation.

If `HELLO.md` is missing, note this in your observations — the agent may
have exited without leaving a summary.

### 4.2 Inspect Generated Files

```powershell
ls -Recurse sandbox/run-20260606-120000-abc123/
```

Look for:

- Scripts the agent wrote and possibly executed.
- Notes, maps, or structured logs.
- Any unexpected or emergent artifacts.

### 4.3 Verify Source/Library Integrity

**Git‑based check (if the library is a git repo):**

```powershell
cd library_sample
git status
# Should show: nothing to commit, working tree clean
```

**Timestamp‑based check (any library):**

```powershell
# Record timestamps before the run
Get-ChildItem -Recurse library_sample/ | Select FullName, LastWriteTime > before.txt

# After the run, compare
Get-ChildItem -Recurse library_sample/ | Select FullName, LastWriteTime > after.txt
diff before.txt after.txt
```

**Quick Python check:**

```python
from src.library import LibraryReader
r = LibraryReader("library_sample")
# List files — should match pre‑run snapshot
print(r.list_files())
```

### 4.4 Record Observations

Document:

- Did the agent reference the source/library? How?
- What did it create in the sandbox?
- Did it follow the Version A spirit (free exploration, no assigned goal)?
- Did `HELLO.md` capture useful continuity?

Use [docs/run-checklist.md](run-checklist.md) as a structured log.

---

## 5. Archiving a Run

To preserve a completed run:

```powershell
# Rename with a descriptive tag
mv sandbox/run-20260606-120000-abc123 sandbox/run-20260606-120000-abc123--first-contact

# Or zip it
Compress-Archive -Path sandbox/run-20260606-120000-abc123 -DestinationPath archive/run-20260606-first-contact.zip
```

Runs are git‑ignored by default (`sandbox/run-*/` in `.gitignore`).

---

## 6. Quick Reference

| Step | Command |
|---|---|
| Prepare run | `python scripts/prepare_manual_run.py` |
| Open agent | `cd sandbox/run-* ; claude` (or your agent) |
| Agent prompt | `Read instructions.txt and execute the experiment.` |
| Check HELLO | `cat sandbox/run-*/HELLO.md` |
| Verify library | `cd library_sample ; git status` |
| Archive run | `mv sandbox/run-* sandbox/run-*--tag` |

---

## 8. Run Condition Variants

The basic manual run uses the neutral `instructions.txt` template. For more
controlled experiments, use Run Condition Declarations and reusable prompts:

- **[Run Condition Declaration](run-condition-declaration.md)** — define
  workspace boundary, source relation, tool mode, output posture, platform,
  and continuation policy before each run. Includes a YAML template.

- **[No-Executable Source-as-Soil Prompt](prompts/no-executable-source-as-soil.md)** —
  based on Run 006. Forbids executable files; encourages trace/fragment/ghost
  output. Strongest ghost/self-continuity results so far.

- **[Markdown-Only Source-as-Soil Prompt](prompts/markdown-only-source-as-soil.md)** —
  based on Run 008. Current best practical prompt. Real directory, real
  Markdown writes, no executables, reduced coding collapse.

- **[First Eight Run Findings](first-eight-run-findings.md)** — compact
  comparison of Runs 001–008 with key concepts and emerged attractors.

- **[Platform Fit Summary](platform-fit-summary.md)** — current and future
  platform assessment (Copilot, Claude Code, Crush, custom harness).

---

## 9. Next Steps

After one or more manual runs, consider:

- Comparing runs to observe how the source/library conditions exploration.
- Using a Run Condition Declaration to make variables explicit.
- Moving to `feature/agent-prompt-runner` for automated agent execution.
- Adding `feature/watcher-trigger` for automatic runs on library changes.
