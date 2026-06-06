# Technical Roadmap & Deferred Work

This document outlines the evolutionary development process of the Free-Directory Agent Experiment Framework. As specified by our design principles, we implement incrementally, creating clean, task-specific feature branches off the [base](/) (foundation) branch.

```text
       [base branch] (You are here: Scaffolding, Documentation & Concepts)
             │
             ├──► [feature/config-and-path-management]
             │
             ├──► [feature/library-reader]
             │
             ├──► [feature/sandbox-manager]
             │
             ├──► [feature/agent-prompt-runner]
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

### Phase 3: Safe Read-Only Library Access Utility (`feature/library-reader`)

* **Objective**: Provide working code helpers to allow safe discovery and retrieval of files from the local sub LLM-Wiki.
* **Deliverables**:
  * Safe methods `list_library_files()` and `read_library_file(relative_path)` in `src/library.py`.
  * Strict path resolution containment validation using `Path.is_relative_to()`.

### Phase 4: Sandbox Creation Utilities & Logging (`feature/sandbox-manager`)

* **Objective**: Implement utilities to dynamically instantiate isolated run directories inside `sandbox/` and log historical metadata.
* **Deliverables**:
  * Working `SandboxManager` class within `src/sandbox.py`.
  * Methods to create a run directory (e.g., `sandbox/run-YYYYMMDD-HHMMSS/`) and seed it with introductory instructions (`instructions.txt`).
  * Metadata registries logging runs.

### Phase 5: Writable Sandbox Agent Runner (`feature/agent-prompt-runner`)

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
