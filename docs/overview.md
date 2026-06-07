# Project Overview: Source-Conditioned Agent Growth Experiment Framework

This project provides a foundation for **open-ended agent growth experiments**.
Agents operate in writable run directories with read-only source/library access
(source-as-soil), human review / feedback, and multi-layered file-based
continuity surfaces.

The project is transitioning from an early manual Version A reproduction into
a **source-conditioned agent growth experiment framework**.

## 1. Core Concept & Philosophy

The project is heavily inspired by Andrej Karpathy's "Version A" free-directory agent experiment. In the original experiment:

1. An AI agent (e.g., Anthropic's Claude) is initiated in a writable local workspace.
2. The agent is given no pre-assigned task, no specific goal, and no user-driven instructions.
3. The prompt is simply: "go".
4. The agent is free to inspect, create, edit, and run files, exploring the limits of its own capabilities and curiosity.
5. Upon completion, the agent may leave behind a journal or message (typically named `HELLO.md`) describing its actions, thoughts, and guidance for a future instance.

### The "Our Variant" Enhancement

Alongside the writable sandbox, the agent is provided with read-only access to an LLM-friendly documentation/wiki directory (referred to as the "source/library").

The agent can query, traverse, read, and reference this library, but cannot modify, add, or delete any files within it. This creates a baseline of structured, background knowledge or system state. We then observe:

* How does the presence of an external read-only library condition free agent exploration?
* How does the agent incorporate, cite, ignore, or react to the library guidelines, knowledge schemas, and active topics within its writable sandbox?

## 2. Experiment Formula

The project is moving from the original observation formula to a growth-oriented one.

**Original formula (v0.1, historical):**

$$\text{Karpathy Version A Setup} + \text{Read-Only Library (Wiki)} + \text{Writable Sandbox} = \text{Open Observation of Agent Behavior}$$

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

The experiment is not a one-shot observation. It is a **growth loop**:
create run → choose condition → launch → let it grow → human review →
feedback / adjust → continue same run → pause / handoff → later re-entry.

## 3. High-Level Workspace Architecture

Our generic base architecture is composed of:

1. **Source Library (`library_sample/`):** A structure simulating the read-only wiki, holding baseline system state and references.
2. **Sandbox (`sandbox/`):** The writable workspace layout. Operational execution runs and dynamic creation occur in downstream feature branches.
3. **Core Scaffolding (`src/`):** Non-operational structural layout of configurations, sandbox managers, and agent execution stubs.

Present boundaries in the base branch are advisory/interface-level only. OS-level containment and secure locking mechanisms are deferred to future work.

For details on security boundaries and file operations, please refer to [docs/permission-model.md](permission-model.md).
For our future development goals, please refer to [docs/roadmap.md](roadmap.md).

For composing experimental prompts from condition modules, see:
- [Prompt Module Registry](prompt-modules/prompt-module-registry.md)
- [Prompt Composition Guide](prompt-modules/prompt-composition-guide.md)
- [Condition Set Template](prompt-modules/condition-set-template.md)

For the apparatus visibility model (how much of the experiment framework the agent can see), see:
- [Apparatus Visibility Model](design/apparatus-visibility-model.md)

For the Phase 4 A2 validation evidence and current main path decision, see:
- [Phase 4G A2 Comparison / Validation Packet](validation/phase-4g-a2-comparison-validation.md)

For Phase 5 — continuity, search, and local scout contrast conditions — see:
- [Phase 5 docs](phase5/)
- [User Manual §6 — Base A2 Capabilities](manuals/user-manual.en.md)
