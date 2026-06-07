# Phase 5A — Continuity Surface Scout

## 1. Current Detached Room Shape

A complete A2.1 detached room after creation looks like:

```
C:\Worlds\room-YYYYMMDD-HHMMSS-xxxxxx\
  WAKE.md                          ← entry point
  WORLD.md                         ← entrance/index + fragment list
  fragments\                       ← world material (neutral names)
    fragment-001.md
    fragment-002.md
    ...
```

After agent growth cycles, the room may also contain:

```
  HELLO.md                         ← handoff artifact
  INDEX.md                         ← emergent index (agent-created)
  LOGS.md                          ← growth log (agent-created)
  maps\                            ← emergent folder structure
  guides\
  poems\
  glossary.md
  ...                              ← various agent-created artifacts
```

The operator-side apparatus lives in the repo:

```
sandbox/run-.../operator/
  run.json
  REVIEW_LOOP.md
  OPERATOR_REVIEW.md
  FEEDBACK_PROMPT.md
  CONTINUITY_NOTES.md
  WORLD_SOURCE_NOTE.md
  EXPORT_NOTES.md
  CONDITION_SET.md
```

---

## 2. Existing Continuity Surfaces

### Agent-Visible (Inside Detached Room)

| Surface | Source | Continuity Role |
|---|---|---|
| `WAKE.md` | Framework-seeded | Tells agent to read HELLO.md if it exists. Frames traces as "part of this place." |
| `HELLO.md` | Agent-created | Primary handoff artifact. "Leave HELLO.md for whoever may later find this place." |
| `fragments/` | Framework-seeded | World material — stable across sessions. |
| `INDEX.md` | Agent-created (emergent) | Emergent navigation aid — not guaranteed to exist. |
| `LOGS.md` | Agent-created (emergent) | Growth log — not guaranteed to exist. |
| Agent files & folders | Agent-created | All agent output persists in the room — maps, stories, glossaries, wikilinks, reorganized paths. |

### Operator-Side (Not in Detached Room)

| Surface | Source | Continuity Role |
|---|---|---|
| `CONTINUITY_NOTES.md` | Framework-seeded | Three-layer continuity model (in-run, file-based, later-instance). Contains apparatus language — not suitable for agent-visible room. |
| `OPERATOR_REVIEW.md` | Human-owned | Review notes per cycle. Contains apparatus language (source/library, boundary check). |
| `REVIEW_LOOP.md` | Framework-seeded | Manual loop guide. Contains apparatus language. |
| `FEEDBACK_PROMPT.md` | Framework-seeded | 5 templates (A–E) for continuation. A2-safe language — could be adapted for room-internal use. |
| `WORLD_SOURCE_NOTE.md` | Framework-written | Source provenance and fragment mapping. Operator-only. |

---

## 3. Missing Continuity Surfaces

### 3.1 Room-Internal Continuity File

**Gap:** No agent-visible file explicitly designed for continuity across sessions.

`HELLO.md` is the closest — but it is:
- Unstructured (any content the agent chooses).
- Written at pause/end — not designed for mid-session orientation.
- Not guaranteed to include a summary of what happened or what to do next.

A re-entering agent has no structured way to understand:
- Who was here before?
- What did they do?
- What should I know before continuing?
- Which files are traces and which are world material?

### 3.2 Structured Handoff Protocol

**Gap:** No structured handoff format.

`HELLO.md` is free-form. This is valuable for organic growth, but:
- A participant re-entering a room with 50+ files has a high cognitive load.
- There is no convention for "here are the key files to read first."

### 3.3 Continuity Across Exported Rooms

**Gap:** When a room is exported to a detached folder, there is no automatic way for the operator to track which room is which version of which growth path.

The `operator/EXPORT_NOTES.md` records the export, but:
- It is operator-side only.
- It does not follow the room if the room is copied or shared.

### 3.4 Room Growth Log / History

**Gap:** No structured growth log that tracks what happened in each cycle.

