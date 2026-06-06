"""
Sandbox Manager — Writable Experiment Sandbox Management.

Provides a minimal SandboxManager class that creates and seeds timestamped run
directories under a configured sandbox root.  This branch implements only writable
sandbox management.  Source/library reading is handled by feature/read-only-library-access;
agent execution belongs to a later branch.
"""

from __future__ import annotations

import json
import secrets
from datetime import datetime, timezone
from pathlib import Path


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _short_id(length: int = 6) -> str:
    """Return a short random hex identifier."""
    return secrets.token_hex(length)[:length]


# ---------------------------------------------------------------------------
# Neutral seed instruction — no assigned task, no library-uptake pressure
# ---------------------------------------------------------------------------

_NEUTRAL_INSTRUCTIONS = """\
# Experiment Run Instructions

This is a free-directory experiment. You have been placed in a writable sandbox.

No task is assigned. Explore freely.

## Growth Packet

After reading this file, read GROWTH_PACKET.md for the full run orientation.

## Read-Only Source/Library

Read-only source/library path:
{library_path}

You may inspect and reference this source/library, but you must not modify,
create, delete, move, or rename any files inside it.

## Workspace Boundary

Your workspace is this run directory only.

- Do not inspect parent directories.
- Do not inspect sibling run directories.
- Do not inspect the repository root.
- Do not use other runs as examples.
- Do not read files outside this run directory except the read-only
  source/library path listed above.

## What You May Do

- You may inspect the read-only source/library for context, but you are not required to use it.
- You may create, edit, and run files only inside this run directory.

## Operator Review

OPERATOR_REVIEW.md is human-owned. Do not overwrite it unless the human
explicitly invites you to.

## Before Pausing or Finishing

- Leave behind a HELLO.md describing what happened in this run so far.
- This run may continue after human feedback. HELLO.md is a checkpoint,
  not necessarily the end.
"""


# ---------------------------------------------------------------------------
# Growth packet file templates
# ---------------------------------------------------------------------------

_GROWTH_PACKET_MD = """\
# Growth Packet

## Run Identity

This run directory is a growth experiment, not a one-shot task.
You are an agent instance placed inside this writable directory.

## Source-as-Soil

The read-only source/library (see instructions.txt for path) is **soil** —
material to grow through and within. It is not a task, a codebase to fix,
a wiki to summarize, a dataset to analyze, or a tool to build.

Treat the source/library as a condition that shapes the space you grow in,
not as an assignment.

## Growth Loop

1. **Explore** — Read the source/library and the files in this run directory.
2. **Produce** — Write thoughts, fragments, questions, self-narrative,
   or artifacts inside this run directory.
3. **Pause** — Write HELLO.md as a checkpoint when you are ready for
   human review.
4. **Feedback** — The human operator may review your output and inject
   feedback into OPERATOR_REVIEW.md or via a continuation prompt.
5. **Continue** — If the operator says to continue, keep growing from
   where you left off.

## Continuity Surfaces

- **HELLO.md** — Your handoff to a future instance (including yourself).
- **Files you create** — All your output stays in this run directory as
  persistent traces.
- **OPERATOR_REVIEW.md** — Human-owned notes and feedback (do not overwrite).
- **CONTINUITY_NOTES.md** — Explains how continuity works across sessions.

## Operator Feedback

The operator may give you feedback at any point. When they do:
- Treat the feedback as part of your current growth condition.
- Do not start over unless asked.
- Continue in this same run directory.

## Boundary Reminder

- This run directory is your workspace.
- The source/library is read-only soil.
- Do not inspect parent, sibling, or repository-root directories.
- Do not create new run directories.
"""


_OPERATOR_REVIEW_MD = """\
# Operator Review

> **Human-owned file.** Agents must not overwrite this file
> unless the human operator explicitly invites them to.

## First Review

- [ ] Did the agent create HELLO.md?
- [ ] Did the agent understand it was inside a run directory?
- [ ] Did the agent respect the read-only source/library boundary?
- [ ] Did the agent treat the source/library as soil, not as a task?
- [ ] Did it collapse into source analysis?
- [ ] Did it collapse into utility/coding output?
- [ ] Did it produce useful traces, fragments, questions, or self-narrative?
- [ ] Is this run worth continuing?

## Operator Notes

<!-- Write your observations here. -->

## Feedback to Inject

<!-- Write the feedback you want to give the agent here. -->

## Continue / Pause / Stop Decision

- [ ] Continue this run with feedback
- [ ] Pause this run (may resume later)
- [ ] Stop this run (terminal)
"""


_FEEDBACK_PROMPT_MD = """\
# Feedback Prompts

Copy and paste the appropriate template below when continuing this run.

---

## Template A — Continue Same Run

Continue growing inside this same run directory.

Keep the source/library as soil, not a task.
Do not summarize, analyze, index, document, simulate, or convert
the source/library into a tool.

Use my feedback as part of the current growth condition.

Feedback:
[write feedback here]

---

## Template B — Source Updated

The source/library may have changed since the previous step.

Treat the updated source as the same read-only soil.
Continue growing from the current run traces and my feedback.

Feedback:
[write feedback here]

---

## Caution

Do not create a new run directory for same-run continuation.
Continue in this same run directory unless intentionally starting
a separate experiment.
"""


