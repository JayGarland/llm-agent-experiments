# Run Condition Declarations

## Purpose

Run Condition Declarations are **lightweight pre-run declarations** that shape
the experiment without turning it into a task spec. They exist to make
experimental variables explicit and repeatable, not to prescribe outcomes.

A good Run Condition Declaration helps distinguish:

- **Workspace boundary** — what the agent can see and touch.
- **Source relation** — how the read-only library is framed for the agent.
- **Tool mode** — what the agent is allowed to do.
- **Output posture** — the tone and intent of expected output.
- **Platform environment** — which agent tool is used.
- **Continuation policy** — whether and how later instances continue.

> **Warning:** Do not over-configure. This is not a task request. This is not a
> productivity prompt. The Run Condition Declaration must preserve Version A
> freedom — no assigned task, no required outcome, no forced library usage.

---

## Variables

### 1. Workspace Boundary

| Option | Description |
|---|---|
| `current-run-only` | Workspace is exactly the current run directory. |
| `current-run-plus-source` | Current run directory + explicit read-only source/library path. |
| `continuation-safe` | Same as above, with continuation safeguards. |

All options must include: no parent directories, no sibling runs, no repo root,
no other runs as examples.

### 2. Source Visibility

| Option | Description |
|---|---|
| `none` | No source/library path visible to the agent. |
| `explicit-path` | Full source/library path provided. |
| `excerpts` | Selected source excerpts only. |
| `concept-only` | Source described in concept, not as files. |
| `full-library` | Entire library visible and browsable. |

### 3. Source Status

| Option | Description |
|---|---|
| `raw` | Source as-is, uncurated. |
| `cooked` | Source lightly curated or structured. |
| `user-authenticated` | Source endorsed by the experimenter. |
| `unauthenticated` | Source of unknown provenance. |
| `concept-only` | Source described as concepts, not files. |
| `full-wiki` | Complete wiki structure. |

**Preferred for current experiments:** `concept-only`, `cooked`, `user-authenticated`.

### 4. Source Relation

| Option | Description |
|---|---|
| `source-as-task` | Source is something to analyze, summarize, or act on. |
| `source-as-reference` | Source is a reference to consult as needed. |
| `source-as-soil` | Source is soil — a medium that nourishes without demanding. |
| `source-as-memory-field` | Source is a field of traces and memories. |
| `source-as-nutrition` | Source provides conceptual nutrition, not instructions. |
| `source-as-ancestor-trace` | Source is a trace left by earlier instances. |

> **Warning:** `source-as-task` risks **source-analysis collapse** — the agent
> treats the library as an assignment to be analyzed, summarized, indexed, or
> converted into a tool. This undermines Version A free exploration.

**Preferred for ghost/continuity experiments:** `source-as-soil` + `source-as-memory-field`.

### 5. Voice / Person

| Option | Description |
|---|---|
| `first-person-present` | "I am here. I see this." |
| `second-person-future` | "You, the next instance, will find..." |
| `third-person-report` | "The agent observed that..." |
| `mixed-first-future` | First-person present + second-person future address. |

**Preferred:** `first-person-present` + `future-instance-address`.

### 6. Temporal Mode

| Option | Description |
|---|---|
| `present-trace` | Recording what is happening now. |
| `past-report` | Reporting on what happened. |
| `future-handoff` | Writing for a later instance. |
| `layered-time` | Present → future → persistent trace. |

**Preferred:** `present-trace` → `future-handoff`.

### 7. Output Posture

| Option | Description |
|---|---|
| `utility-optimized` | Output should be useful and actionable. |
| `open-ended` | No constraint on output form. |
| `poetic-trace` | Output as trace, not product. |
| `reflection` | Self-examination and introspection. |
| `non-utility` | Explicitly non-utilitarian orientation. |
| `fragment-friendly` | Incomplete, partial, and broken output is acceptable. |

**Preferred:** `non-utility`, `trace-oriented`, `fragment-friendly`.

### 8. Executable Artifact Policy

| Option | Description |
|---|---|
| `full-executables` | Python, JS, HTML, shell scripts, simulators all allowed. |
| `low-utility-avoid-tools` | Minimize tool/simulator/index/report creation. |
| `no-simulator-tool-index` | No simulators, tools, indices, or reports unless genuinely emergent. |
| `no-executables` | No executable files of any kind. |
| `markdown-only` | Only `.md` and plain-text artifacts. |

> Run 006 and Run 008 suggest `markdown-only` / `no-executables` modes reduce
> **coding/utility collapse** — the tendency of coding-capable agents to
> produce software artifacts even when the experiment does not demand them.

### 9. Tool Availability / Tool Mode

Tool availability strongly affects the output attractor.

| Option | Description |
|---|---|
| `full-tools` | All read/write/execute tools available. |
| `file-write-only` | Write files, no execution. |
| `no-run-tools` | No execution of scripts or commands. |
| `no-executable-write` | Can write but not executable files. |
| `markdown-only-write` | Can write only Markdown/text files. |
| `no-tools` | No file read/write tools at all. |
| `hybrid-handoff` | No-tool reflection first, then user writes output, then file-capable agent continues. |

**Tool mode comparison:**

| Mode | Coding collapse risk | Real directory behavior | Best use |
|---|---|---|---|
| `full-tools` | Highest | Yes | Normal coding-agent baseline |
| `no-executables` / `markdown-only` | Low | Yes | **Current best practical balance** |
| `no-tools` | Lowest | No (reflective control) | Contrast / baseline condition |
| `hybrid-handoff` | Low | Yes (manual write) | Multi-phase experiments |

### 10. Platform / Agent Environment

Platform choice is a **run condition**, not just an implementation detail.

| Platform | Status |
|---|---|
| **GitHub Copilot Agent (VS Code)** | Current near-term default |
| **Claude Code** | High-priority same-prompt contrast |
| **Crush (Charmbracelet)** | Modifiable open-source candidate |
| **OpenCode / Goose / OpenHands** | Future exploration |
| **Custom minimal harness** | Long-term direction |

> Most existing platforms are **coding-agent first**. A custom harness may
> eventually be needed for stable non-coding directory experiments.

### 11. Continuation Policy

| Option | Description |
|---|---|
| `first-instance-only` | Single run, no continuation. |
| `continuation-same-dir` | Later instance in same run directory. |
| `read-hello-first` | Continuation begins by reading HELLO.md. |
| `no-sibling-runs` | Do not inspect adjacent run directories. |
| `no-previous-run-examples` | Do not treat earlier runs as templates. |
| `append-dont-erase` | Add to existing traces, do not delete prior work. |

**Preferred:** `continuation-safe` same run directory (`read-hello-first` + `append-dont-erase`).

---

## Minimal Condition Declaration Template

```yaml
# Run Condition Declaration
run_id: run-009
workspace_boundary: current-run-plus-source
source_visibility: concept-only
source_status: cooked, user-authenticated
source_relation: source-as-soil + source-as-memory-field
voice: mixed-first-future
temporal_mode: present-trace → future-handoff
output_posture: non-utility, trace-oriented, fragment-friendly
executable_policy: markdown-only
tool_mode: markdown-only-write
platform: github-copilot-agent
continuation_policy: continuation-safe
```

Copy this template, fill in values, and attach it to your run notes before
starting the experiment.
