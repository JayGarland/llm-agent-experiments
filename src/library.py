"""
Library Access Utilities.

Provides secure interfaces for the AI agent to list and read content from 
the configured sub LLM-Wiki. Enforces strict read-only guarantees in code.
"""

from pathlib import Path
from typing import List, Generator
from src.config import READ_ONLY_LIBRARY_PATH

class LibraryAccessError(Exception):
    """Raised when an invalid operation is performed on the Read-Only Library."""
    pass

def _resolve_safe_path(relative_path: str | Path) -> Path:
    """
    Resolves the target path inside the read-only library.
    Enforces strict path-traversal boundaries to block path breakout attacks (e.g. '../../').
    """
    library_base = READ_ONLY_LIBRARY_PATH.resolve()
    target_path = (library_base / relative_path).resolve()
    
    # Check that target_path starts with library_base path (is a sub-path)
    if not str(target_path).startswith(str(library_base)):
        raise LibraryAccessError(
            f"Access Denied: Attempted path escape detected! Path '{target_path}' "
            f"is outside library boundary '{library_base}'"
        )
        
    return target_path

def list_library_files() -> List[str]:
    """
    Recursively list all file paths relative to the read-only library root.
    Files matching system ignore filters or git placeholders are filtered out.
    """
    library_base = READ_ONLY_LIBRARY_PATH.resolve()
    if not library_base.exists():
        raise LibraryAccessError("Library base directory does not exist.")
        
    discovered_files = []
    for path in library_base.rglob("*"):
        if path.is_file():
            # Skip hidden files or git keeps
            if path.name.startswith(".") or path.suffix == ".gitkeep":
                continue
            relative = path.relative_to(library_base)
            discovered_files.append(str(relative).replace("\\", "/"))
            
    return sorted(discovered_files)

def read_library_file(relative_path: str | Path) -> str:
    """
    Retrieves the raw content of a file from the read-only library.
    """
    resolved_path = _resolve_safe_path(relative_path)
    
    if not resolved_path.exists():
        raise LibraryAccessError(f"File not found: {relative_path}")
        
    if not resolved_path.is_file():
        raise LibraryAccessError(f"Target is not a file: {relative_path}")
        
    try:
        return resolved_path.read_text(encoding="utf-8")
    except Exception as e:
        raise LibraryAccessError(f"Failed to read file '{relative_path}': {e}")

# Strict read-only operations — intentionally no rewrite / delete / update code is declared.
# If an LLM or consumer tries to write to the library, it will fail due to the lack of exposed APIs.
