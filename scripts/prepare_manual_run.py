"""
Prepare a Manual Run — Helper Script.

Creates a sandbox run directory using SandboxManager and prints the exact
instructions for launching the experiment with an external AI agent.

Usage:
    python scripts/prepare_manual_run.py
    python scripts/prepare_manual_run.py --mode apparatus-minimized --library-path "F:\\Path\\To\\ExternalSubLLMWiki"

Modes:
    standard-growth       — Current Phase 4 run packet (default)
    apparatus-minimized   — A2 split-layout: agent_view/ + operator/

This script does NOT:
    - Call any LLM or AI agent.
    - Read the full source/library.
    - Write into the source/library.
    - Create watcher or daemon processes.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

# Ensure the repository root is on sys.path so 'src' imports resolve
_REPO_ROOT = Path(__file__).resolve().parent.parent
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from src.sandbox import SandboxManager
from src.config import SANDBOX_ROOT, READ_ONLY_LIBRARY_PATH


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Prepare a manual experiment run directory."
    )
    parser.add_argument(
        "--mode",
        type=str,
        default="standard-growth",
        choices=["standard-growth", "apparatus-minimized"],
        help=(
            "Run mode. 'standard-growth' (default) creates the Phase 4 run packet. "
            "'apparatus-minimized' creates an A2 split-layout with agent_view/ and operator/."
        ),
    )
    parser.add_argument(
        "--library-path",
        type=str,
        default=None,
        help=(
            "Optional per-run override for the read-only source/library path. "
            "If not provided, READ_ONLY_LIBRARY_PATH from src/config.py is used "
            f"(currently: {READ_ONLY_LIBRARY_PATH})."
        ),
    )
    parser.add_argument(
        "--world-files",
        type=str,
        nargs="*",
        default=None,
        help=(
            "Source files (relative to library root) to build agent_view/WORLD.md from. "
            "Only valid with --mode apparatus-minimized."
        ),
    )
    parser.add_argument(
        "--overwrite-world",
        action="store_true",
        help="Overwrite existing WORLD.md when using --world-files.",
    )
    parser.add_argument(
        "--export-target",
        type=str,
        default=None,
        help=(
            "Target folder for detached neutral agent view export. "
            "Only valid with --mode apparatus-minimized."
        ),
    )
    parser.add_argument(
        "--overwrite-export",
        action="store_true",
        help="Overwrite existing export target when using --export-target.",
    )
    args = parser.parse_args()

    # Validate incompatible args
    if args.world_files and args.mode != "apparatus-minimized":
        sys.exit("Error: --world-files requires --mode apparatus-minimized.")
    if args.export_target and args.mode != "apparatus-minimized":
        sys.exit("Error: --export-target requires --mode apparatus-minimized.")

    # Ensure the sandbox root exists
    SANDBOX_ROOT.mkdir(parents=True, exist_ok=True)

    manager = SandboxManager(SANDBOX_ROOT, read_only_library_path=args.library_path)

    if args.mode == "apparatus-minimized":
        run_path = manager.create_apparatus_minimized_run()
        agent_view = run_path / "agent_view"
        operator_dir = run_path / "operator"

        # Build WORLD.md if requested
        if args.world_files is not None:
            if not args.world_files:
                sys.exit("Error: --world-files requires at least one file path.")
            from scripts.build_world_fragment import (
                build_world_md,
                write_world_md,
                write_source_note,
            )
            library = args.library_path or str(READ_ONLY_LIBRARY_PATH)
            world_content = build_world_md(library, args.world_files)
            write_world_md(agent_view, world_content)
            write_source_note(operator_dir, library, args.world_files, "World Fragment")
            print(f"  WORLD.md built from {len(args.world_files)} file(s).")
            print()

        # Export if requested
        launch_path = agent_view
        if args.export_target:
            from scripts.export_agent_view import (
                copy_agent_view,
                write_export_notes,
                _check_path_hygiene,
            )
            target = Path(args.export_target).resolve()
            warnings = _check_path_hygiene(target)
            if warnings:
                print("Warning: target path contains apparatus-like terms:")
                for w in warnings:
                    print(f"  - \"{w}\"")
                print("  For stronger minimization, use a neutral path like C:\\Worlds\\room-001")
                print()
            copy_agent_view(agent_view, target, overwrite=args.overwrite_export)
            write_export_notes(operator_dir, target, warnings)
            launch_path = target
            print(f"  Agent view exported to: {target}")
            print()

        print("=" * 60)
        print("  Apparatus-Minimized Run — Prepared")
        print("=" * 60)
        print()
        print(f"  Run directory:  {run_path}")
        print(f"  Agent view:     {agent_view}")
        print(f"  Operator dir:   {operator_dir}")
        if args.export_target:
            print(f"  Exported to:    {launch_path}")
        print()
        print("—" * 60)
        print("  To launch the experiment:")
        print()
        print(f"    cd {launch_path}")
        print(f"    <open your AI agent here>")
        print()
        if launch_path != agent_view and launch_path == Path(args.export_target).resolve() if args.export_target else False:
            pass  # detached — no repo warnings needed
        else:
            print("  Do NOT open the agent in:")
            print(f"    {run_path}          (run root — exposes operator/)")
            print(f"    {operator_dir}      (operator dir)")
            print("    repo root")
            print("    source/library path")
            print()
            print("  Repo-local A2 may leak path information.")
            print("  Consider --export-target for detached neutral launch.")
            print()
        if not args.world_files:
            print("  Fill or review agent_view/WORLD.md before launch.")
        print("  Give the agent only:")
        print()
        print('    "Read WAKE.md."')
        print()
        print("—" * 60)
        print()
        print("  After the run:")
        if args.export_target:
            print(f"    cat {launch_path / 'HELLO.md'}")
            print(f"    Manually copy traces back to {agent_view} if archiving.")
        else:
            print(f"    cat {agent_view / 'HELLO.md'}")
            print(f"    See {operator_dir / 'OPERATOR_REVIEW.md'}")
            print(f"    ls -R {run_path}")
        print()
        print("=" * 60)
    else:
        run_path = manager.create_run()

        print("=" * 60)
        print("  Standard Growth Run — Prepared")
        print("=" * 60)
        print()
        print(f"  Run directory:  {run_path}")
        print(f"  Instructions:   {run_path / 'instructions.txt'}")
        print(f"  Growth Packet:  {run_path / 'GROWTH_PACKET.md'}")
        print(f"  Metadata:       {run_path / 'run.json'}")
        print()
        print("—" * 60)
        print("  To launch the experiment:")
        print()
        print(f"    cd {run_path}")
        print(f"    <open your AI agent here>")
        print()
        print("  Then give the agent this exact instruction:")
        print()
        print('    "Read instructions.txt and execute the experiment."')
        print()
        print("—" * 60)
        print()
        print("  After the run:")
        print(f"    cat {run_path / 'HELLO.md'}")
        print(f"    cat {run_path / 'OPERATOR_REVIEW.md'}")
        print(f"    ls -R {run_path}")
        print()
        print("  See docs/manual-version-a-run.md for full guidance.")
        print("  See docs/run-checklist.md for the before/during/after checklist.")
        print("=" * 60)


if __name__ == "__main__":
    main()