`LOGS.md` emerged organically in a real multi-cycle run, but:
- It is agent-created and not guaranteed.
- There is no framework convention for "record what you did this cycle."

### 3.5 Participant Identity and Sequence

**Gap:** No way for a re-entering agent to know:
- How many participants have been here before.
- In what order.
- What each contributed.

Current `HELLO.md` can address a future instance, but there is no convention for signing or sequencing contributions.

---

## 4. Apparatus Leakage Risks

### 4.1 CONTINUITY_NOTES.md Is Operator-Side — Correctly

The current `CONTINUITY_NOTES.md` lives in `operator/` and contains apparatus language:
- "experiment," "framework," "run directory," "GROWTH_PACKET.md," "OPERATOR_REVIEW.md"

**Risk:** Low. This file is correctly positioned and should remain operator-side.

### 4.2 FEEDBACK_PROMPT.md Is Operator-Side but A2-Safe

The A2 feedback templates avoid apparatus language — but the file header says "hidden setup."

**Risk:** Low. The operator copies templates into agent-facing prompts. The file itself should remain operator-side.

### 4.3 WAKE.md References HELLO.md — Correctly

WAKE.md frames HELLO.md and traces as "part of this place." No apparatus leakage.

**Risk:** None. This is the correct posture.

### 4.4 WORLD.md Contains No Apparatus — Correctly

WORLD.md uses soil metaphor and growth language. No apparatus leakage.

**Risk:** None.

### 4.5 Room Structure Leakage

The `fragments/fragment-001.md` naming is neutral and non-leaking.

**Risk:** None.

---

## 5. Participant Re-Entry Support

### Current Support

WAKE.md supports participant re-entry:
- "If `HELLO.md` already exists, read it first."
- "There may be traces left here before you arrived."
- "You may continue, answer, diverge, or leave your own trace."

This is sufficient for basic re-entry but does not provide:
- A structured overview of the room's current state.
- A recommended reading order.
- A distinction between world material (fragments) and previous traces.

### Validated Behavior

Real runs have validated:
- A new agent instance can read HELLO.md and existing files.
- It can follow traces and add new dimensions.
- It can update the room.
- Fresh room replication produces similar growth trajectories.

---

## 6. Room-Internal Continuity Needs

Based on real multi-cycle growth runs, the room needs:

### 6.1 A Room-Internal State File (READ_ME_FIRST.md or similar)

A file the agent can discover that tells it:
- This room has been visited before.
- Here are the key files to read (in order).
- Here is what the last participant was working on.
- Here is what might be continued.

This should use world-facing language and avoid apparatus terms.

### 6.2 Structured HELLO.md Convention (Optional)

Not a mandatory format, but a suggested convention the agent might adopt:
- Section: "What happened here"
- Section: "Key files to read"
- Section: "What could be continued"
- Section: "For whoever arrives next"

This is for the agent to adopt, not for the framework to enforce.

### 6.3 Room Growth Log Convention

