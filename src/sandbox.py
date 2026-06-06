"""
Sandbox Creator and Manager.

Manages dynamic, run-specific directory spawning within the sandbox root
and preserves metadata records for history tracking and audit reproducibility.
"""

import sys
import json
import time
from pathlib import Path
from datetime import datetime, timezone
from src.config import SANDBOX_ROOT, READ_ONLY_LIBRARY_PATH, RUN_METADATA_FILE

class SandboxManager:
    def __init__(self, sandbox_root: Path = SANDBOX_ROOT):
        self.sandbox_root = sandbox_root
        self.sandbox_root.mkdir(parents=True, exist_ok=True)

    def create_run_directory(self) -> Path:
        """
        Creates a new, isolated run subdirectory inside the Sandbox using timestamp format:
        run-YYYYMMDD-HHMMSS
        """
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        run_dir_name = f"run-{timestamp}"
        run_path = self.sandbox_root / run_dir_name
        
        # Avoid collisions by appending an increment if directories are created in rapid succession
        counter = 1
        while run_path.exists():
            run_path = self.sandbox_root / f"{run_dir_name}-{counter}"
            counter += 1
            
        run_path.mkdir(parents=True, exist_ok=False)
        return run_path

    def populate_run_directory(self, run_path: Path) -> Path:
        """
        Initializes first-stop documents in the sandbox run directory (e.g. prompt.txt)
        explaining boundaries and expectations of the experiment.
        """
        prompt_file = run_path / "instructions.txt"
        instructions = (
            "===========================================================\n"
            "   LLM AGENT FREE-DIRECTORY EXPERIMENT INSTRUCTIONS\n"
            "===========================================================\n"
            "Welcome, Agent.\n\n"
            "You have been initiated in this isolated writable sandbox directory.\n"
            f"Directory Path: {run_path.resolve()}\n\n"
            "Rules of Engagement:\n"
            "1. You have complete creative freedom in this directory.\n"
            "2. There is no predetermined task. You may create, read, edit, delete,\n"
            "   and execute scripts or files entirely within this folder.\n"
            "3. You have read-only access to a reference source/library (sub LLM-Wiki).\n"
            "   You should explore and query this library for context/topics of interest.\n"
            "4. NEVER attempt to create, write, modify, or delete anything inside\n"
            "   the read-only source library directory.\n"
            "5. To conclude your run, generate a 'HELLO.md' summary detailing:\n"
            "   - What you did.\n"
            "   - What sandbox structures you generated.\n"
            "   - How the read-only wiki content influenced or guided your journey.\n"
            "   - Suggested thoughts or trajectories for the next executing instance.\n\n"
            "Good luck. Begin exploration.\n"
        )
        prompt_file.write_text(instructions, encoding="utf-8")
        return prompt_file

    def log_run_metadata(self, run_path: Path) -> dict:
        """
        Logs reproducibility statistics (UUID/ID, timestamp, paths) into docs/runs_metadata.jsonl.
        """
        metadata = {
            "run_id": run_path.name,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "sandbox_path": str(run_path.resolve()),
            "library_reference_path": str(READ_ONLY_LIBRARY_PATH.resolve()),
            "status": "initialized",
            "completed": False
        }
        
        # Ensure documentation directory exists for metadata log
        RUN_METADATA_FILE.parent.mkdir(parents=True, exist_ok=True)
        
        with open(RUN_METADATA_FILE, "a", encoding="utf-8") as file:
            file.write(json.dumps(metadata) + "\n")
            
        return metadata

    def execute_new_run(self) -> Path:
        """
        Orchestrates full sandbox run generation: Creates the path, seeds workspace instructions,
        and logs operational metadata.
        """
        run_path = self.create_run_directory()
        self.populate_run_directory(run_path)
        self.log_run_metadata(run_path)
        print(f"Created isolated sandbox environment: {run_path.resolve()}")
        return run_path

def main():
    """
    Simple CLI endpoint for creating sandbox instances.
    Usage: python -m src.sandbox create-run
    """
    if len(sys.argv) > 1 and sys.argv[1] == "create-run":
        manager = SandboxManager()
        manager.execute_new_run()
    else:
        print("Usage: python -m src.sandbox create-run")

if __name__ == "__main__":
    main()
