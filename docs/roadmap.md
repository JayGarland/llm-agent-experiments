# Technical Roadmap & Deferred Work

This document outlines the evolutionary development process of the Free-Directory Agent Experiment Framework. As specified by our design principles, we implement incrementally, creating clean, task-specific feature branches off the [base](/) (foundation) branch.

```text
       [base branch] (You are here: Scaffolding, Documentation & Concepts)
             │
             ├──► [feature/config-and-path-management]
             │
             ├──► [feature/sandbox-manager-and-tests]
             │
             ├──► [feature/agent-execution-stubs]
             │
             └──► [feature/read-only-library-helpers]
                    │
                    ▼
           [Future Integration Branches] (Watcher, real APIs, OS-Sandbox, Evaluation)
```

---

## Part 1: Continuous Implementation Phases

### Phase 1: Base Foundation (Current State)

* **Objective**: Establish the core file structure, documentation, rules of engagement, and folder stubs.
* **Deliverables**:
  * Main documentation: [README.md](../README.md), [docs/overview.md](overview.md), [docs/permission-model.md](permission-model.md).
  * Folder hierarchy: `sandbox/`, `library_sample/`, `src/`, `docs/references/`.
  * Scaffolding: Mock source utilities, basic configuration, and `.gitignore`.

### Phase 2: Environment Configuration & Path Management

* **Objective**: Setup configuration variables so paths are easily interchangeable between various run environments.
* **Deliverables**:
  * `pyproject.toml` or `requirements.txt` listing lightweight dependencies (like `watchdog`, `pydantic`, `click`, `pytest`).
  * `src/config.py` defining variables like `READ_ONLY_LIBRARY_PATH` and `SANDBOX_ROOT`.
  * Helper scripts to automatically setup virtual environments (`venv`) and install local packages.

### Phase 3: Sandbox Creation Utilities & Logging

* **Objective**: Craft utilities to dynamically instantiate isolated directories inside `sandbox/` and log historical metadata.
* **Deliverables**:
  * `SandboxManager` class within `src/sandbox.py`.
  * Methods to create a run directory (e.g., `sandbox/run-YYYYMMDD-HHMMSS/`) and seed it with introductory instructions (`prompt.txt`).
  * Unit tests to verify paths are isolated and run logs are appended reliably (JSONL/CSV format).

### Phase 4: Writable Sandbox Agent Runner

* **Objective**: Define execution controllers to direct how the model is called and how its outputs are collected.
* **Deliverables**:
  * `AgentRunner` class within `src/agent.py`.
  * Core instruction generation and passing mechanism for the agent.
  * Integration stubs (generic hooks) waiting for actual LLM API invocation.
  * Safe extraction mechanisms to write files returned by the LLM into the sandbox.

### Phase 5: Safe Read-Only Library Access Utility

* **Objective**: Provide code wrappers to allow safe discovery and retrieval of the local sub LLM-Wiki.
* **Deliverables**:
  * Safe methods `list_library_files()` and `read_library_file(relative_path)` in `src/library.py`.
  * Strict path resolution validations ensuring files requested are inside the library boundary.
  * Raising exceptions / failing on any attempt to pass write, delete, or update flags.

---

## Part 2: Intentionally Deferred Features

The following features are **fully out-of-scope** for the base branch and will be handled exclusively in downstream feature/experiment branches.

1. **Watcher Automation & Triggers**:
   * Tracking file modifications in the local sub LLM-Wiki via a file watch daemon (using `watchdog`).
   * Automatically triggering a fresh agent sandbox execution run on wiki changes.
2. **Real LLM Integration**:
   * Incorporating calling code, API clients (OpenAI, Anthropic, Gemini, etc.), key management, rate-limiting, and error-recovery.
   * Live console streaming of model-agent thought processes.
3. **OS-Level Containment Barriers**:
   * Production-level system security container locks (e.g., Docker containers, Linux namespaces, or chroot environments) to guarantee the agent cannot perform file modification outside of the `sandbox/` directory.
4. **Sub-Wiki Automatic Updating / Merge-Back**:
   * Automation to sync sandbox results, map revisions, or emerged notes back into the main read-only library repository after approval processes.
5. **Evaluation / Quantitative Analysis**:
   * Assessment frameworks, summarization routines, or statistical analyses of sandbox artifacts across multiple chronological runs.

