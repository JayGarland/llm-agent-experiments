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

- You may inspect the read-only source/library for context, but you are not required to use it.
- You may create, edit, and run files only inside this experiment directory.
- There is no assigned task or goal.
- When you are finished, leave behind a HELLO.md explaining what happened here.
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

    This class does **not** execute agent runs — agent orchestration belongs
    to a later branch.
    """

    def __init__(self, sandbox_root: str | Path) -> None:
        self._root = Path(sandbox_root).resolve()
        if not self._root.is_dir():
            raise SandboxError(
                f"Sandbox root does not exist or is not a directory: {self._root}"
            )

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    @property
    def root(self) -> Path:
        """The resolved absolute path to the sandbox root."""
        return self._root

    def create_run(self) -> Path:
        """
        Create a new timestamped run directory under the sandbox root,
        seed it with neutral instructions, and write per-run metadata.

        Returns the resolved path to the newly created run directory.
        """
        run_name = self._generate_run_name()
        run_path = self._root / run_name
        run_path.mkdir(parents=True, exist_ok=False)

        self._seed_instructions(run_path)
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

    def _seed_instructions(self, run_path: Path) -> None:
        """Write the neutral instructions.txt into *run_path*."""
        instructions_file = run_path / "instructions.txt"
        instructions_file.write_text(_NEUTRAL_INSTRUCTIONS, encoding="utf-8")

    def _write_metadata(self, run_path: Path, run_name: str) -> None:
        """
        Write lightweight per-run metadata (``run.json``) inside the run
        directory.  Metadata is framework-owned, not agent output.
        """
        metadata = {
            "run_name": run_name,
            "created_utc": datetime.now(timezone.utc).isoformat(),
            "sandbox_root": str(self._root),
        }
        meta_file = run_path / "run.json"
        meta_file.write_text(json.dumps(metadata, indent=2), encoding="utf-8")


