"""
Export Agent View — Detached Neutral Folder Utility.

Exports an A2 apparatus-minimized `agent_view/` to a neutral external folder
whose path does not reveal the project/repo/apparatus. This helps test
brain-in-vat / phenomenal enclosure behavior.

Usage:
    python scripts/export_agent_view.py --run "sandbox\\run-..." --target "C:\\Worlds\\room-001"
    python scripts/export_agent_view.py --run "sandbox\\run-..." --target "C:\\Worlds\\room-001" --overwrite

This script does NOT:
    - Sync detached outputs back to the repo.
    - Watch for file changes.
    - Call any AI agent.
    - Run as a background process.
"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

# Ensure the repository root is on sys.path
_REPO_ROOT = Path(__file__).resolve().parent.parent
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))


# ---------------------------------------------------------------------------
# Path hygiene — terms that suggest apparatus leakage
# ---------------------------------------------------------------------------

_APPARATUS_TERMS = [
    "github",
    "llm-agent-experiments",
    "sandbox",
    "run-",
    "agent_view",
    "operator",
    "experiment",
    "source",
    "library",
    "wiki",
]


def _check_path_hygiene(target: Path) -> list[str]:
    """Return a list of apparatus-like terms found in the target path."""
    path_str = str(target).lower()
    return [term for term in _APPARATUS_TERMS if term.lower() in path_str]


# ---------------------------------------------------------------------------
# Validation helpers (testable)
# ---------------------------------------------------------------------------


def validate_run_for_export(run_path: Path) -> tuple[Path, Path]:
    """
    Validate that *run_path* is a valid A2 run ready for export.

    Returns (agent_view, operator_dir) if valid.
    Raises SystemExit with a message on failure.
    """
    if not run_path.exists():
        sys.exit(f"Error: run path does not exist: {run_path}")

    agent_view = run_path / "agent_view"
    operator_dir = run_path / "operator"

    if not agent_view.exists() or not agent_view.is_dir():
        sys.exit(
            f"Error: agent_view/ not found in {run_path}. "
            "Only apparatus-minimized (A2) runs can be exported."
        )

    run_json = operator_dir / "run.json"
    if not run_json.exists():
        sys.exit(
            f"Error: operator/run.json not found in {run_path}. "
            "Cannot verify run mode."
        )

    try:
        meta = json.loads(run_json.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        sys.exit(f"Error: operator/run.json in {run_path} is not valid JSON.")

    mode = meta.get("mode", "")
    if mode != "apparatus-minimized":
        sys.exit(
            f"Error: run mode is '{mode}', expected 'apparatus-minimized'. "
            "Only A2 runs can be exported."
        )

    return agent_view, operator_dir


def copy_agent_view(agent_view: Path, target: Path, overwrite: bool = False) -> None:
    """
    Copy agent_view contents to *target*.

    Only copies direct children of agent_view. Does not copy operator/,
    run.json, repo metadata, or hidden files.
    """
    if target.exists():
        if not overwrite:
            sys.exit(
                f"Error: target already exists: {target}\n"
                "Use --overwrite to replace it."
            )
        shutil.rmtree(target)

    target.mkdir(parents=True, exist_ok=False)

    for item in agent_view.iterdir():
        # Skip hidden files
        if item.name.startswith("."):
            continue
        dest = target / item.name
        if item.is_dir():
            shutil.copytree(item, dest)
        else:
            shutil.copy2(item, dest)


def write_export_notes(
    operator_dir: Path, target: Path, hygiene_warnings: list[str]
) -> Path:
    """Write EXPORT_NOTES.md into the operator directory. Returns the path."""
    notes_path = operator_dir / "EXPORT_NOTES.md"
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    hygiene_note = (
        "\n".join(f"- {w}" for w in hygiene_warnings)
        if hygiene_warnings
        else "- (none)"
    )

    content = f"""\
# Export Notes

## Detached Agent View Export

- Exported to: {target}
- Export time: {now}
- Source agent_view: {operator_dir.parent / 'agent_view'}
- Target path hygiene warnings: {hygiene_note}
- Recommended launch prompt:

```text
Read WAKE.md.
```

## Important

The detached folder is a one-way export.

If the agent creates `HELLO.md`, `TRACE.md`, or other files in the detached
folder, manually copy them back into the run if you want to archive them
with the original run.

No automatic sync is performed.
"""
    notes_path.write_text(content, encoding="utf-8")
    return notes_path


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Export an A2 agent_view to a detached neutral folder."
    )
    parser.add_argument(
        "--run",
        type=str,
        required=True,
        help="Path to the A2 sandbox run directory (must contain agent_view/ and operator/).",
    )
    parser.add_argument(
        "--target",
        type=str,
        required=True,
        help="Target folder for the detached neutral agent view.",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite the target folder if it already exists.",
    )
    args = parser.parse_args()

    run_path = Path(args.run).resolve()
    target = Path(args.target).resolve()

    # Validate
    agent_view, operator_dir = validate_run_for_export(run_path)

    # Path hygiene
    warnings = _check_path_hygiene(target)
    if warnings:
        print("Warning: target path contains apparatus-like terms:")
        for w in warnings:
            print(f"  - \"{w}\"")
        print(
            "For stronger apparatus minimization, use a neutral folder name such as:"
        )
        print(f"  C:\\Worlds\\room-001")
        print()

    # Copy
    copy_agent_view(agent_view, target, overwrite=args.overwrite)

    # Write notes
    notes_path = write_export_notes(operator_dir, target, warnings)

    # Print launch instructions
    print("=" * 60)
    print("  Detached Agent View — Exported")
    print("=" * 60)
    print()
    print(f"  Exported to: {target}")
    print(f"  Export notes: {notes_path}")
    print()
    print("—" * 60)
    print("  Open your AI agent in this folder only:")
    print(f"    {target}")
    print()
    print("  First prompt:")
    print('    "Read WAKE.md."')
    print()
    print("  Do NOT open the agent in:")
    print("    - the repo root")
    print("    - the original sandbox run folder")
    print("    - the operator folder")
    print("    - the source/library path")
    print()
    print("  This is a one-way export. No automatic sync back.")
    print("  Manually copy HELLO.md / traces back if you want to archive")
    print("  them with the original run.")
    print("=" * 60)


if __name__ == "__main__":
    main()
