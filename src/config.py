"""
Configuration Parameters for the Experiment Framework (Scaffolding).

Centralizes path variables. Actual loading logic is deferred to feature/config-and-path-management.
"""

from pathlib import Path

# Base Paths (Relative to Repository Root)
REPO_ROOT = Path(__file__).resolve().parent.parent

# Writable Sandbox Root (Where individual run directories are spawned in the future)
SANDBOX_ROOT = REPO_ROOT / "sandbox"

# Read-Only Wiki/Library Path
READ_ONLY_LIBRARY_PATH = REPO_ROOT / "library_sample"

# Run Metadata Database file (JSONL format)
RUN_METADATA_FILE = REPO_ROOT / "docs" / "runs_metadata.jsonl"

def validate_config() -> bool:
    """
    Validation scaffolding. Returns True as a placeholder.
    Real validation logic belongs to feature/config-and-path-management.
    """
    raise NotImplementedError(
        "Active environment and configuration validation is deferred to downstream branches, "
        "specifically 'feature/config-and-path-management'."
    )

