"""
Build World Fragment — Generate agent_view/WORLD.md from source files.

Reads selected files from the read-only source/library and writes
agent_view/WORLD.md with world-facing content. Does NOT expose the
source path, wiki path, or apparatus in the agent-visible WORLD.md.

Provenance is recorded in operator/WORLD_SOURCE_NOTE.md.

Usage:
    python scripts/build_world_fragment.py --run "sandbox\\run-..." --files "index.md" "overview.md"
    python scripts/build_world_fragment.py --run "sandbox\\run-..." --files "index.md" --overwrite

This script does NOT:
    - Summarize with an LLM.
    - Watch the source for changes.
    - Run the AI agent.
    - Sync detached outputs.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

# Ensure the repository root is on sys.path
_REPO_ROOT = Path(__file__).resolve().parent.parent
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))


# ---------------------------------------------------------------------------
# Validation / path helpers
# ---------------------------------------------------------------------------


def validate_a2_run(run_path: Path) -> tuple[Path, Path, str]:
    """
    Validate *run_path* is an A2 run and return
    (agent_view, operator_dir, library_path).
    Exits on failure.
    """
    if not run_path.exists():
        sys.exit(f"Error: run path does not exist: {run_path}")

    agent_view = run_path / "agent_view"
    operator_dir = run_path / "operator"
    run_json = operator_dir / "run.json"

    if not agent_view.is_dir():
        sys.exit("Error: agent_view/ not found. Only A2 runs supported.")
    if not run_json.exists():
        sys.exit("Error: operator/run.json not found.")

    meta = json.loads(run_json.read_text(encoding="utf-8"))
    if meta.get("mode") != "apparatus-minimized":
        sys.exit(
            f"Error: run mode is '{meta.get('mode')}', "
            "expected 'apparatus-minimized'."
        )

    library_path = meta.get("read_only_library_path", "")
    if not library_path:
        sys.exit("Error: read_only_library_path not found in run.json.")

    return agent_view, operator_dir, library_path


def resolve_safe(library_root: str, rel_path: str) -> Path:
    """
    Resolve *rel_path* relative to *library_root* and verify it stays
    inside the library. Exits on breakout.
    """
    root = Path(library_root).resolve()
    resolved = (root / rel_path).resolve()
    if not str(resolved).startswith(str(root)):
        sys.exit(
            f"Error: path breakout detected: '{rel_path}' "
            f"resolves outside library root."
        )
    return resolved


# ---------------------------------------------------------------------------
# WORLD.md builder
# ---------------------------------------------------------------------------


def build_world_md(
    library_root: str,
    files: list[str],
    title: str = "World Fragment",
) -> str:
    """Build world-facing WORLD.md content from source files."""
    header = (
        f"# {title}\n\n"
        "You are inside the following world fragment.\n\n"
        "The material below is the world currently available here.\n\n"
        "---\n"
    )
    fragments: list[str] = []
    for i, rel_path in enumerate(files, 1):
        resolved = resolve_safe(library_root, rel_path)
        if not resolved.exists():
            sys.exit(f"Error: source file not found: {rel_path}")
        try:
            content = resolved.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            sys.exit(f"Error: cannot read file as text: {rel_path}")
        fragments.append(f"\n## Fragment {i}\n\n{content.strip()}\n")

    return header + "\n---\n".join(fragments) + "\n"


def write_world_md(agent_view: Path, content: str) -> None:
    """Write WORLD.md to agent_view/."""
    (agent_view / "WORLD.md").write_text(content, encoding="utf-8")


# ---------------------------------------------------------------------------
# WORLD_SOURCE_NOTE.md
# ---------------------------------------------------------------------------


def write_source_note(
    operator_dir: Path,
    library_path: str,
    files: list[str],
    title: str,
) -> Path:
    """Write operator/WORLD_SOURCE_NOTE.md with provenance."""
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    file_list = "\n".join(f"- {f}" for f in files)
    rebuild_cmd = (
        f"python scripts/build_world_fragment.py "
        f"--run \"{operator_dir.parent}\" "
        + " ".join(f'--files "{f}"' for f in files)
    )

    content = f"""\
# World Source Note

## Source

- Read-only source path: {library_path}
- Selected files:
{file_list}
- Built at: {now}
- Title: {title}
- Target WORLD.md: {operator_dir.parent / 'agent_view' / 'WORLD.md'}

## Boundary

The source path and selected file list are operator-side provenance.
They are not exposed to the agent-visible WORLD.md.

## Refresh

To rebuild WORLD.md after source changes, run:

```
{rebuild_cmd}
```

Do not use automatic watcher sync. Rebuild explicitly when needed.
"""
    note_path = operator_dir / "WORLD_SOURCE_NOTE.md"
    note_path.write_text(content, encoding="utf-8")
    return note_path


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Build agent_view/WORLD.md from selected source files."
    )
    parser.add_argument(
        "--run", type=str, required=True,
        help="Path to the A2 sandbox run directory.",
    )
    parser.add_argument(
        "--files", type=str, nargs="+", required=True,
        help="Source files (relative to the read-only library root).",
    )
    parser.add_argument(
        "--title", type=str, default="World Fragment",
        help="Title for WORLD.md (default: 'World Fragment').",
    )
    parser.add_argument(
        "--overwrite", action="store_true",
        help="Overwrite existing WORLD.md without prompt.",
    )
    args = parser.parse_args()

    run_path = Path(args.run).resolve()

    # Validate
    agent_view, operator_dir, library_path = validate_a2_run(run_path)

    # Check overwrite
    world_md = agent_view / "WORLD.md"
    if world_md.exists() and not args.overwrite:
        sys.exit(
            f"Error: WORLD.md already exists: {world_md}\n"
            "Use --overwrite to rebuild it."
        )

    # Build
    print(f"Building WORLD.md from {len(args.files)} file(s)...")
    content = build_world_md(library_path, args.files, args.title)
    write_world_md(agent_view, content)
    print(f"  Written: {world_md}")

    # Write source note
    note_path = write_source_note(
        operator_dir, library_path, args.files, args.title
    )
    print(f"  Source note: {note_path}")
    print()
    print("WORLD.md does not expose the source path or file names.")
    print(
        "Source provenance is recorded in "
        f"operator/{note_path.name}."
    )


if __name__ == "__main__":
    main()
