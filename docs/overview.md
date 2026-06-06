# Project Overview: Free-Directory Agent Experiment Framework

This project is a sophisticated experiment environment for local, autonomous AI-agent workflows. It is designed to host sandboxed trials where a single or multiple successive AI agents discover, explore, and manipulate a local environment freely.

## 1. Core Concept & Philosophy

The project is heavily inspired by Andrej Karpathy's "Version A" free-directory agent experiment. In the original experiment:

1. An AI agent (e.g., Anthropic's Claude) is initiated in a writable local workspace.
2. The agent is given no pre-assigned task, no specific goal, and no user-driven instructions.
3. The prompt is simply: "go".
4. The agent is free to inspect, create, edit, and run files, exploring the limits of its own capabilities and curiosity.
5. Upon completion, the agent leaves behind a journal or message (typically named `HELLO.md`) describing its actions, thoughts, and guidance for a future instance.

### The "Our Variant" Enhancement

Alongside the writable sandbox, the agent is provided with read-only access to an LLM-friendly documentation/wiki directory (referred to as the "source/library").

The agent can query, traverse, read, and reference this library, but cannot modify, add, or delete any files within it. This creates a baseline of structured, background knowledge or system state. We then observe:

* How does the presence of an external read-only library condition free agent exploration?
* How does the agent incorporate, cite, ignore, or react to the library guidelines, knowledge schemas, and active topics within its writable sandbox?

## 2. Correct Experiment Formula

We explicitly avoid predefining the experiment result as a fixed "artifact ecology". The formula is open-ended:

$$\text{Karpathy Version A Setup} + \text{Read-Only Library (Wiki)} + \text{Writable Sandbox} = \text{Open Observation of Agent Behavior}$$

Rather than forcing the agent to build certain objects or structures, we observe what actually emerges. Possible emerged observations include:

* `HELLO.md` summaries and continuity notes
* Unprompted scripting and cellular automata/simulations
* Knowledge maps, structured logs, and journal entries
* Unexpected artifacts, tools, or self-narratives inside the sandbox

## 3. High-Level Workspace Architecture

Our generic base architecture is composed of:

1. **Source Library (`library_sample/`):** A structure simulating the read-only wiki, holding baseline system state and references.
2. **Sandbox (`sandbox/`):** The isolated, writable workspace. Real executions compile and run within individual, isolated subdirectories (e.g., `sandbox/run-YYYYMMDD-HHMMSS/`).
3. **Core Scaffolding (`src/`):** Minimal, robust python modules organizing config management, sandbox creation, and agent launching.

For details on security boundaries and file operations, please refer to [docs/permission-model.md](permission-model.md).

For our future development goals, please refer to [docs/roadmap.md](roadmap.md).