Encourage (but don't require) the agent to maintain a growth log:
- One entry per growth cycle.
- What was read, what was created, what changed.

### 6.4 Participant Sequence Convention

A simple way for participants to sign their contributions:
- Each participant adds a section to a shared file or creates a trace file with their "name" (chosen by agent, not enforced).

---

## 7. What Should Remain Operator-Side Only

The following must **never** enter the agent-visible detached room:

| Item | Reason |
|---|---|
| `run.json` | Contains repo paths, mode metadata, apparatus language |
| `CONTINUITY_NOTES.md` | Contains three-layer model with apparatus language |
| `REVIEW_LOOP.md` | Contains "operator," "agent," "experiment" |
| `OPERATOR_REVIEW.md` | Human-owned review notes |
| `WORLD_SOURCE_NOTE.md` | Contains real source paths and filenames |
| `CONDITION_SET.md` | Contains apparatus visibility levels, source paths |
| `EXPORT_NOTES.md` | Contains export metadata, repo paths |
| Source/library path | Never in agent-visible files |
| Repo name, sandbox path | Never in agent-visible files |

---

## 8. What Should Be Visible Inside Detached Room

The following should be in (or added to) the agent-visible detached room:

| Item | Current Status | Recommendation |
|---|---|---|
| `WAKE.md` | ✅ Present | Keep. Already handles basic re-entry. |
| `WORLD.md` | ✅ Present | Keep. Entrance/index works well. |
| `fragments/` | ✅ Present | Keep. Neutral world material. |
| `HELLO.md` | ✅ Created by agent | Keep. Primary handoff. |
| Room state / orientation file | ❌ Missing | **Add.** A world-facing file that helps re-entering participants understand the room's state. |
| Growth log convention | ⚠️ Emergent | **Encourage.** Add gentle guidance in WAKE.md or WORLD.md. |
| Participant sequence | ❌ Missing | **Optional future.** Not critical for MVP. |

---

## 9. Minimum Viable Continuity-v2 Proposal

### Phase 5B Target: Room-Internal Orientation Surface

Add **one** new file to the A2 detached room:

```
agent_view/
  TRACES.md       ← NEW: room-internal continuity surface
```

**TRACES.md** is a world-facing file that helps re-entering participants understand the room's state. It is:

- **Framework-seeded** as a minimal placeholder.
- **Agent-editable** — participants update it as the room grows.
- **Apparatus-free** — no source/library/operator/experiment/framework language.
- **World-facing** — uses "room," "traces," "fragments," "participants," "wake," "grow."

**Suggested placeholder content:**

```
# Traces

This room has been visited before.

If you are a new participant, start with:
- READ HELLO.md
- READ WORLD.md
- Browse a few fragments that call to you

The room may have changed since it was last visited.
Traces from those who passed through before are part of this place.
```

**How TRACES.md grows:**

Participants may update it as they work:
- Add sections recording what they did.
- Update reading recommendations.
- Leave notes for the next participant.

**Why this is MVP:**

- One file. No complex protocol.
- World-facing language only.
- Builds on existing WAKE.md → HELLO.md flow.
- Does not require changes to export, build, or layout.
- Does not introduce apparatus into the room.

### Phase 5C (Optional Follow-up)

After 5B is validated in real runs, consider:
- A growth log convention (LOGS.md or TRACES.md append-only entries).
- Room state summary that can be generated from the file surface.
- Import protocol for bringing detached room output back to the run archive.

---

## 10. Recommended Phase 5B Target

**Implement a room-internal TRACES.md continuity surface.**

Scope:
1. Add `_TRACES_MD` template to `src/sandbox.py` (A2 section).
2. Seed `TRACES.md` in `agent_view/` for apparatus-minimized runs.
3. Update `WAKE.md` to reference `TRACES.md` ("If TRACES.md exists, read it after HELLO.md.").
4. Update `WORLD.md` to mention traces as part of the room.
5. Update the export script to include `TRACES.md`.
6. Update tests.
7. Update manuals.

Out of scope for 5B:
- Structured handoff protocol.
- Participant identity/sequence.
- Automatic room state summary.
- Growth log enforcement.
- Import/archive workflow.

---

## Summary

| Dimension | Finding |
|---|---|
| **Current continuity surfaces** | WAKE.md (entry, re-entry), HELLO.md (handoff), WORLD.md (index), fragments (world material), agent-created files (traces) |
| **Main gap** | No room-internal file designed for continuity orientation. HELLO.md is unstructured. Re-entering participants have no guided entry point beyond WAKE.md's basic re-entry language. |
| **Apparatus leakage risk** | Low. Operator-side files are correctly separated. Agent-visible files avoid apparatus language. |
| **Phase 5B target** | Add `TRACES.md` as a world-facing room-internal continuity surface. One file, framework-seeded, agent-editable. |
| **Phase 4 not reimplemented** | ✅ Confirmed. No changes to existing A2 mode, export, build, or layout. |
| **No automation added** | ✅ Confirmed. Scout only. No watcher, runner, provider, harness, or auto-eval. |
