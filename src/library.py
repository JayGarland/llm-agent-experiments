"""
Library Access Utilities — Read-Only Source/Library Access Layer.

Provides a minimal LibraryReader class for safe, read-only discovery and retrieval of files
from a configured source/library root (e.g., a local sub LLM-Wiki).

This branch implements only the read-only access layer. Sandbox writing, agent execution,
watcher automation, provider integration, and metadata logging belong to later branches.
"""

from pathlib import Path
from typing import List


class LibraryAccessError(Exception):
    """Raised when an invalid or unsafe operation is attempted on the Read-Only Library."""
    pass


def verify_and_resolve_path(relative_path: str | Path, base_dir: Path) -> Path:
    """
    Standalone path-resolution utility: checks that a requested path falls within base_dir.
    Used for advisory boundary checks; also consumed internally by LibraryReader.
    """
    base_resolved = base_dir.resolve()
    target_resolved = (base_resolved / relative_path).resolve()

    if not target_resolved.is_relative_to(base_resolved):
        raise LibraryAccessError(
            f"Advisory Denied: Escape detected. "
            f"'{target_resolved}' is outside base directory '{base_resolved}'"
        )
    return target_resolved


class LibraryReader:
    """
    Minimal read-only access layer for a configured source/library root.

    The agent may inspect this source/library, but is not required to use it.
    All operations are read-only — this class never writes, deletes, renames,
    or modifies files in the library.
    """

    def __init__(self, library_root: str | Path) -> None:
        self._root = Path(library_root).resolve()
        if not self._root.is_dir():
            raise LibraryAccessError(
                f"Library root does not exist or is not a directory: {self._root}"
            )

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    @property
    def root(self) -> Path:
        """The resolved absolute path to the library root (read-only)."""
        return self._root

    def list_files(self) -> List[Path]:
        """
        Return a sorted list of every file under the library root, expressed as
        relative paths from the root.  Directories are excluded.
        """
        files: List[Path] = []
        for entry in sorted(self._root.rglob("*")):
            if entry.is_file():
                files.append(entry.relative_to(self._root))
        return files

    def read_file(self, relative_path: str | Path) -> str:
        """
        Read a text file from the library by relative path.

        Raises LibraryAccessError if the resolved path escapes the library root
        or if the target is not a regular file.
        """
        target = self._resolve_safe(relative_path)
        if not target.is_file():
            raise LibraryAccessError(f"Not a file or not found: {relative_path}")
        return target.read_text(encoding="utf-8")

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _resolve_safe(self, relative_path: str | Path) -> Path:
        """Resolve *relative_path* inside the library root, rejecting breakouts."""
        return verify_and_resolve_path(relative_path, self._root)


# ---------------------------------------------------------------------------
# Module-level convenience functions (delegate to a default LibraryReader)
# ---------------------------------------------------------------------------

_default_reader: LibraryReader | None = None


def _get_default_reader() -> LibraryReader:
    """Lazily create a default LibraryReader pointed at the configured library path."""
    global _default_reader
    if _default_reader is None:
        from src.config import READ_ONLY_LIBRARY_PATH
        _default_reader = LibraryReader(READ_ONLY_LIBRARY_PATH)
    return _default_reader


def list_library_files() -> List[str]:
    """
    List files relative to the configured library root (convenience wrapper).

    Returns file paths as strings for easy consumption by downstream consumers.
    """
    return [str(p) for p in _get_default_reader().list_files()]


def read_library_file(relative_path: str | Path) -> str:
    """
    Read a file from the configured library root (convenience wrapper).
    """
    return _get_default_reader().read_file(relative_path)


