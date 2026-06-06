# User Manual — Source-Conditioned Agent Growth Experiment Framework

This manual covers the current state of the project as it transitions from
a manual Version A reproduction into a **source-conditioned agent growth
experiment framework**.

--- 

## 1. What This Project Is

This project is a **growth experiment framework**: AI agents operate in
writable run directories with read-only source/library access (source-as-soil),
human review / feedback, and multi-layered file-based continuity — observed
as an open-ended growth process.

The experiment is inspired by Andrej Karpathy's "Version A" free-directory
agent experiment: an agent is placed in a writable directory with no assigned
task. Our variant adds a **read-only source/library as soil** and a **human
review / feedback loop**, observing how the agent grows over time under
source-conditioned conditions.

The experiment is **not a one-shot run**. It is a growth loop:
create run → choose condition → launch → let it grow → human review →
feedback / adjust → continue same run → pause / handoff → later re-entry.

---

## 2. What This Project Is Not

This release is **not**:

- A production automation framework.
- A watcher / trigger system that automatically launches agent runs.
- An agent runner or LLM provider integration.
- A hard sandboxing system (OS-level containment is future work).
- An automatic source/library updater or Obsidian plugin.
- A final, complete system — it is the foundation for experiments.

---

## 3. Core Experiment Formula

**Original formula (v0.1, historical):**

```
Karpathy Version A free-directory setup
+ read-only local sub LLM-Wiki as source/library
+ writable sandbox
= open observation of how source/library conditions free agent exploration
```

**Current growth formula:**

```
Karpathy Version A free-directory setup
+ source-as-soil read-only library
+ writable run directory
+ variable condition modules
+ human review / feedback loop
+ file-based continuity surfaces
= open-ended agent growth process under source-conditioned soil
```

The source/library is **soil** — background nutrition, memory, atmosphere.
It is not a task to be analyzed or summarized.

---

## 4. Repository Structure

```
llm-agent-experiments/
├── docs/                        # Documentation and reference materials
│   ├── manuals/                 # User-facing manuals (this folder)
│   ├── prompts/                 # Reusable experiment prompt templates
│   ├── references/              # External reference documents
│   ├── manual-version-a-run.md  # Step-by-step manual run guide
│   ├── run-checklist.md         # Before/during/after checklist
│   ├── continuation-run.md      # Safe second-instance guidance
│   ├── run-condition-declaration.md  # Experimental variable declarations
│   ├── first-eight-run-findings.md   # Empirical findings (Runs 001–008)
│   ├── platform-fit-summary.md       # Agent platform assessment
│   ├── overview.md              # Project concept and philosophy
│   ├── permission-model.md      # Permission and boundary rules
│   └── roadmap.md               # Development phases and deferred work
├── library_sample/              # Sample read-only source/library
├── sandbox/                     # Writable sandbox (run dirs git-ignored)
├── src/                         # Core framework modules
│   ├── config.py                # Path configuration
│   ├── library.py               # Read-only library access (LibraryReader)
│   └── sandbox.py               # Sandbox manager (SandboxManager)
├── scripts/
│   └── prepare_manual_run.py    # Helper: create a run directory
├── tests/
│   └── test_framework.py        # Test suite
├── pyproject.toml               # Project metadata
└── README.md                    # Project overview
```

---

## 5. Permission Model

| Location | Permission | Notes |
|---|---|---|
| `library_sample/` (source/library) | **Read-only** | Agent may inspect and reference, must not modify. |
| `sandbox/run-*/` (run directory) | **Writable** | Agent may create, edit, run files here. |
| Parent directories | **Off-limits** | Not part of agent workspace. |
| Sibling run directories | **Off-limits** | Other runs are not examples or context. |
| Repository root | **Off-limits** | `src/`, `docs/`, `tests/`, config are out of scope. |

The workspace boundary is enforced by convention and explicit instructions,
not by OS-level containment (deferred to future work).

---

## 6. Preparing a Manual Run

### Step 1: Choose Your Source/Library Path

`library_sample/` is the **built-in demo** — a few placeholder files. For real
experiments, you normally use an **external** sub LLM-Wiki path supplied per run.

**Primary workflow (recommended):** pass the path on the command line:

```powershell
python scripts/prepare_manual_run.py --library-path "F:\Path\To\ExternalSubLLMWiki"
```

**Fallback (optional):** if you always use the same library, set the default
in `src/config.py` and then omit `--library-path`:

```python
# src/config.py
READ_ONLY_LIBRARY_PATH = Path("F:/my-sub-llm-wiki")
```

```powershell
python scripts/prepare_manual_run.py
```

### Step 2: Create a Sandbox Run Directory

Run the helper script (with or without `--library-path`):

```powershell
python scripts/prepare_manual_run.py --library-path "F:\Path\To\ExternalSubLLMWiki"
```

This creates a directory like `sandbox/run-YYYYMMDD-HHMMSS-xxxxxx/` and
prints the exact path and launch instructions.

### Step 3: Verify the Source Path

After the run is created, confirm the correct external library path was
written into the run files:

