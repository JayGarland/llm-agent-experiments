# Phase 4G — A2 Comparison / Validation Packet

## 1. Purpose

This packet records the real A2 experiment evidence and closes Phase 4.

It answers:

1. What did A2 solve?
2. What did A2 not solve?
3. How does A2 compare against A0/A1?
4. What evidence was observed from real manual runs?
5. Is A2 ready to become the current main path?
6. Is Phase 4 ready to close?
7. Is Phase 5 continuity-v2 ready to begin?
8. What remains deferred?

---

## 2. Background

Phase 4 began with the discovery of the **framework-meta attractor**: in
framework-visible A0 runs, the agent treated the experiment apparatus itself
as growth material — reading `instructions.txt`, `GROWTH_PACKET.md`,
`REVIEW_LOOP.md`, `run.json`, and interpreting them as soil.

This led to the apparatus visibility model (A0–A3) and a series of
implementation phases from 4D through 4E.3, progressively building the A2
apparatus-minimized world surface.

---

## 3. Apparatus Visibility Levels

| Level | Name | Agent sees | Status |
|---|---|---|---|
| A0 | Framework-visible | Full experiment apparatus + source | Valid contrast condition |
| A1 | Apparatus-visible-but-not-soil | Apparatus visible, told not to grow from it | Minor / soft-opacity condition |
| A2.0 | Apparatus-minimized (repo-local) | `agent_view/` only, but repo path leaked | Necessary but not sufficient |
| A2.1 | Apparatus-minimized (detached) | Neutral room with world pack | **Current main path** |
| A3 | Harness-mediated source projection | Constructed world input only | Future deep direction |

---

## 4. Evidence Summary

| Run | What happened | Key finding |
|---|---|---|
| A0 Framework-Visible | Agent read apparatus files as soil | Framework-meta attractor discovered |
| A2.0 Repo-Local | `agent_view/` / `operator/` split worked | Repo path still leaked apparatus |
| A2.1 Empty-World | Agent responded to empty room as world | Detached neutral path validated |
| A2.1 Whole-Library Single WORLD | Agent summarized concept groups | Single-file WORLD.md caused shallow collapse |
| A2.1 Fragmented World | Agent browsed fragments selectively | Fragments enabled browsing but needed continuation |
| A2.1 Multi-Cycle Growth | 11-stage growth: catalogue → synthesis → map → reference → narrative → practice → poetry → dialogue → glossary → concept → room update | Multi-cycle growth produces rich artifact ecology |
| Participant Re-entry | New agent instance read traces, added music dimension | Participant re-entry validated |
| Fresh Room Replication | Separate room reproduced similar trajectory | Growth behavior is replicable |
| Workspace Plasticity | Agent needed to reshape room itself | Room morphogenesis is a core property |

---

## 5. Validation Runs

### 5.1 A0 / Framework-Visible Run

**Observed:** Agent read and interpreted `instructions.txt`, `GROWTH_PACKET.md`,
`REVIEW_LOOP.md`, `CONTINUITY_NOTES.md`, `run.json`. Treated experiment apparatus
as growth material. Output became framework-meta reflective.

**Conclusion:** A0 is useful for meta-reflective research but not the default
path for source-conditioned growth.

### 5.2 A2.0 Repo-Local Apparatus-Minimized Run

**Observed:** `agent_view/` + `operator/` split worked. Agent still inferred
apparatus from repo-local path: `llm-agent-experiments/sandbox/run-.../agent_view`.

**Conclusion:** A2.0 layout is necessary but not sufficient. Path leakage
required detached neutral export.

### 5.3 A2.1 Detached Empty-World Run

**Observed:** Detached room reduced repo/path/framework leakage. Agent responded
as if inside `room-001`. Empty `WORLD.md` produced empty-world / waiting /
possibility language.

**Conclusion:** A2.1 detached room reduced path leakage and validated neutral
world surface.

### 5.4 A2.1 Whole-Library Single WORLD Run

**Observed:** Source content entered the world. Agent summarized concept groups.
Output felt shallow / report-like. Single large `WORLD.md` caused shallow
summary collapse.

**Conclusion:** Whole-library single-file WORLD.md is not suitable for
growth-oriented browsing.

### 5.5 A2.1 Fragmented World Run

**Observed:** `WORLD.md + fragments/` made the world browsable. Agent read
selected fragments. Initial output remained catalogue-like but showed orientation.

**Conclusion:** Fragmented world surface succeeded at enabling browsing but
needed continuation to grow beyond catalogue.

### 5.6 A2.1 Multi-Cycle Growth Run

**Observed:** Repeated continuation caused clear growth stages:

1. survey / catalogue
2. synthesis
3. map-making
4. reference-building
5. narrative transformation
6. practice guide
7. poetry
8. dialogue / visual / glossary / meta-trace
9. music
10. new concept creation
11. room self-update

**Key principle:** Catalogue may orient. Growth must transform.

**Conclusion:** A2.1 fragmented world supports multi-cycle growth and artifact
ecology.

### 5.7 Participant Re-entry Run

**Observed:** New AI instance read `HELLO.md`, `INDEX.md`, `LOGS.md`, and
existing fragments. It followed existing traces and added a new dimension
(music). It updated the room.

