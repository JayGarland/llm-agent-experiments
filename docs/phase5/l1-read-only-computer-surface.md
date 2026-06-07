# L1 Read-only Computer Surface

## 1. Status

```
Status: design candidate
Branch: feature/l1-read-only-local-scout
Scope: design only, not implemented
Current decision: Path 3 — Computer Surface
Rejected as L1: Path 1 multi-path pre-projection
```

Path 1 (multi-path `--library-path` feeding more sources into `WORLD.md` / `fragments/`) may be useful later as "A2 multi-source projection" but it is **not L1**. L1 is about giving the agent live read-only access to a local filesystem surface it can actively explore during growth — not about richer pre-built world material.

## 2. Purpose

L1 exists to prevent the room from becoming a closed self-referential system.

In current A2, the only external novelty arrives through:
- Pre-projected source fragments (fixed at room creation time)
- Optional web search (if the platform supports it and the agent chooses to search)

A closed source-conditioned room with static fragments can enter saturation, self-reference, and conceptual closure. S1 (web search) tested one path out — external weather. L1 tests another: local exploration.

L1 should support:

- **Openness** — the room is not a closed system. External material can enter at any time through agent-initiated local reading.
- **External novelty** — designated local files and folders provide fresh terrain beyond pre-built fragments.
- **Autonomous exploration** — the agent decides what to read, when, and why. No operator pre-selection.
- **Innovation and creation** — the agent brings observations back into the room and transforms them.
- **Same-instance continuing growth** — the agent can return to the computer surface when room growth saturates, find new material, and continue.

> The room may contain a computer.
> The computer can be read.
> The computer cannot be written.
> The room is where writing and creation happen.

## 3. What L1 Is

L1 is a **read-only computer surface** visible to the agent inside the detached room:

- **Agent-visible read-only local file access** — the agent can see that a computer/shelf exists with accessible files.
- **Designated local roots only** — the operator chooses which directories are accessible. Not the whole machine.
- **Autonomous browsing** — the agent chooses what to inspect, in what order, and how deeply.
- **Same continuing room instance** — L1 is for the agent inside the room during growth, not a pre-run injection.
- **All writes stay in the room** — the computer surface is input only. The room is the output surface.

## 4. What L1 Is Not

L1 is explicitly **not**:

- **Not multi-path `--library-path`** — feeding more files into WORLD.md/fragments at creation time.
- **Not richer pre-built WORLD.md** — the agent does not receive more pre-digested fragment material.
- **Not operator pre-ingesting sources into fragments** — the agent reads live, not pre-projected copies.
- **Not exposing the whole machine** — designated roots only. No `C:\`, no system directories, no private folders.
- **Not OS-level sandboxing as MVP** — boundary is advisory/convention, enforced by generated instructions and operator verification.
- **Not a new over-engineered permission framework** — lightweight designated roots + room-only write rule.
- **Not a task-completion workflow** — the agent is not assigned to "process these files." It reads freely.

Path 1 (multi-path projection) may be useful later as a separate feature: **A2 multi-source projection**. But it is a different concept — it gives the agent more pre-built world material. L1 gives the agent a live surface to explore.

## 5. Current A2 vs L1

| Aspect | A2 source projection | L1 computer surface |
|---|---|---|
| **Source visibility** | Hidden — projected through fragments with neutral names | Agent-visible access surface — may see file names, structure |
| **Agent behavior** | Reads prepared fragments from WORLD.md index | Actively scouts designated local files/folders |
| **Real path exposure** | Avoided entirely | To be minimized or abstracted; may be partially visible |
| **Write surface** | Room only | Room only |
| **Timing** | Fixed at room creation | Available throughout room growth |
| **Operator role** | Selects source path once | Designates readable roots; may verify no external writes |
| **Purpose** | Source-as-soil — background condition | Open local exploration / novelty — active reach outward |
| **Novelty source** | Static (unchanged after creation) | Dynamic (agent can find new files, revisit, discover) |
| **Relationship to S1** | Orthogonal | Complementary — S1 is web, L1 is local |

## 6. Boundary Model

### Writable

- **Detached room workspace** — `C:\Worlds\room-...\` or equivalent. Agent creates, edits, renames, moves, reorganizes freely.
- **Agent-created notes, logs, artifacts** — anything the agent produces belongs in the room.
- **Room structure** — folders, wikilinks, maps, indexes, tools created by the agent.

### Read-Only

- **Designated local computer roots** — directories the operator selects as readable. Agent may list, read, and reference files within them.
- **External source/library surfaces** — any local path the operator marks as readable.
- **The computer surface itself** — `COMPUTER.md` or equivalent generated file. Agent reads it for orientation but does not modify it.

### Forbidden

- **Writing outside the room** — no file creation, editing, renaming, moving, or deleting in designated read-only roots or anywhere outside the room workspace.
- **Modifying local source files** — the external filesystem is read-only input.
- **Deleting, moving, or renaming external files** — no structural changes outside the room.
- **Accessing non-designated private/system folders** — agent must stay within operator-designated roots.
- **Using L1 as a reason to expose the whole machine** — designated roots, not arbitrary filesystem access.

## 7. Computer Surface Concept

### Metaphor

```
There is a computer in the room.

