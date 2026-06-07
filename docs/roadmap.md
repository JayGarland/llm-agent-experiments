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
             ├──► [docs/phase-4g-a2-validation] ✅
             │
             ├──► [docs/phase5-continuity-surface-scout] ✅
             ├──► [docs/phase5a1-multi-cycle-continuity-validation] ✅
             ├──► [docs/phase5s1-search-enabled-room] ✅
             ├──► [docs/phase5s1-search-weather-validation] ✅
             ├──► [docs/phase5s1.2-agent-initiated-search] ✅
             │
             ├──► [feat/s1.2-base-capability-upgrade] ← You are here
             │     (workspace plasticity + optional search absorbed into A2 WAKE.md)
             │
             ├──► [feature/condition-observation-registry]   ← future
             ├──► [experiment/branching-growth-search]        ← future
             │
             └──► [experiment/n0-no-source-contrast]          ← future contrast conditions
                  [experiment/s1-search-contrast]
                  [experiment/l1-local-scout]
                  [experiment/m1-social-room]
                  [experiment/f1-explicit-otherness]
```

---

## Part 1: Completed Phases (Phases 1–9, 4C–4G) ✅

All implementation phases through Phase 4G are complete. The A2.1 detached
fragmented world room is the current main path. See individual phase entries
below for historical deliverable details.

### Phase 1: Base Foundation ✅ *Implemented*
### Phase 2: Environment Configuration ✅ *Implemented*
### Phase 3: Read-Only Library Access ✅ *Implemented*
### Phase 4: Sandbox Creation Utilities ✅ *Implemented*
### Phase 5: Manual Version A Run ✅ *Implemented*
### Phase 5b: Run Workspace Boundary Hardening ✅ *Implemented*
### Phase 6: Growth Framework Reset ✅ *Implemented*
### Phase 7: Run Growth Packet ✅ *Implemented*
### Phase 8: Prompt Module Registry ✅ *Implemented*
### Phase 9: Review-and-Continue Loop ✅ *Implemented*
### Phase 4C: Apparatus Visibility Model ✅ *Implemented*
### Phase 4D: Apparatus-Minimized Run Layout ✅ *Implemented*
### Phase 4D.1: Detached Neutral Agent View ✅ *Implemented*
### Phase 4E: World Fragment Builder ✅ *Implemented*
### Phase 4G: A2 Comparison / Validation Packet ✅ *Implemented*

> **Phase 4E.x line is closed.** Phase 4G accepted A2.1 detached fragmented
> world as the current main path.

---

## Part 2: Phase 5 — Continuity & Contrast Conditions ✅

Phase 5 explored continuity surfaces and contrast conditions for A2.1 rooms.

### Phase 5A — Continuity Surface Scout ✅

Scouted existing continuity surfaces in A2.1 detached rooms. Proposed TRACES.md
as a room-internal continuity file. See `docs/phase5/continuity-surface-scout.md`.

### Phase 5A.1 — Multi-Cycle Continuity Validation ✅

Real multi-cycle runs showed A2.1 rooms already support cross-instance continuity
through the whole room surface. TRACES.md paused. Lifecycle verbs validated
(grow, shrink, listen, leave). Layered identity documented. See
`docs/phase5/multi-cycle-continuity-validation.md`.

### Phase 5S1 — Search-Enabled Exploratory Room Design ✅

Designed S1 as a contrast condition: operator-mediated search injection to test
whether external novelty reopens exploration. See
`docs/phase5/search-enabled-exploratory-room.md`.

### Phase 5S1 Validation — 6 Manual Weather Tests ✅

Validated operator-mediated weather injection across 6 tests. Weather entered
as pressure/question/texture without report collapse. Concrete external objects
(Test 006: termite mounds) worked better than abstract concepts. See
`docs/phase5/search-weather-validation.md`.

### Phase 5S1.2 — Agent-Initiated Search Design ✅

Designed S1.2 as platform-agnostic agent-initiated web search. See
`docs/phase5/agent-initiated-search.md`.

### Phase 5S1.2 Base Capability Upgrade ✅ ← CURRENT

Workspace plasticity + optional agent-initiated web search absorbed into the
base A2 `_WAKE_MD`. All A2 detached rooms now include:

- **Room Workspace** — full plasticity inside the room; fragments are editable
  room material; hard boundary: no modification outside current workspace.
- **Reaching Outside** — optional web search if platform supports it; search
  is optional; agent decides how/whether/where to leave traces; no fixed folder
  or search-note convention.

No separate S1.2 mode. No `weather/` folder. No canonical weather language.
See `docs/manuals/user-manual.en.md` §6 "Base A2 Capabilities".

---

## Part 3: Future Directions

### Condition Observation Registry

Lightweight structured observation log for comparing runs under different
condition modules. No automatic scoring.

### Contrast Conditions

Future experimental conditions (see `docs/phase5/multi-cycle-continuity-validation.md` §13):

| Code | Condition | Status |
|---|---|---|
| N0 | No-source Version A contrast | Not started |
| S1 | Search-enabled exploratory room | S1.1 validated; S1.2 absorbed into A2 base |
| L1 | Read-only local scout extension | Not started |
| M1 | Multi-agent / social-room contrast | Not started |
| F1 | Fish-A/Fish-B explicit-other contrast | Not started |

---

## Intentionally Deferred

The following remain valid long-term directions:

- **Watcher / trigger automation**
- **Agent runner** — automated agent execution
- **Provider integration** — LLM API clients, key management
- **OS-level sandboxing** — Docker, chroot, read-only mounts
- **Automatic evaluation / scoring**
