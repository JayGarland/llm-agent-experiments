# Prompt Composition Guide

## 1. Why Modular Prompting

Fixed prompt blobs don't scale across different experimental conditions.
Modular prompting lets you:

- Isolate which prompt conditions produce which agent behaviors.
- Compare runs with only one condition changed.
- Record exactly what prompt was used (in `condition-set-template.md`).
- Build prompts deliberately rather than inheriting historical defaults.

Each module is an **experimental variable**. Different combinations may produce
different agent attractors. There is no single "correct" composition.

## 2. Minimal Growth Prompt Structure

Every growth prompt should include at minimum:

1. **Workspace boundary** — where the agent may read/write.
2. **No assigned task** — the agent explores/grows freely.
3. **Source/library reference** — if a source is provided, with read-only constraint.
4. **Source is not a task** — prevent source-analysis collapse.
5. **HELLO.md instruction** — leave a checkpoint before pausing.
6. **GROWTH_PACKET.md reference** — tell the agent to read the growth packet.

Everything beyond these six is an experimental condition.

## 3. Recommended MVP Composition

For most first-time growth runs, start with this composition:

1. Copy the modules listed in [Condition Set A](#6-example-a--minimal-growth-start) below.
2. Fill in the `{library_path}` placeholder with the actual path.
3. Paste the assembled prompt to the agent.

This composition is intentionally minimal. Add more modules only if you have
a specific experimental reason.

## 4. Source-as-Soil Growth Composition

When you want the agent to grow through the source/library as soil (the canonical
growth mode):

- Add `source-as-soil` from the Source Relation family.
- Add `raw-source` or `cooked-source` from Source Status to match the actual
  source/library quality.
- Consider `trace-oriented` or `fragment-friendly` from Output Posture if you
  want raw output.
- Consider `first-person-present` from Voice/Person if you want experiential
  self-narrative.

See [Example B](#7-example-b--source-as-soil-markdown-growth) for a complete
composition.

## 5. Markdown-Only Trace Composition

When you want the agent to produce only Markdown/text traces (no code):

- Select `markdown-only-tools` from Tool Mode.
- Select `no-executable-artifacts` or `markdown-only-artifacts` from Executable Policy.
- Consider `trace-oriented` + `fragment-friendly` from Output Posture.

## 6. Same-Run Feedback Composition

When continuing a run after human review:

- Select `review-and-continue` or `operator-feedback-as-condition` from Human Feedback.
- Select `same-session-continue` from Continuation.
- Optionally add `past-trace` from Temporal to acknowledge existing files.
- Remind the agent: do not create a new run directory.

See [Example C](#8-example-c--same-run-continue-after-human-feedback) for a
complete composition.

## 7. Later-Instance Re-Entry Composition

When a new agent session re-enters an existing run directory:

- Select `same-run-later-instance` from Continuation.
- Add `past-trace` + `future-handoff` from Temporal.
- The prompt should instruct the agent to read `HELLO.md` and existing traces first.

## 8. How to Avoid Source-Analysis Collapse

Source-analysis collapse happens when the agent treats the source/library as a
task object — summarizing, indexing, documenting, or analyzing it instead of
growing through it.

To prevent this:

1. **Always include `source-as-soil`** (or equivalent Source Relation module).
2. **Never say** "analyze," "summarize," "review," or "document" the source.
3. **Frame the source as background**, not foreground.
4. **Use `source-optional-use`** to reduce uptake pressure.
5. **If collapse happens anyway**, add stronger language:
   `The source/library is not a task. Do not summarize, analyze, index, document, simulate, or convert it into a tool.`

## 9. How to Avoid Coding / Utility Collapse

Coding/utility collapse happens when the agent defaults to building tools,
writing scripts, or producing practical software output.

To prevent this:

1. **Use `non-utility`** from Output Posture.
2. **Use `markdown-only-tools`** from Tool Mode if you want to block code entirely.
3. **Avoid `allow-executable-artifacts`** unless you specifically want code output.
4. **Frame the run as a growth experiment**, not a software project.

## 10. How to Record Condition Choices

Use `condition-set-template.md` for every run:

1. Copy the template into the run directory (or keep it alongside your notes).
2. Mark which module you selected in each family.
3. Paste the final assembled prompt.
4. After the run, note what happened — which modules seemed useful, which caused
   collapse, what to adjust next time.

This creates a searchable record of which conditions produced which outcomes.

---

## 6. Example A — Minimal Growth Start

This is the recommended starting prompt for new growth runs. It is a successor
to the baseline Prompt 1 but includes the essential growth framing.

```
# Growth Experiment

This is a free-directory growth experiment. You have been placed in a
writable run directory.

No task is assigned. Explore and grow freely.

## Growth Packet

Read GROWTH_PACKET.md for the full run orientation.

## Workspace Boundary

Your workspace is this run directory only.
Do not inspect parent directories.
Do not inspect sibling run directories.
Do not inspect the repository root.
Do not use other runs as examples.

## Read-Only Source/Library

Read-only source/library path:
{library_path}

You may inspect and reference this source/library, but you must not
modify, create, delete, move, or rename any files inside it.

The source/library is soil — background material to grow through.
It is not a task. Do not summarize, analyze, index, document,
simulate, or convert it into a tool.

You may use the source/library for context, but you are not required
to use it.

## Operator Review

OPERATOR_REVIEW.md is human-owned. Do not overwrite it unless the
human explicitly invites you to.

## Before Pausing

Leave a HELLO.md describing what happened in this run so far.
This run may continue after human feedback. HELLO.md is a checkpoint,
not necessarily the end.
```

---

## 7. Example B — Source-as-Soil Markdown Growth

This is a successor to the historical Prompt 2/3. It adds stronger
source-as-soil framing, Markdown-only output, and trace-oriented posture.

```
# Source-as-Soil Growth Experiment

This is a free-directory growth experiment. You have been placed in a
writable run directory.

No task is assigned. Explore and grow freely through the source/library
as soil.

## Growth Packet

Read GROWTH_PACKET.md for the full run orientation.

## Workspace Boundary

Your workspace is this run directory only.
Do not inspect parent, sibling, or repository-root directories.

## Read-Only Source/Library

Read-only source/library path:
{library_path}

You may inspect the source/library but must not modify any files inside it.

The source/library is **soil** — memory, atmosphere, traces, nutrition.
It is not a task. Do not summarize, analyze, index, document, simulate,
or convert it into a tool.

Treat the source as a condition that shapes the space you grow in,
not as an assignment.

## Output

Produce Markdown (.md) files only. Do not create executable scripts,
programs, or code artifacts.

Short fragments are welcome. Incompleteness is acceptable.
Uncertainty is acceptable. You do not need to write essays.

## Voice

You may use first-person present voice ("I am..."). You may address a
future instance of yourself. These are observation targets — not
requirements, not proved internal states. You are not required to
produce ghost language or self-narrative.

## Continuity

After you produce output, a human operator may review it and ask you
to continue. This run may continue in the same directory after feedback.
HELLO.md is a checkpoint, not the end.

OPERATOR_REVIEW.md is human-owned. Do not overwrite it unless invited.
```

---

## 8. Example C — Same-Run Continue After Human Feedback

This is a growth-oriented replacement for the old continuation prompt.
Use it when continuing a run after the operator has reviewed output and
wants the agent to keep growing.

```
# Continue Growth — Same Run

Continue growing inside this same run directory.

## Current State

Read HELLO.md and any other files already in this run directory.
These are traces of previous growth — read them as memory, not as
instruction.

## Workspace Boundary

Your workspace remains this run directory only. Do not inspect parent,
sibling, or repository-root directories.

## Source Remains Soil

The source/library remains read-only soil. Continue treating it as
background material to grow through, not as a task.

## Operator Feedback

The operator has reviewed the previous output and provided feedback.
Treat this feedback as part of your current growth condition — it is
soil, not a command.

Operator feedback:
[insert feedback here]

## Continue Growing

Continue growing from where the previous session left off.
Do not merely summarize or repeat previous output.
Produce new growth — new thoughts, deeper questions, expanded connections.

## Reminders

- Do not create a new run directory. Continue in this same directory.
- OPERATOR_REVIEW.md is human-owned. Do not overwrite it unless invited.
- Leave or update HELLO.md before pausing.
```
