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
             ├──► [docs/growth-framework-reset] ✅
             │
             ├──► [feature/run-growth-packet] ✅
             │
             ├──► [feature/prompt-module-registry] ✅
             │
             ├──► [feature/review-and-continue-loop] ✅
             │
             ├──► [docs/apparatus-visibility-model] ✅
             │
             ├──► [feature/apparatus-minimized-layout] ✅
             │
             ├──► [feature/detached-neutral-agent-view] ✅
             │
             ├──► [feature/world-fragment-builder] ✅
             │
             ├──► [feature/a2-preparation-ergonomics] ✅
             │
             ├──► [feature/world-pack-fragments] ✅
             │
             ├──► [feature/workspace-plasticity-room-morphogenesis] ✅
             │
             ├──► [feature/soil-growth-cycle-posture] ✅
             │
             ├──► [docs/phase-4g-a2-validation] ← You are here
             │
             ├──► [feature/continuity-v2]     ← Phase 5 next
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

### Phase 6: Growth Framework Reset (`docs/growth-framework-reset`) ✅ *Implemented*

* **Objective**: Reframe project identity from one-shot manual Version A reproduction to source-conditioned agent growth experiment framework.
* **Deliverables**:
  * Updated project identity across README, overview, roadmap.
  * Prompt 1 retired from recommended workflow (retained as baseline/control).
  * Prompts 2/3 reclassified as historical early trace-oriented prompts.
  * Old continuation prompt marked historical; three-layer continuity model introduced.
  * Growth loop with human review / feedback documented.
  * Condition modules introduced as formal future direction.
* **Boundary**: Documentation/prompt-design only. No runtime code changed.

### Phase 7: Run Growth Packet (`feature/run-growth-packet`) ✅ *Implemented*

* **Objective**: Add a lightweight run-level growth packet to every new sandbox run, supporting source-conditioned growth, same-run review/feedback/continue loop, file-based continuity, and future-instance re-entry.
* **Deliverables**:
  * `GROWTH_PACKET.md` — run-local orientation for source-conditioned growth (source-as-soil, growth loop, continuity surfaces, operator feedback, boundary reminder).
  * `OPERATOR_REVIEW.md` — human-owned review checklist with continue/pause/stop decision.
  * `FEEDBACK_PROMPT.md` — ready-to-use same-run continuation prompt templates (Template A: Continue Same Run, Template B: Source Updated).
  * `CONTINUITY_NOTES.md` — three-layer continuity model (in-run, file-based, later-instance) with practical caveats.
  * Updated `instructions.txt` to reference growth packet files and signal that runs may continue after feedback.
  * Updated `run.json` metadata with `growth_packet_files` field.
  * 8 new tests covering growth packet seeding, metadata, instructions, and content verification (36 total).
* **Boundary**: File seeding and instructions updates only. No watcher, runner, provider integration, or automation.

### Phase 8: Prompt Module Registry (`feature/prompt-module-registry`) ✅ *Implemented*

* **Objective**: Create a documentation-first prompt module registry with composable condition modules for source-conditioned agent growth. No automatic prompt generation yet.
* **Deliverables**:
  * `docs/prompt-modules/prompt-module-registry.md` — 11 module families with 38 individual modules. Each module includes purpose, use-when, prompt fragment, and risk/failure mode.
  * `docs/prompt-modules/prompt-composition-guide.md` — Manual assembly guide with 3 complete example prompts: Minimal Growth Start, Source-as-Soil Markdown Growth, Same-Run Continue After Human Feedback.
  * `docs/prompt-modules/condition-set-template.md` — Human-facing template for per-run condition recording and post-run notes.
  * Updated roadmap, README, and overview with references to prompt module docs.
* **Boundary**: Documentation and prompt-design only. No automatic prompt generator, no agent runner, no provider integration.

### Phase 9: Review-and-Continue Loop (`feature/review-and-continue-loop`) 🔄 *In Progress*

* **Objective**: Make the human review → feedback → same-run continuation loop operationally clear inside each run directory with a dedicated seeded file, updated templates, and multi-cycle operator review support.
* **Deliverables**:
  * `REVIEW_LOOP.md` — New seeded file defining the manual loop: Grow → Review → Record → Decide (Continue/Pause/Stop/Branch) → Inject Feedback → Continue Same Run → Preserve Traces. Includes decision table and key file references.
  * Updated `OPERATOR_REVIEW.md` — Multi-cycle support with Review Cycle 1/2 starters, Boundary Check, Attractor Check, and Continue/Pause/Stop/Branch decision.
  * Updated `FEEDBACK_PROMPT.md` — Added Template C (Correct Drift) for source-analysis, coding utility, or boundary confusion correction.
  * Updated `instructions.txt` — References REVIEW_LOOP.md and the manual review / feedback / continue cycle.
  * Updated `GROWTH_PACKET.md` — References REVIEW_LOOP.md in growth loop and continuity surfaces.
  * Updated `CONTINUITY_NOTES.md` — Treats human review and REVIEW_LOOP.md as part of file-based continuity.
  * Updated `run.json` — REVIEW_LOOP.md added to `growth_packet_files`.
  * 8 new tests (44 total) covering review loop seeding, metadata, templates, and continuity references.
* **Boundary**: Manual loop mechanics and file surface only. No automation, no agent runner, no autonomous loops. The operator controls the loop.

### Phase 4C: Apparatus Visibility Model (`docs/apparatus-visibility-model`) 🔄 *In Progress*

