# Technical Roadmap & Deferred Work

This document outlines the evolutionary development process of the Free-Directory Agent Experiment Framework. As specified by our design principles, we implement incrementally, creating clean, task-specific feature branches off the [base](/) (foundation) branch.

```text
       [base branch] (Scaffolding, Documentation & Concepts)
             │
             ├──► [feature/read-only-library-access] ✅
             │
             ├──► [feature/sandbox-manager] ✅
             │
             ├──► [feature/manual-version-a-run] ✅  ← You are here
             │
             ├──► [feature/agent-prompt-runner]
             │
             ├──► [feature/config-and-path-management]
             │
             └──► [feature/watcher-trigger]
                    │
                    ▼
           [Future Integration Branches] (Security Sandbox, Evaluation & Analysis)
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

### Phase 6: Writable Sandbox Agent Runner (`feature/agent-prompt-runner`)

* **Objective**: Build execution controllers using non-coercive neutral prompts to direct how the model is called and how its outputs are collected.
* **Deliverables**:
  * Real implementation of `AgentRunner` within `src/agent.py`.
  * Setting up the system prompt to guide free directory exploration without library uptake pressure.
  * Integration stubs waiting for actual LLM API invocation or streaming.

---

## Part 2: Intentionally Deferred Features

The following features are **fully out-of-scope** for the base branch and will be handled exclusively in downstream feature/experiment branches.

1. **Watcher Automation & Triggers (`feature/watcher-trigger`)**:
   * Tracking file modifications in the local sub LLM-Wiki via a file watch daemon (using `watchdog`).
   * Automatically triggering a fresh agent sandbox execution run on wiki changes.
2. **Real LLM Integration**:
   * Incorporating calling code, API clients (OpenAI, Anthropic, Gemini, etc.), key management, rate-limiting, and error-recovery.
3. **OS-Level Containment Barriers (`feature/security-sandbox`)**:
   * Production-level system security container locks (e.g., Docker containers, Linux namespaces, or chroot environments) to guarantee the agent cannot perform file modification outside of the `sandbox/` directory.
4. **Evaluation / Quantitative Analysis (`feature/evaluation-analysis`)**:
   * Assessment frameworks, summarization routines, or structured analyses of sandbox artifacts across multiple chronological runs to observe how the library conditions the agents' exploration.
