Plan for GitHub Copilot Implementation

This plan outlines a continuous roadmap that GitHub Copilot will follow in VS Code to build an experiment framework inspired by the Karpathy‑style “free‑directory” agent experiment. The goal is to let an AI agent operate in a sandbox directory with read‑only access to a local sub LLM‑Wiki (library), freely explore and leave artefacts (e.g., HELLO.md) for future runs. The plan stresses incremental steps; Copilot should implement each phase sequentially and commit the results as separate branches or pull requests. The first milestone is to establish a generic base branch from which all future experiments will derive.

Evidence of current capability: GitHub’s own changelog (Sept 2025) notes that when assigning an issue to a Copilot coding agent you can choose which repository and pick a starting branch. We leverage this flexibility by creating a dedicated base branch for experimentation.

1 Repository and base branch setup
Create a new GitHub repository for the experiment framework (e.g., llm-agent-experiments). Include a short description and license (MIT or Apache‑2.0).
Add an initial commit on a new branch named base (or foundation). Set this branch as the default repository branch; this will serve as the generic starting point for all future work. According to GitHub’s changelog, Copilot assignments can be started from any branch, so using a base branch allows downstream branches to derive from a clean slate.
Create core directories on the base branch:
docs/ – high‑level documentation and design rationale.
src/ – source code (Python scripts and modules).
sandbox/ – empty folder; actual runs will create subfolders here.
library_sample/ – optional folder containing a minimal example of a read‑only sub LLM‑Wiki (structure only, no proprietary content) to illustrate expected structure.
.github/ – configuration files (issue templates, workflows, etc.).
Add a .gitignore file tuned for Python and VS Code projects (ignore virtual environment folders, .pytest_cache, etc.).
Write an initial README.md explaining:
The purpose of the repository (to host experiments where an AI agent freely explores a sandbox with read‑only access to a knowledge library).
High‑level overview of folder structure and how to derive new branches.
How to set up the development environment (Python 3.11+, recommended virtual environment, and recommended VS Code extensions).
Document project goals in docs/overview.md, including the philosophical background (Karpathy’s experiment) and constraints (read‑only source, writable sandbox, leaving artefacts for future agents).
2 Define environment configuration
Add a pyproject.toml or requirements.txt in the base branch specifying dependencies (e.g., watchdog for file monitoring, pydantic for data models, click for CLI scripts). Keep dependencies minimal to avoid bloat.
Create a src/config.py module that defines configurable paths:
READ_ONLY_LIBRARY_PATH – absolute path to the local sub LLM‑Wiki; to be set by the user (not packaged in the repository).
SANDBOX_ROOT – root directory where run‑specific sandboxes will be created (e.g., sandbox/).
Other optional settings (e.g., naming scheme for runs, time stamp format, maximum runs to keep).
Provide a setup.sh script or Makefile target that creates a virtual environment, installs dependencies, and initializes the sandbox directory.
Update README.md to explain how to run the setup script and how to configure the environment variables or configuration file.
3 Implement sandbox creation utilities
In src/sandbox.py, implement a SandboxManager class with methods to:
Create a new run directory under SANDBOX_ROOT using a timestamp or UUID (e.g., run-20260606-0001).
Populate the run directory with any necessary initial files (e.g., an empty HELLO.md or a prompt.txt describing the experiment instructions). Do not copy the read‑only library; only point to it via configuration to avoid duplication.
Record metadata for each run (e.g., run id, creation time, path, reference to library path) in a log (CSV or JSONL) under docs/ for reproducibility.
Write unit tests (using pytest) in a tests/ directory to verify that:
New run directories are created correctly.
Metadata logging works as expected.
The read‑only library path is not modified during run creation.
Expose a simple CLI (e.g., python -m src.sandbox create-run) for developers or Copilot to create a new sandbox when needed.
4 Write the free‑exploration agent harness
In src/agent.py, define an AgentRunner class responsible for executing a free‑form exploration:
Initialize with a sandbox path and configuration, giving the agent read‑only access to the configured library path.
Present the free prompt to the agent: instruct the AI to explore freely within the sandbox directory, with read‑only access to the library, leaving a HELLO.md summarizing what it did, what influenced its exploration, and any suggestions for continuation.
Run the model invocation (e.g., call to openai.ChatCompletion or other provider). Keep this stub generic; actual API calls will be added in derived branches.
Write outputs returned by the agent into the sandbox directory (e.g., create files or scripts). Ensure that the agent never writes outside the sandbox.
Leave TODO markers where future branches will implement concrete agent calls, error handling, and security checks.
Update documentation to describe how AgentRunner should be extended in downstream branches to connect to specific LLM providers (OpenAI, Anthropic, etc.).
5 Provide guidelines for read‑only library access
Create a docs/library-usage.md that explains how the AI can reference the local sub LLM‑Wiki:
The library path is passed as context to the agent, but the agent must not modify any files within it.
Describe the expected structure (e.g., index.md, current_state.md, trace.md, notes/, raw/), without including actual proprietary content.
Encourage agents to quote or summarize relevant information when exploring, while leaving the original library untouched.
Include helper functions in src/library.py to safely read files from the library (e.g., read_file(relative_path)) and to list available files. These helpers should enforce read‑only behaviour by raising an exception on any write attempt.
Document how future branches can extend these helpers to perform semantic search or embed retrieval (e.g., hooking up to an embedding model) if needed.
6 Outline future tasks (not in base branch)

The base branch should only include scaffolding, configuration, and safe utilities. After the base branch is stable, subsequent branches can implement more advanced features. Document these as issues or TODOs in docs/roadmap.md, for Copilot to address incrementally:

Agent integration: Connect AgentRunner to a real LLM API (OpenAI, Anthropic, Claude, etc.) and implement streaming of agent outputs into files.
Watcher/trigger system: Use the watchdog library to watch for changes in the read‑only library (e.g., index.md updates). When changes occur, automatically create a new sandbox run via SandboxManager and invoke AgentRunner.
Experiment logging: Implement richer logs for each run, including agent prompts, responses, and environment metadata. Provide utilities to aggregate and analyse these logs.
Security and sandboxing: Explore OS‑level controls to ensure the agent cannot escape the sandbox (e.g., using Docker or chroot). Implement tests to verify that file writes outside the sandbox are blocked.
Evaluation and analysis: Add scripts to analyse the artefacts produced by different runs (e.g., detect emergent themes, self‑narrative patterns, or references to the read‑only library). Incorporate evaluation metrics if desired.
Branch policies: Define branching and merging rules. For example, each new feature or experiment goes into a separate feature branch derived from base; after review, results can be merged back into base or a release branch.
7 How to derive new branches

Since GitHub now allows choosing a starting branch for Copilot assignments, downstream contributors should:

Checkout the base branch and pull the latest changes.
Create a new branch from base (e.g., feature/agent-openai, feature/watcher or experiment/run-20260606). Use descriptive names that reflect the purpose.
Implement the desired feature or experiment following the guidelines in docs/roadmap.md.
Write tests and update documentation accordingly.
Open a pull request targeting base and request review. Merge only after passing tests and meeting repository guidelines.

This roadmap should provide GitHub Copilot with a clear sequence of tasks. The first stop is to implement Phase 1—create the repository, set up the base branch with the described structure, commit the initial files, and document the high‑level purpose. Subsequent phases can then be tackled in order, allowing the project to evolve into a robust, reproducible experimental framework.