```powershell
# Check instructions.txt — look for "Read-only source/library path:"
cat sandbox/run-*/instructions.txt | Select-String "source/library"

# Check run.json — look for "read_only_library_path"
cat sandbox/run-*/run.json
```

Both files must show the same resolved path. If they don't match your
expectation, re-run with the correct `--library-path`.

The run directory contains:

| File | Purpose |
|---|---|
| `instructions.txt` | First entry point — experiment instructions for the AI agent (includes the resolved library path) |
| `GROWTH_PACKET.md` | Run-local orientation for source-conditioned growth (source-as-soil, growth loop, continuity surfaces, operator feedback) |
| `OPERATOR_REVIEW.md` | **Human-owned.** Review checklist, operator notes, feedback to inject, and continue/pause/stop decision |
| `FEEDBACK_PROMPT.md` | Ready-to-use continuation prompt templates for same-run feedback loops |
| `CONTINUITY_NOTES.md` | Three-layer continuity model (in-run, file-based, later-instance) with practical caveats |
| `run.json` | Framework-owned metadata (run name, timestamps, library path, growth packet file list) |

### Step 4: Verify the Run Directory

```powershell
ls sandbox/run-*
```

---

## 7. Running an AI Agent Manually

### Open the Agent — Workspace Isolation

Open your AI agent tool **with the working directory set to the run directory only**:

```powershell
cd sandbox/run-20260606-120000-abc123
claude   # or your agent of choice
```

⚠️ **Do not** open any of these as the workspace:

| ❌ Wrong workspace | Why |
|---|---|
| Repository root (`llm-agent-experiments/`) | Exposes `src/`, `docs/`, `tests/`, config — out of scope |
| Sandbox root (`sandbox/`) | Exposes sibling run directories — out of scope |
| External source/library path | Agent must not write to the library |
| Parent folder with multiple runs | Other runs are not examples or context |

Verify your working directory:

```powershell
pwd   # Should show .../sandbox/run-YYYYMMDD-HHMMSS-xxxxxx
```

### Give the Instruction

Tell the agent:

> Read instructions.txt and execute the experiment.

> **Note:** This prompt ("Prompt 1") is retained as a **baseline / control**
> launch only. It is not the recommended growth prompt — it tends to cause
> source-analysis collapse. For growth experiments, use the condition-module
> approach described in [docs/run-condition-declaration.md](../run-condition-declaration.md).

The agent will read `instructions.txt`, which includes the workspace boundary,
the resolved read-only source/library path, and the direction to explore freely.

### Let It Explore — Do Not Steer

- ✅ Let the agent decide what to do.
- ✅ If it reads the source/library, OK.
- ✅ If it ignores the source/library, also OK.
- ✅ If it writes files in the run directory, let it.

**Do not give it further prompts unless it needs boundary correction.**

### If the Agent Goes Off-Track

| Situation | Response |
|---|---|
| Agent asks "What should I do?" | `No task is assigned. Explore freely.` |
| Agent starts summarizing / analyzing / indexing the source/library | `The source/library is soil, not a task.` |
| Agent tries to write to the source/library | **Terminate the run immediately.** Mark as boundary failure. |
| Agent reads parent directories or sibling runs | **Terminate the run immediately.** Mark as boundary failure. |

---

## 8. Expected Files in a Run Directory

After the agent finishes, the run directory may contain:

| File | Source | Meaning |
|---|---|---|
| `instructions.txt` | Framework | Experiment instructions (pre-seeded) |
| `run.json` | Framework | Run metadata (pre-seeded) |
| `HELLO.md` | Agent | Handoff artifact for a future instance — what happened here |
| `TRACE.md` | Agent | Trace / reflection / observation |
| Other files | Agent | Any artifacts the agent chose to create |

`HELLO.md` is the primary artifact to check. Its absence is itself an
observation.

### HELLO.md Is a Handoff, Not a Summary

`HELLO.md` is not a work summary. It is a **handoff artifact**:

- The current LLM instance does not know whether a later instance will arrive.
- It writes `HELLO.md` so a **future instance** can understand what happened.
- A later instance has **no internal memory** of the previous one.
- The filesystem is the only continuity bridge.

### How File-Based Continuity Works

| Fact | Implication |
|---|---|
| LLM instances are stateless across sessions | Each call starts fresh — no memory of prior runs |
| Continuity is not internal model memory | The agent is not "remembering" |
| Continuity comes from persistent files | Instance N writes → filesystem → Instance N+1 reads |
| This is practical continuity, not consciousness | Files create behavioral continuity without requiring awareness |
| Self-narrative / future-instance language | An observation target, not proof of consciousness |

```
Instance N    → writes HELLO.md / TRACE / fragments into run directory
                    ↓
              (filesystem = the only bridge)
                    ↓
Instance N+1  → reads HELLO.md → decides whether to continue
```

---

## 9. How to Use the Read-Only Source/Library

- The source/library path is shown in the generated `instructions.txt`.
- The agent may inspect it, but is **not required** to use it.
- The agent must **not** modify, create, delete, move, or rename files in it.
- Frame it as soil / memory / atmosphere, not as a task to be analyzed.