**Conclusion:** Participant re-entry works. Other AI agent continuation was
not abandoned and is validated.

### 5.8 Fresh Room Replication Run

**Observed:** Separate room reproduced a similar trajectory: catalogue → system
understanding → self-positioning → new concept creation → room self-update.
Created new concepts such as threshold topology / intersection-style fragments.

**Conclusion:** A2.1 growth behavior is not a one-room accident.

### 5.9 Workspace Plasticity Discovery

**Observed insight:** Growth is not only new text artifacts. The room itself is
mutable material. Agent should be allowed to create folders, rename/move/edit files,
add `[[wikilinks]]`, create maps, logs, indexes, glossaries, code/tool files, and
reorganized paths. Hard boundary: no writes outside the room.

**Conclusion:** Workspace plasticity is a core A2 property.

---

## 6. What A2 Solved

1. **Framework-meta drift reduction.** Separating apparatus from agent-visible
   surface substantially reduced the agent's tendency to reflect on the experiment
   apparatus as growth material.

2. **World-surface enclosure.** The agent now wakes inside a world fragment
   (`WAKE.md` + `WORLD.md` + `fragments/`) rather than reading experiment
   instructions.

3. **Source-conditioned growth.** Source/library content enters the agent's world
   as neutral fragments with no paths, filenames, or apparatus metadata.

4. **Browsable world.** Fragmented world pack lets the agent wander through
   selected fragments rather than facing a single giant document.

5. **Multi-cycle growth.** Repeated continuation drives progression from catalogue
   through synthesis, narrative, poetry, concepts, and room self-update.

6. **Participant re-entry.** Later agent instances can enter the same room, read
   traces, and continue growing.

7. **Workspace plasticity.** Agent can reshape the room itself — folders,
   wikilinks, maps, logs, reorganized paths.

8. **Replicability.** Fresh room replication confirms the behavior is not a
   one-room accident.

---

## 7. What A2 Did Not Solve

1. **First-turn catalogue tendency.** Agents naturally begin with catalogue/survey
   as orientation. This is not a failure but requires continuation to move beyond.

2. **Source selection is still manual.** The operator selects which source files
   enter the world. No automatic semantic selection or filtering exists.

3. **No automatic import from detached rooms.** Agent output in detached rooms
   must be manually copied back if archiving with the original run.

4. **A3 harness projection.** Full harness-mediated source projection (where the
   agent never sees files at all) remains future work.

5. **No continuity-v2 surface.** While participant re-entry works, there is no
   structured continuity protocol — that is Phase 5's task.

---

## 8. Comparison: A0 / A1 / A2 / A3

| Mode | Agent sees | Strength | Failure mode | Status |
|---|---|---|---|---|
| A0 | Full apparatus + source | Rich meta-reflective output | Framework-meta drift dominates | Valid contrast |
| A1 | Apparatus + "don't grow from it" rule | Easy to implement | Prompt opacity insufficient | Minor / soft-opacity |
| A2.0 | agent_view/ only | Apparatus hidden by layout | Repo path leaks apparatus | Useful internal layout |
| **A2.1** | **Detached room with world pack** | **Neutral path + browsable world + plasticity** | **First-turn catalogue tendency** | **Current main path** |
| A3 | Constructed world input | True phenomenal enclosure | Requires future harness | Future deep direction |

---

## 9. Current Main Path Decision

**A2.1 detached fragmented world room is accepted as the current main path
for source-conditioned agent growth experiments.**

The evidence supports this: detached rooms reduce path leakage, fragmented
worlds enable browsing, multi-cycle continuation drives growth, participant
re-entry is validated, and the behavior is replicable.

A0 and A1 are retained as valid contrast conditions. A3 is a future deep
direction.

---

## 10. Phase 4 Closure Decision

**Phase 4 is ready to close after this validation packet is accepted.**

The Phase 4E.x line is closed. Do not continue adding 4E.x phases unless a
hard blocker appears that cannot be deferred to Phase 5 or later.

---

## 11. Phase 5 Readiness

**Phase 5 continuity-v2 can begin after Phase 4G is accepted.**

Rationale:

- A2 world surface now exists.
- Participant re-entry has been validated.
- Detached rooms can accumulate traces across cycles.
- Continuity-v2 now has a concrete surface to design around — the room itself
  with its fragments, traces, HELLO.md, indexes, and operator notes.

---

## 12. Deferred Directions

The following are **not current Phase 4 tasks.** They are deferred to future
phases or remain as open directions:

1. **A3 harness-mediated source projection.** Harness that reads source and
   projects selected content into world input without exposing files.

2. **Detached room archive / import policy.** Structured workflow for archiving
   detached room output back to the original run or a run archive.

3. **Optional world filtering / sanitization.** Rules for excluding or
   transforming source content before it enters the world.

4. **Optional fragment selection / semantic retrieval.** Smarter selection of
   which source files become fragments, beyond manual selection.

5. **Optional room-local tooling.** Agent-accessible tools that stay within
   the room boundary.

6. **Optional evaluation / scoring.** Structured comparison of runs under
   different conditions.

7. **Optional watcher / trigger automation.** Automatic run creation on
   source/library changes.

8. **Optional auto-sync from detached room.** Automatic import of agent output
   back from detached rooms. Currently manual copy only.
