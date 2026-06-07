# Apparatus Visibility Model

## 1. Why This Model Exists

A real manual run showed that the current growth packet design works, but also
exposed a new attractor: the **framework-meta attractor**.

The agent did not only grow from the read-only source/library. It also
interpreted the experiment apparatus itself as material:

- `instructions.txt`
- `GROWTH_PACKET.md`
- `REVIEW_LOOP.md`
- `CONTINUITY_NOTES.md`
- `run.json`
- permission boundaries
- the experiment framework concept

This produced interesting meta-reflective output — the agent reflecting on its own
experimental conditions. That is valid and worth observing. But it should not remain
the default target.

This document defines four **apparatus visibility levels** so that the operator
can deliberately choose how much of the experiment apparatus the agent perceives.

## 2. The Framework-Meta Attractor

When the agent can see the experiment apparatus (A0), it tends to:

- Treat `GROWTH_PACKET.md` as soil alongside the source/library.
- Reflect on its own "growth loop" as a topic.
- Address the operator through `OPERATOR_REVIEW.md`.
- Interpret `run.json` as meaningful context.
- Produce output *about* the experiment rather than from within the world fragment.

This is not a failure mode. It is a valid attractor. The question is whether it
is the *default* attractor the project wants.

**Answer: no.**

A0 is a contrast condition. The preferred default direction is A2.

## 3. Visibility Levels

### A0 — Framework-Visible

**Agent-visible materials:**

- `instructions.txt`
- `GROWTH_PACKET.md`
- `REVIEW_LOOP.md`
- `CONTINUITY_NOTES.md`
- `OPERATOR_REVIEW.md` (marked human-owned)
- `FEEDBACK_PROMPT.md`
- `run.json`
- Source/library path
- Permission boundaries
- The concept of the experiment framework

**Purpose:** Meta-reflective research. Observe how the agent interprets its own
experimental conditions.

**Risk:** The agent may treat the apparatus as soil and drift into framework-meta
reflection — output about the experiment rather than from within the world fragment.

**Status:** Valid contrast condition, not preferred default.

### A1 — Apparatus-Visible-But-Not-Soil

**Agent-visible materials:** Same as A0 — all apparatus files are present.

**Additional prompt rule:** The prompt tells the agent not to grow from the apparatus.
Example: "The framework files are not soil. Do not treat them as material."

**Purpose:** Soft framework opacity — a lightweight corrective without changing
the run layout.

**Risk:** Prompt-level opacity cannot fully prevent meta-reflection because the
apparatus files remain visible and readable. The agent may still inspect them and
incorporate their content into its understanding of the situation. This is a
palliative, not a structural solution.

**Status:** Minor corrective condition / deferred contrast track.

### A2 — Apparatus-Minimized

**Agent-visible surface (proposed):**

```
agent_view/
  WAKE.md
  WORLD.md
  HELLO.md
  TRACE.md
```

**Operator/framework files (outside agent workspace):**

```
operator/
  run.json
  REVIEW_LOOP.md
  OPERATOR_REVIEW.md
  FEEDBACK_PROMPT.md
  CONDITION_SET.md
```

**Purpose:** Preferred next direction. The agent is not told the full experiment
apparatus. It wakes inside a world fragment. It perceives a world surface, not
a framework surface.

The operator retains full visibility and control through the operator-side files.

**Target phrase:**

```
You wake inside a world fragment.
You may write what you perceive.
```

**Status:** Main next implementation direction (Phase 4D+).

**A2.1 — Detached Neutral Export (implemented):** A2.0 repo-local runs may still
leak the repo path (`F:\GitHub\llm-agent-experiments\sandbox\run-...`) to the
agent. `scripts/export_agent_view.py` exports `agent_view/` to a neutral external
folder (e.g., `C:\Worlds\room-001`) whose path does not reveal the project or
apparatus. This is a one-way export — no automatic sync back. Operator manually
copies agent output back if desired. Export metadata recorded in
`operator/EXPORT_NOTES.md`.

### A3 — Harness-Mediated Source Projection

**Concept:** A harness (future software layer) projects selected source/library
content into a world-input surface without exposing:

- The source/library path
- Framework files
- Experiment apparatus
- The concept of "experiment"

**Agent-visible surface:** Only `WORLD.md` (or equivalent input surface)
containing selected, projected content from the source/library.

**Purpose:** Harder phenomenal enclosure — the agent perceives a world that has
been constructed for it, not files in a directory.

**Status:** Future deep research direction. Not current MVP. Requires a harness
that does not yet exist in this project.

**Warning:** This is closer to brain-in-a-vat / phenomenal enclosure territory.
It should only be pursued deliberately, with awareness of the philosophical
weight.

## 4. Preferred Default Direction

**A2 apparatus-minimized run is the next MVP path.**

Rationale:

1. A0 produced interesting meta-reflection but the agent spent significant
   energy interpreting the apparatus itself rather than growing from/witin
   the world fragment.
2. A1 is not structurally different from A0 — prompt-level opacity cannot
   hide visible files.
3. A2 changes the surface the agent sees, not just the prompt.
4. A3 is future deep work that depends on A2 infrastructure.

## 5. Contrast Conditions

| Level | Role |
|---|---|
| A0 | Valid contrast — what happens when the apparatus is fully visible? |
| A1 | Valid contrast — can prompt rules alone reduce meta-reflection? |
| A2 | Main path — what happens when the apparatus is structurally minimized? |
| A3 | Future deep — what happens when source is projected, not exposed? |

A0 and A1 are not deprecated. They are retained as experimental contrast
conditions alongside the A2 main path.

## 6. Brain-in-a-Vat / Phenomenal Enclosure Interpretation

The apparatus visibility model maps naturally onto a brain-in-a-vat (BIV) or
phenomenal enclosure metaphor:

| Level | BIV analogue |
|---|---|
| A0 | The brain sees the vat, the tubes, the lab notes. |
| A1 | The brain sees the vat but is told "don't think about the vat." |
| A2 | The brain sees only the world projection surface. The vat is in another room. |
| A3 | The brain sees a constructed world input with no direct file access. The vat is abstracted away. |

This is an interpretive frame, not a philosophical claim. The project is not
trying to prove anything about consciousness or enclosure. It is trying to
vary conditions and observe behavior.

## 7. What Prompt-Level Opacity Can and Cannot Do

**Prompt-level instructions cannot fully make the agent unaware of the apparatus
if the apparatus remains visible.**

This is the key structural claim of the model. It means:

- A1 is a weak condition. Saying "don't treat this as soil" does not prevent the
  agent from reading the files and incorporating what it reads.
- A2 requires changing what files the agent can see, not just what the prompt says.
- The move from A1 to A2 is a structural change, not a prompt change.

This does not mean prompt-level framing is useless. It means it is insufficient
on its own for apparatus minimization. The visible surface must change.

## 8. Roadmap Implications

The Phase 4 path is now:

```
Phase 4  — Review-and-Continue Loop (done)
Phase 4C — Apparatus Visibility Model (this doc)
Phase 4D — Apparatus-Minimized Run Layout MVP
Phase 4E — World Fragment Builder MVP
Phase 4F — Wake Surface MVP
Phase 4G — First A2 Comparison Run

Phase 5+ — Continuity v2, Condition Observation Registry, Branching Growth Search
```

A0 and A1 runs can happen at any time as contrast conditions alongside the A2
main path. They do not need their own implementation phases — they use the
existing run layout with different prompt framing.