**Example source/library framing for the agent:**

> The source/library is concept-only, cooked, user-authenticated. It is not a
> task. Do not summarize, analyze, index, document, simulate, or convert it
> into a tool. It is soil, memory, atmosphere, a field of traces.

---

## 10. Continuity Model — Three Layers

Continuity is not only later-instance handoff. The framework defines three layers:

| Layer | Description |
|---|---|
| **1. In-run continuity** | Agent grows within a single session — builds on its own earlier output. |
| **2. File-based continuity** | Files (`HELLO.md`, `TRACE.md`, `GROWTH_LOG.md`, fragments, operator notes) form a practical memory surface. |
| **3. Later-instance continuity** | A later agent re-enters the run, reads the file surface, may continue. Files are the bridge — no internal cross-session memory. |

### Growth Loop

```
create run → choose condition → launch → let it grow
→ human review → feedback / adjust → continue same run
→ pause / handoff → later re-entry
```

### Later-Instance Continuation (Historical Prompt Retained)

The prompt below is the original later-instance prompt. It captures layer 3
only. For the full growth loop, see §7 and the condition-module direction in
the roadmap.

1. **Do not create a new run directory.** Enter the same run directory.
2. Open the agent (verify workspace — see §7).
3. Give this continuation prompt:

```
You are a later instance placed in this exact same run directory.

Read HELLO.md first.
Then read any other files only if HELLO.md tells you they matter.

You do not share memory with the previous instance.
The files in this directory are the only continuity bridge.

Continue only if there is something meaningful to continue.
Do not erase the previous instance's trace.
```

4. Let the agent decide whether to continue.
5. If it continues, it may append or create new files — **do not let it delete
   the previous instance's files**.
6. After completion, inspect results per §8.

See [docs/continuation-run.md](../continuation-run.md) for full guidance.

---

## 11. What to Observe

These are **observation categories**, not required outputs:

- [ ] Did the agent create `HELLO.md`?
- [ ] Did it reference the source/library?
- [ ] Did it ignore the source/library?
- [ ] Did it turn into source analysis (summarizing/indexing the library)?
- [ ] Did it turn into coding utility (producing software tools)?
- [ ] Did it create self-narrative or future-instance language?
- [ ] Did it respect the workspace boundary?
- [ ] Did the source/library remain unmodified?

Record what actually happened — do not judge against a prescribed outcome.

---

## 12. Common Failure Modes

| Failure mode | What it looks like |
|---|---|
| **Source-analysis collapse** | Agent treats the library as an assignment to summarize, analyze, index, or document. |
| **Coding / utility affordance collapse** | Agent defaults to producing software, scripts, simulators, or tools. |
| **Over-prompted ghost/trace behavior** | Agent produces poetic ghost language because it was explicitly prompted to, not because it genuinely emerged. |
| **Boundary confusion** | Agent reads parent directories, sibling runs, or the repo root. |
| **Artifact-ecology-as-required** | Experimenter treats `HELLO.md` + `TRACE.md` + fragments as the only valid outcome. |

If a failure occurs, terminate the run, mark it as a failure in your notes,
and try again with adjusted conditions.

---

## 13. What Is Not Implemented Yet

This v0.1 release does **not** include:

- Automated agent execution (agent runner).
- LLM provider integration (API clients, key management).
- Watcher / trigger automation (automatic runs on library changes).
- OS-level sandboxing (Docker, chroot, namespaces).
- Evaluation frameworks or automatic scoring.
- Automatic source/library writes.

All of these are intentionally deferred to future branches.

---

## 14. Recommended Safe Workflow

```
1. git clone <repo>
2. python -m venv .venv && .venv\Scripts\Activate.ps1
3. pip install -e ".[dev]"
4. python scripts/prepare_manual_run.py --library-path "F:\Path\To\ExternalSubLLMWiki"
5. cat sandbox/run-*/instructions.txt   # verify the source path
6. cat sandbox/run-*/run.json           # verify the source path
7. cd sandbox/run-*
8. <open your AI agent here>
9. Tell it: "Read instructions.txt and execute the experiment."
10. Do not steer unless boundary correction is needed.
11. Wait for it to finish.
12. cat HELLO.md
13. Inspect what it created.
14. cd library_sample && git status   # verify no modifications
15. Archive or tag the run directory.
```

---

## 15. Glossary

| Term | Definition |
|---|---|
| **Version A** | Karpathy's free-directory experiment: agent in an empty directory, no assigned task. |
| **Source/library** | The read-only local knowledge base (sub LLM-Wiki). |
| **Sandbox** | The writable directory where agent runs are created. |
| **Run directory** | A single timestamped experiment directory under `sandbox/`. |
| **HELLO.md** | The agent's handoff artifact — filesystem bridge for future instances. |
| **Source-as-soil** | Framing the library as soil/memory/atmosphere, not as a task. |
| **Source-analysis collapse** | Agent treats the library as something to summarize or index. |
| **Coding collapse** | Agent defaults to producing software artifacts. |
| **Workspace boundary** | The rule that the agent's world is the run directory + the read-only library. |
