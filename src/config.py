"""
Configuration Management for the Experiment Framework.

Handles resolution of workspace paths, default names, and environments parameters.
"""

import os
from pathlib import Path

# Base Paths (Relative to Repository Root)
REPO_ROOT = Path(__file__).resolve().parent.parent

# Writable Sandbox Root (Where individual run directories are spawned)
SANDBOX_ROOT = Path(os.getenv("SANDBOX_ROOT", REPO_ROOT / "sandbox"))

# Read-Only Wiki/Library Path
# Users should configure this environment variable to point to their real sub LLM-Wiki.
# Defaults to our local mock library `library_sample/` if not specified.
READ_ONLY_LIBRARY_PATH = Path(
    os.getenv("READ_ONLY_LIBRARY_PATH", REPO_ROOT / "library_sample")
)

# Run Metadata Database file (JSONL format)
RUN_METADATA_FILE = Path(
    os.getenv("RUN_METADATA_FILE", REPO_ROOT / "docs" / "runs_metadata.jsonl")
)

def validate_config() -> bool:
    """
    Validates that the directories configured actually exist or can be created.
    """
    try:
        # Sandbox root must exist or be writable (ensure we can write to it)
        os.makedirs(SANDBOX_ROOT, exist_ok=True)
        
        # Library path must exist
        if not READ_ONLY_LIBRARY_PATH.exists():
            print(f"Warning: Configure library path does not exist: {READ_ONLY_LIBRARY_PATH}")
            return False
            
        return True
    except Exception as e:
        print(f"Configuration validation failed: {e}")
        return False

if __name__ == "__main__":
    print("Project Configuration Summary:")
    print(f"  Repository Root: {REPO_ROOT}")
    print(f"  Sandbox Root:    {SANDBOX_ROOT}")
    print(f"  Read-Only Wiki:  {READ_ONLY_LIBRARY_PATH}")
    print(f"  Metadata Log:    {RUN_METADATA_FILE}")
    print(f"  Validation:      {'Passed' if validate_config() else 'Failed'}")