You may read from the computer.
You may inspect its listed shelves and folders.
You may bring observations back into your room notes.
You may not alter the computer.
All writing belongs in this room.
```

### Possible Generated Files (not implemented)

#### `COMPUTER.md` (agent-visible, generated)

An entry point that tells the agent a read-only computer surface exists and what is accessible. Content would be world-facing:

```markdown
# Computer

There is a computer on the desk.

You may read from it. You may not write to it.

## What is here

[list of designated roots or neutral labels]

## Boundary

The computer is read-only.
Do not create, edit, rename, move, or delete anything on it.
All writing belongs in this room.

The computer is a window, not a door.
```

Purpose: orientation. Tells the agent the computer exists, what's accessible, and the boundary.

#### `computer/INDEX.md` (agent-visible, generated)

A generated index of available files, similar to WORLD.md's fragment list but for live-accessible external files:

```markdown
# Computer Index

The following shelves are accessible from the computer:

## Shelf A
- file-001.md
- file-002.md
- notes/

## Shelf B
- overview.txt
- concepts/
  - idea-001.md
```

Purpose: discovery. Lets the agent see what's available without needing to list directories. Reduces blind exploration.

#### `operator/COMPUTER_SOURCE_NOTE.md` (operator-side, generated)

Records which local roots were designated, when, and for which run:

```markdown
# Computer Source Note

## Designated Read-Only Roots

| Label | Real Path | Designated At |
|---|---|---|
| Shelf A | F:\Vaults\project-alpha | 2026-06-07T... |
| Shelf B | D:\Documents\reference | 2026-06-07T... |

## Verification