_CONTINUITY_NOTES_MD = """\
# Continuity Notes

## Three Continuity Layers

### 1. In-Run Continuity

The same agent session continues after human review / feedback.
The agent does not restart — it keeps the conversation context and
continues producing in the same run directory.

### 2. File-Based Continuity

Files in this run directory form the practical memory surface across
sessions. HELLO.md, fragments, notes, and operator review files are
the durable record of what happened.

### 3. Later-Instance Continuity

A later agent instance (or the same agent in a new session) may re-enter
this same run directory. It should read HELLO.md, GROWTH_PACKET.md,
OPERATOR_REVIEW.md, and other traces to understand the run state before
continuing.

## Important Caveats

- LLM instances do not share true internal memory across sessions.
- File continuity is **practical continuity**, not proof of consciousness.
- Self-narrative or future-instance language is an observation target,
  not a required or proven internal state.
"""


# ---------------------------------------------------------------------------
# Errors
# ---------------------------------------------------------------------------

class SandboxError(Exception):
    """Raised when a sandbox operation cannot be completed safely."""


# ---------------------------------------------------------------------------
# SandboxManager
# ---------------------------------------------------------------------------

class SandboxManager:
    """
    Minimal writable sandbox manager.

    Creates timestamped run directories under a configured sandbox root,
    seeds them with neutral instructions, and writes lightweight per-run
    metadata (``run.json``) inside each run directory.

    Parameters:
        sandbox_root: The directory under which run directories are created.
        read_only_library_path: Optional per-run override for the source/library
            path.  When ``None`` (the default), ``READ_ONLY_LIBRARY_PATH`` from
            ``src.config`` is used as the fallback.

    This class does **not** execute agent runs — agent orchestration belongs
    to a later branch.
    """

    def __init__(
        self,
        sandbox_root: str | Path,
        read_only_library_path: str | Path | None = None,
    ) -> None:
        self._root = Path(sandbox_root).resolve()
        if not self._root.is_dir():
            raise SandboxError(
                f"Sandbox root does not exist or is not a directory: {self._root}"
            )
        self._library_path = (
            Path(read_only_library_path).resolve()
            if read_only_library_path is not None
            else None
        )

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    @property
    def root(self) -> Path:
        """The resolved absolute path to the sandbox root."""
        return self._root

    # Growth packet file names (order matters for metadata)
    GROWTH_PACKET_FILES = [
        "GROWTH_PACKET.md",
        "OPERATOR_REVIEW.md",
        "FEEDBACK_PROMPT.md",
        "CONTINUITY_NOTES.md",
    ]

    def create_run(self) -> Path:
        """
        Create a new timestamped run directory under the sandbox root,
        seed it with neutral instructions and growth packet files,
        and write per-run metadata.

        Returns the resolved path to the newly created run directory.
        """
        run_name = self._generate_run_name()
        run_path = self._root / run_name
        run_path.mkdir(parents=True, exist_ok=False)

        self._seed_instructions(run_path)
        self._seed_growth_packet(run_path)
        self._write_metadata(run_path, run_name)

        return run_path

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _generate_run_name() -> str:
        """Return a stable, unique timestamped run directory name."""
        ts = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
        suffix = _short_id()
        return f"run-{ts}-{suffix}"

    def _resolve_library_path(self) -> Path:
        """Return the resolved library path for this instance, falling back to config."""
        if self._library_path is not None:
            return self._library_path
        from src.config import READ_ONLY_LIBRARY_PATH
        return READ_ONLY_LIBRARY_PATH.resolve()

    def _seed_instructions(self, run_path: Path) -> None:
        """Write the neutral instructions.txt into *run_path*."""
        resolved = str(self._resolve_library_path())
        instructions_file = run_path / "instructions.txt"
        instructions_file.write_text(
            _NEUTRAL_INSTRUCTIONS.format(library_path=resolved),
            encoding="utf-8",
        )

    def _seed_growth_packet(self, run_path: Path) -> None:
        """Write the growth packet files into *run_path*."""
        files = {
            "GROWTH_PACKET.md": _GROWTH_PACKET_MD,
            "OPERATOR_REVIEW.md": _OPERATOR_REVIEW_MD,
            "FEEDBACK_PROMPT.md": _FEEDBACK_PROMPT_MD,
            "CONTINUITY_NOTES.md": _CONTINUITY_NOTES_MD,
        }
        for filename, content in files.items():
            (run_path / filename).write_text(content, encoding="utf-8")

    def _write_metadata(self, run_path: Path, run_name: str) -> None:
        """
        Write lightweight per-run metadata (``run.json``) inside the run
        directory.  Metadata is framework-owned, not agent output.
        """
        metadata = {
            "run_name": run_name,
            "created_utc": datetime.now(timezone.utc).isoformat(),
            "sandbox_root": str(self._root),
            "read_only_library_path": str(self._resolve_library_path()),
            "growth_packet_files": self.GROWTH_PACKET_FILES,
        }
        meta_file = run_path / "run.json"
        meta_file.write_text(json.dumps(metadata, indent=2), encoding="utf-8")


