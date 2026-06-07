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
    args = parser.parse_args()

    # Ensure the sandbox root exists (create if needed — safe, it's our own directory)
    SANDBOX_ROOT.mkdir(parents=True, exist_ok=True)

    manager = SandboxManager(SANDBOX_ROOT, read_only_library_path=args.library_path)

    if args.mode == "apparatus-minimized":
        run_path = manager.create_apparatus_minimized_run()
        agent_view = run_path / "agent_view"
        operator_dir = run_path / "operator"

        print("=" * 60)
        print("  Apparatus-Minimized Run — Prepared")
        print("=" * 60)
        print()
        print(f"  Run directory:  {run_path}")
        print(f"  Agent view:     {agent_view}")
        print(f"  Operator dir:   {operator_dir}")
        print()
        print("—" * 60)
        print("  To launch the experiment:")
        print()
        print(f"    cd {agent_view}")
        print(f"    <open your AI agent here>")
        print()
        print("  Do NOT open the agent in:")
        print(f"    {run_path}          (run root — exposes operator/)")
        print(f"    {operator_dir}      (operator dir)")
        print("    repo root")
        print("    source/library path")
        print()
        print("  Fill or review agent_view/WORLD.md before launch.")
        print("  Give the agent only:")
        print()
        print('    "Read WAKE.md."')
        print()
        print("—" * 60)
        print()
        print("  After the run:")
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