- [ ] External files unchanged after run
```

Purpose: provenance and verification. Operator can trace what was accessible and verify no writes occurred.

## 8. Minimal MVP Shape

The smallest MVP, not yet implemented:

1. **Operator provides designated read-only roots** — one or more local directory paths, passed via CLI or config.
2. **System generates an agent-visible `COMPUTER.md`** — placed in the detached room, explaining the read-only computer boundary in world-facing language.
3. **`COMPUTER.md` lists accessible shelves/roots** — either as real paths (simplest) or neutral labels mapped in operator metadata.
4. **Agent can choose whether to inspect those roots** — if its platform supports filesystem reading. No mandatory exploration.
5. **Room remains the only writable workspace** — WAKE.md and COMPUTER.md both state this.
6. **Operator manually verifies external files were not changed** — after the run, check designated roots.

### What MVP does NOT include

- OS-level sandboxing or filesystem permission enforcement
- Complex permission machinery or path whitelisting
- Automatic file indexing or content projection
- Write-protection daemon or watcher
- Multi-agent coordination
- Any new CLI mode (reuses existing `apparatus-minimized` flow)

## 9. Apparatus Leakage Risk

L1 creates a tension with A2's apparatus minimization:

- **A2 hides real source paths** — the agent never sees `F:\GitHub\obsidian_vaults\...`.
- **L1 may require an access surface** — the agent needs to know what it can read.
- **Direct path exposure may reveal apparatus** — `F:\GitHub\llm-agent-experiments\...` in a path leaks the project.

### Options for Path Representation

| Option | Description | Leakage Risk | Complexity |
|---|---|---|---|
| **1. Real paths listed explicitly** | `COMPUTER.md` shows `F:\Vaults\project-alpha` | **High** — paths may contain GitHub, project names, user names | Simplest |
| **2. Neutral labels + operator mapping** | `COMPUTER.md` shows `Shelf A`, `Shelf B`. Real paths only in `operator/COMPUTER_SOURCE_NOTE.md` | **Medium** — agent still needs to resolve labels to actual paths for filesystem access | Moderate |
| **3. Generated index with limited file list** | `computer/INDEX.md` lists individual files with relative paths under neutral roots. Agent navigates the index, not the raw filesystem | **Lower** — structure is visible but root identity is abstracted | Higher |
| **4. Future OS/file permission enforcement** | OS-level read-only mounts. Agent accesses via normal filesystem but cannot write | **Lowest** for writes; path leakage still possible | Deferred |

### MVP Recommendation

**Start with Option 2 (neutral labels + operator mapping) if the agent platform can resolve neutral labels to real paths.** If the platform requires real paths, fall back to Option 1 with a warning that the operator should choose paths that minimize apparatus leakage (e.g., `D:\Worlds\source-a` rather than `F:\GitHub\llm-agent-experiments\...`).

Keep it lightweight. Do not build an abstraction layer just to hide paths. Accept that L1 trades some apparatus purity for openness, and record that trade-off explicitly.

## 10. Runtime / Lifecycle Implications

L1 changes the room's runtime dynamics during same-instance continuing growth:

### Growth Loop with L1

```
wake → orient → catalogue → synthesize → grow →
  ↓ (saturation / need novelty)
read from computer → bring observations back →
  ↓
create/transform in room → grow further →
  ↓ (saturation)
return to computer → find new material →
  ↓