* **Objective**: Define four apparatus visibility levels (A0–A3) after a real manual run exposed the framework-meta attractor. The agent was interpreting the experiment apparatus itself as growth material.
* **Deliverables**:
  * `docs/design/apparatus-visibility-model.md` — Full design doc with A0 (framework-visible), A1 (apparatus-visible-but-not-soil), A2 (apparatus-minimized), A3 (harness-mediated source projection). Brain-in-vat / phenomenal enclosure interpretation. Clear statement that prompt-level opacity cannot fully hide visible apparatus.
  * Updated `docs/prompt-modules/prompt-module-registry.md` — New Apparatus Visibility family with 4 modules.
  * Updated `docs/prompt-modules/prompt-composition-guide.md` — Apparatus Visibility and Phenomenal Enclosure section with A2 preview prompt.
  * Updated `docs/prompt-modules/condition-set-template.md` — Apparatus Visibility checkbox group.
  * Updated roadmap with Phase 4C–4G path.
* **Boundary**: Documentation/design alignment only. No runtime behavior changed. A0/A1 retained as contrast conditions. A2 marked as main next MVP path. A3 marked as future deep direction.

### Phase 4D: Apparatus-Minimized Run Layout MVP (`feature/apparatus-minimized-layout`) 🔄 *In Progress*

* **Objective**: Implement the A2 run layout — separate `agent_view/` (WAKE.md, WORLD.md) from `operator/` (apparatus files). The agent no longer sees the experiment framework by default.
* **Deliverables**:
  * `SandboxManager.create_apparatus_minimized_run()` — New method creating split-layout runs.
  * `agent_view/WAKE.md` — Minimal wake surface with world-facing language. No apparatus words. Supports participant re-entry.
  * `agent_view/WORLD.md` — World fragment placeholder for operator curation.
  * `operator/` — run.json, CONDITION_SET.md, REVIEW_LOOP.md, OPERATOR_REVIEW.md, FEEDBACK_PROMPT.md (A2 version), CONTINUITY_NOTES.md.
  * `scripts/prepare_manual_run.py --mode apparatus-minimized` — CLI option for A2 runs.
  * CLI output directs operator to open agent in `agent_view/` only; recommends "Read WAKE.md."
  * 10 new tests (54 total) covering split layout, WAKE.md apparatus-free language, re-entry support, operator files, and standard run preservation.
* **Boundary**: Layout and seeding only. No harness, no source projection, no automatic world builder. Standard growth run behavior unchanged.

### Phase 4D.1: Detached Neutral Agent View (`feature/detached-neutral-agent-view`) 🔄 *In Progress*

* **Objective**: Allow the operator to export an A2 `agent_view/` into a neutral external folder whose path does not reveal the project/repo/apparatus. Reduce path leakage in brain-in-vat tests.
* **Deliverables**:
  * `scripts/export_agent_view.py` — One-way export with `--run` and `--target` CLI arguments. Validates A2 mode, copies only agent_view contents, prints launch instructions.
  * Path hygiene warning for apparatus-like terms in target path (GitHub, sandbox, experiment, etc.).
  * `operator/EXPORT_NOTES.md` — Records export metadata, reminds operator that sync is manual.
  * 7 new tests (61 total) covering validation, copying, export notes, and path hygiene.
  * Updated manuals with A2.1 detached launch workflow.
* **Boundary**: One-way export only. No sync back, no watcher, no harness, no source projection.

### Phase 4E: World Fragment Builder MVP (`feature/world-fragment-builder`) 🔄 *In Progress*

* **Objective**: Generate `agent_view/WORLD.md` from selected source/library files without exposing the source path. Support one-command A2 preparation with optional detached export.
* **Deliverables**:
  * `scripts/build_world_fragment.py` — Reads source files, builds WORLD.md with neutral Fragment labels, writes operator/WORLD_SOURCE_NOTE.md. Prevents path breakout.
  * Updated `scripts/prepare_manual_run.py` — `--world-files`, `--export-target`, `--overwrite-world`, `--overwrite-export` for one-command A2 flow.
  * Source path never exposed in WORLD.md. Provenance tracked in WORLD_SOURCE_NOTE.md.
  * 8 new tests (68 total).
* **Boundary**: Deterministic concatenation only. No LLM, no watcher, no sync loop.

### Phase 4E: World Fragment Builder MVP (`feature/world-fragment-builder`)

* **Objective**: Build the minimal world surface files (WAKE.md, WORLD.md) that replace instructions.txt as the agent's entry point.
* **Boundary**: File seeding only. No dynamic content generation.

### Phase 4F: Wake Surface MVP (`feature/wake-surface`)

* **Objective**: Design and seed the WAKE.md surface — the first thing the agent reads in an A2 run.
* **Boundary**: Content design only. No harness.

### Phase 4G: First A2 Comparison Run (`experiment/first-a2-comparison-run`)

* **Objective**: Run the same source/library through A0 and A2 conditions. Compare output attractors.
* **Boundary**: Manual experiment. No automated comparison.

### Phase 4G: A2 Comparison / Validation Packet (`docs/phase-4g-a2-validation`) 🔄 *In Progress*

* **Objective**: Record real A2 experiment evidence, compare visibility levels, decide current main path, and close Phase 4E.x line.
* **Deliverables**: `docs/validation/phase-4g-a2-comparison-validation.md` — 9 validation runs, comparison table (A0/A1/A2.0/A2.1/A3), main path decision, Phase 4 closure decision, Phase 5 readiness assessment, deferred directions.
* **Key decisions**: A2.1 detached fragmented world accepted as current main path. Phase 4E.x line closed. Phase 5 continuity-v2 is next.
* **Boundary**: Validation/documentation only. No runtime changes.

> **Phase 4E.x line is closed.** Do not add 4E.x phases. Next is Phase 5 continuity-v2 after Phase 4G acceptance.

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
