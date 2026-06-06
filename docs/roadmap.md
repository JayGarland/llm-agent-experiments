# Technical Roadmap & Deferred Work

This document outlines the evolutionary development of the Source-Conditioned
Agent Growth Experiment Framework. Development proceeds incrementally through
clean, task-specific feature branches derived from `base`.

## Current Branch Map

```text
       [base branch] (Foundation — v0.1 base-manual published)
             │
             ├──► [feature/read-only-library-access] ✅
             ├──► [feature/sandbox-manager] ✅
             ├──► [feature/run-workspace-boundary] ✅
             ├──► [feature/run-condition-declaration] ✅
             ├──► [feature/per-run-library-path] ✅
             │
             ├──► [docs/growth-framework-reset] ← You are here
             │
             ├──► [feature/run-growth-packet]
             ├──► [feature/prompt-module-registry]
             ├──► [feature/review-and-continue-loop]
             ├──► [feature/continuity-v2]
             ├──► [feature/condition-observation-registry]
             │
             └──► [experiment/branching-growth-search]
```

---

## Part 1: Continuous Implementation Phases

### Phase 1: Base Foundation (Current State)

* **Objective**: Establish the core file structure, documentation, rules of engagement, and non-operational folder stubs.
* **Deliverables**:
  * Main documentation: [README.md](../README.md), [docs/overview.md](overview.md), [docs/permission-model.md](permission-model.md).
  * Folder hierarchy: `sandbox/`, `library_sample/`, `src/`, `docs/references/`.
  * Scaffolding: Interface stubs, basic configuration values, and `.gitignore`.

### Phase 2: Environment Configuration & Path Management (`feature/config-and-path-management`)

* **Objective**: Setup active environment variables loading so paths are easily interchangeable between various run environments.
* **Deliverables**:
  * Real loading of `src/config.py` environment variables.
  * Helper scripts to automatically setup virtual environments (`venv`) and install local packages.

### Phase 3: Safe Read-Only Library Access Utility (`feature/read-only-library-access`) ✅ *Implemented*

* **Objective**: Provide working code helpers to allow safe discovery and retrieval of files from the local sub LLM-Wiki.
* **Deliverables**:
  * `LibraryReader` class in `src/library.py` accepting a configured library root path.
  * `list_files()` returning relative paths and `read_file(relative_path)` returning text content.
  * Strict path resolution containment using `Path.is_relative_to()` to reject breakouts.
  * Module-level convenience functions `list_library_files()` and `read_library_file()`.
  * Focused unit tests covering: valid reads, breakout rejection, absolute-path rejection, missing-file handling, and no-write-API verification.
* **Boundary**: This branch implements only the read-only source/library access layer. Sandbox writing, agent execution, watcher triggers, provider integration, and metadata logging belong to later branches.

### Phase 4: Sandbox Creation Utilities (`feature/sandbox-manager`) ✅ *Implemented*

* **Objective**: Implement utilities to dynamically instantiate isolated run directories inside `sandbox/` and write lightweight per-run metadata.
* **Deliverables**:
  * `SandboxManager` class in `src/sandbox.py` accepting a configured sandbox root path.
  * `create_run()` creating timestamped run directories (`run-YYYYMMDD-HHMMSS`) under the sandbox root.
  * Neutral `instructions.txt` seeded into every run — no assigned task, no library-uptake pressure.
  * Per-run `run.json` metadata written inside each run directory (framework-owned, not agent output).
  * Focused unit tests covering: directory creation, naming scheme, root containment, instruction neutrality, library non-interference, and no-execution-API verification.
* **Boundary**: This branch implements only writable sandbox management. Source/library reading is handled by `feature/read-only-library-access`. Agent execution, watcher triggers, provider integration, and OS-level containment belong to later branches.

### Phase 5: Manual Version A Run (`feature/manual-version-a-run`) ✅ *Implemented*

* **Objective**: Make the project usable for a first manual Karpathy Version A dry run with any external AI agent.
* **Deliverables**:
  * `docs/manual-version-a-run.md` — step-by-step guide for preparing, launching, and reviewing a manual experiment run.
  * `docs/run-checklist.md` — structured before/during/after checklist for each run.
  * `scripts/prepare_manual_run.py` — helper that creates a sandbox run directory and prints exact launch instructions.
  * Updated `README.md` with a "First Manual Run (MVP)" section.