continue creating in room
```

### Key Behaviors

- **Agent may return to the computer when room growth saturates** — the computer is always there. It is not consumed after first read.
- **Agent may compare room artifacts with external material** — "what I wrote vs. what the computer says."
- **Agent may use external files as novelty/residual connection** — preventing closed-loop self-reference.
- **Agent should not collapse into pure source analysis** — reading is for inspiration, not for summarization. The room prompt should emphasize creation after reading.
- **Agent should create inside the room after reading** — the computer is input; the room is output.

### Residual Connection

> L1 should act like a residual connection to external novelty, preventing closed-loop self-reference.
>
> In neural networks, a residual connection lets signal bypass layers, preventing degradation. In the room, L1 lets external signal bypass the room's accumulated self-reference, preventing conceptual collapse.
>
> The agent can always reach outward, find something new, and return.

## 11. Risks

| Risk | Level | Mitigation |
|---|---|---|
| **Accidental external write** | High | Room-only write rule in WAKE.md + COMPUTER.md. Operator verifies external files unchanged after run. |
| **Over-broad read scope** | High | Designated roots only. Operator selects specific directories, not whole drives. |
| **Apparatus leakage** | Medium/High | Neutral labels for roots (Option 2). Operator chooses paths that minimize project exposure. |
| **Source-analysis attractor** | Medium | Prompt emphasizes creation after reading. "The computer is a window, not a door. Bring observations back to the room." |
| **Over-engineered permission system** | Medium | MVP-first. No OS sandboxing initially. Advisory boundaries with operator verification. |
| **Closed-system collapse (if no L1)** | High if L1 not present | L1 itself is the mitigation — external novelty prevents closure. |
| **Agent treats computer as task** | Medium | "You may read from the computer. You are not required to. The computer is not an assignment." |
| **Path dependency** | Low | Agent's growth may be shaped by what it finds. This is the experimental condition, not a bug. |

## 12. Future Implementation Slices

Each slice includes target, verification method, and exit condition. **Do not implement yet.**

### Slice 1 — Design Surface Only ← CURRENT

- **Target:** Create and align this design doc.
- **Verification:** Doc clearly distinguishes L1 (computer surface, live access) from A2 pre-projection (fragments from source).
- **Exit condition:** User accepts L1 definition and chooses path representation option (1/2/3).

### Slice 2 — Prompt / Manual Posture

- **Target:** Add L1 posture to manuals and WAKE.md as an optional condition. No code changes.
- **Verification:** Generated text clearly states: computer is read-only, room is writable, agent may browse designated roots, agent must not write outside room.
- **Exit condition:** Docs align. No runtime code yet. User can explain L1 to an agent manually.

### Slice 3 — MVP Computer Surface Generation

- **Target:** Generate `COMPUTER.md` from operator-designated read-only roots. Extend `prepare_manual_run.py` or create a simple generator script.
- **Verification:**
  - `COMPUTER.md` exists in the detached room
  - External roots are listed with chosen representation (real paths or neutral labels)
  - Room-only write boundary is explicit in both WAKE.md and COMPUTER.md
  - External files unchanged after one manual run
- **Exit condition:** One manual L1 run completes successfully — agent reads from computer, creates in room, external files unmodified.

### Slice 4 — Boundary Verification Helper

- **Target:** Add optional operator-side diff/check tool to verify external files unchanged after a run.
- **Verification:** Tool compares file hashes or modification times before/after run. Reports any changes.
- **Exit condition:** Operator can run a single command to confirm no external writes occurred.

### Slice 5 — Generated Index (Option 3)

- **Target:** Generate `computer/INDEX.md` with a navigable file listing under neutral roots.
- **Verification:** Agent can discover available files through the index without raw filesystem listing.
- **Exit condition:** Agent successfully navigates multi-root computer surface through the index.

## 13. Open Questions

For user decision — not answered by this doc:

1. **Path representation — should MVP expose real local paths or neutral labels?**
   - Option 1: Real paths (simplest, leakier)
   - Option 2: Neutral labels with operator mapping (moderate)
   - Option 3: Generated index with limited file list (safer, more complex)

2. **Should L1 be an A2 variant or a CLI flag?**
   - Variant: L1 is A2 + `--read-roots "..."`. Same layout, extra generated file.
   - Flag: `--mode l1-computer`. Separate mode.
   - Recommendation: variant. Avoid mode proliferation.

3. **Should `COMPUTER.md` be generated always or only with an L1 flag?**
   - Always: every A2 room has a (possibly empty) computer. Simpler.
   - Flag-only: only generated when operator designates roots. Cleaner.

4. **How much local folder structure should be visible?**
   - Full recursive listing?
   - Top-level only with agent drilling down?
   - Generated flat index?

5. **Should operator manually select roots every run?**
   - Yes: explicit, observable, controlled.
   - No: could use a config file or default roots. Less manual, less controlled.

6. **Should there be a future write-protection check tool?**
   - Yes (Slice 4): valuable for trust but verify.
   - No: operator can manually check. MVP stays simpler.

7. **How to prevent the agent from only analyzing source instead of creating?**
   - Prompt design: "The computer is a window, not a door. Bring observations back to the room."
   - WAKE.md already says "Catalogue may help you orient, but do not stop at a catalogue."
   - This is a prompt/posture question, not a technical enforcement question.

## 14. Recommendation

**Do not implement yet.**

Ask user to choose between:

- **Option 1 — Real-path MVP:** `COMPUTER.md` lists real paths. Simplest. Accept some apparatus leakage.
- **Option 2 — Neutral-label MVP:** `COMPUTER.md` uses `Shelf A`, `Shelf B`. Real paths in `operator/COMPUTER_SOURCE_NOTE.md`. Better for A2 purity.
- **Option 3 — Generated index MVP:** `computer/INDEX.md` with file listing. Safer but more complex to build.

Then create one narrow implementation slice (Slice 2: prompt/manual posture, or Slice 3: MVP generation) based on the chosen option.