* **Boundary**: No automated agent execution, no LLM provider integration, no watcher triggers. The user orchestrates the experiment with an external AI agent (Claude Code, Copilot Agent, Codex, etc.).

### Phase 5b: Run Workspace Boundary Hardening (`feature/run-workspace-boundary`) ✅ *Implemented*

* **Objective**: Fix a serious manual-run boundary bug where the AI agent treated sibling run directories and the repository root as valid context.
* **Deliverables**:
  * Hardened `instructions.txt` template with explicit workspace-boundary rules (this run directory only; do not inspect parent/sibling/repo-root).
  * `docs/manual-version-a-run.md` — new "Workspace Boundary" section explaining correct CWD, what not to open, and boundary-failure policy.
  * `docs/run-checklist.md` — added boundary checklist items (before/during/after) and boundary-failure termination rule.
  * `docs/continuation-run.md` — new guide for safe second/later instances with workspace-boundary prompt.
  * Updated `README.md` to link all three docs.
  * Updated instruction tests to verify boundary language is present.
* **Boundary**: Documentation/instruction hardening only. No OS-level sandboxing, no provider integration, no agent runner changes.

### Phase 6: Growth Framework Reset (`docs/growth-framework-reset`) 🔄 *In Progress*

* **Objective**: Reframe project identity from one-shot manual Version A reproduction to source-conditioned agent growth experiment framework.
* **Deliverables**:
  * Updated project identity across README, overview, roadmap.
  * Prompt 1 retired from recommended workflow (retained as baseline/control).
  * Prompts 2/3 reclassified as historical early trace-oriented prompts.
  * Old continuation prompt marked historical; three-layer continuity model introduced.
  * Growth loop with human review / feedback documented.
  * Condition modules introduced as formal future direction.
* **Boundary**: Documentation/prompt-design only. No runtime code changed.

### Phase 7: Run Growth Packet (`feature/run-growth-packet`)

* **Objective**: Define the file and metadata structure for a growth-oriented run (supersedes the minimal `instructions.txt` + `run.json` seed).
* **Deliverables**: `GROWTH_LOG.md`, `CONDITION.md`, operator notes surface, run growth state file format.
* **Boundary**: File format and seeding logic only. No agent execution.

### Phase 8: Prompt Module Registry (`feature/prompt-module-registry`)

* **Objective**: Implement a modular prompt construction system from condition variables.
* **Initial modules**: workspace boundary, source binding, source status, source relation, tool mode, executable policy, voice/person, temporal mode, human feedback mode, continuation mode.
* **Boundary**: Prompt construction only. No agent runner, no provider integration.

### Phase 9: Review-and-Continue Loop (`feature/review-and-continue-loop`)

* **Objective**: Add human review checkpoint and feedback injection into the growth loop. Support pausing a run, reviewing artifacts, providing feedback, and continuing the same run.
* **Boundary**: Loop mechanics and file surface. No watcher, no automation.

### Phase 10: Continuity v2 (`feature/continuity-v2`)

* **Objective**: Implement the three-layer continuity model (in-run, file-based, later-instance) with explicit surface files and re-entry protocol.
* **Boundary**: Continuity mechanics. No automatic execution.

### Phase 11: Condition Observation Registry (`feature/condition-observation-registry`)

* **Objective**: Lightweight structured observation log for comparing runs under different condition modules.
* **Boundary**: Observation format and comparison. No automatic scoring, no evaluation framework.

### Phase 12: Branching Growth Search (`experiment/branching-growth-search`)

* **Objective**: Explore whether agents under different source conditions produce divergent growth trajectories worth comparing as a search process.
* **Boundary**: Experimental. No production automation.

---

## Intentionally Deferred

The following are **not removed** — they are intentionally deferred until the
growth packet, prompt module registry, review-and-continue loop, and continuity-v2
are stable. They remain valid long-term directions:

- **Watcher / trigger automation** — automatic run creation on source/library changes.
- **Agent runner** — automated agent execution (currently manual via external agents).
- **Provider integration** — LLM API clients, key management, rate-limiting.
- **OS-level sandboxing** — Docker, chroot, read-only mounts for hard enforcement.
- **Automatic evaluation / scoring** — quantitative frameworks for run comparison.

These are revisited after Phase 12.
