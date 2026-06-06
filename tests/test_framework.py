"""
Unit Tests — Read-Only Source/Library Access Layer.

This branch (feature/read-only-library-access) implements only the library access layer.
Tests for sandbox creation, agent execution, watcher triggers, and provider integration
belong to later branches.
"""

import pytest
from pathlib import Path
import tempfile

from src.library import (
    LibraryReader,
    LibraryAccessError,
    verify_and_resolve_path,
)


# ---------------------------------------------------------------------------
# Path containment utility
# ---------------------------------------------------------------------------

def test_verify_and_resolve_path_valid():
    """Valid relative paths resolve correctly inside the base directory."""
    with tempfile.TemporaryDirectory() as tmp:
        base = Path(tmp).resolve()
        (base / "sub").mkdir()
        (base / "sub" / "f.txt").write_text("hello", encoding="utf-8")

        resolved = verify_and_resolve_path("sub/f.txt", base)
        assert resolved == base / "sub" / "f.txt"


def test_verify_and_resolve_path_breakout():
    """../ breakout attempts are rejected."""
    with tempfile.TemporaryDirectory() as tmp:
        base = Path(tmp).resolve()
        (base / "sub").mkdir()

        with pytest.raises(LibraryAccessError):
            verify_and_resolve_path("../escape.txt", base / "sub")


# ---------------------------------------------------------------------------
# LibraryReader construction
# ---------------------------------------------------------------------------

def test_constructor_rejects_missing_root():
    """LibraryReader raises if the given root does not exist."""
    with pytest.raises(LibraryAccessError):
        LibraryReader("/nonexistent/path/42")


def test_constructor_rejects_file_as_root():
    """LibraryReader raises if the given root is a file, not a directory."""
    with tempfile.NamedTemporaryFile(delete=False) as f:
        f.write(b"data")
        tmp_file = f.name
    try:
        with pytest.raises(LibraryAccessError):
            LibraryReader(tmp_file)
    finally:
        Path(tmp_file).unlink()


def test_root_property():
    """The .root property returns the resolved absolute path."""
    with tempfile.TemporaryDirectory() as tmp:
        reader = LibraryReader(tmp)
        assert reader.root == Path(tmp).resolve()


# ---------------------------------------------------------------------------
# list_files
# ---------------------------------------------------------------------------

def test_list_files_empty_library():
    """An empty library root returns an empty list."""
    with tempfile.TemporaryDirectory() as tmp:
        reader = LibraryReader(tmp)
        assert reader.list_files() == []


def test_list_files_returns_relative_paths():
    """list_files returns relative Paths, excluding directories."""
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        (root / "a.txt").write_text("a", encoding="utf-8")
        (root / "sub").mkdir()
        (root / "sub" / "b.txt").write_text("b", encoding="utf-8")

        reader = LibraryReader(tmp)
        files = reader.list_files()
        assert files == [Path("a.txt"), Path("sub/b.txt")]


# ---------------------------------------------------------------------------
# read_file — happy path
# ---------------------------------------------------------------------------

def test_read_file_returns_content():
    """read_file returns the full text content of a library file."""
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        (root / "notes").mkdir()
        (root / "notes" / "todo.md").write_text("# TODO\n- item 1\n", encoding="utf-8")

        reader = LibraryReader(tmp)
        content = reader.read_file("notes/todo.md")
        assert content == "# TODO\n- item 1\n"


# ---------------------------------------------------------------------------
# read_file — error paths
# ---------------------------------------------------------------------------

def test_read_file_rejects_breakout():
    """read_file raises LibraryAccessError on ../ path breakout."""
    with tempfile.TemporaryDirectory() as tmp:
        reader = LibraryReader(tmp)
        with pytest.raises(LibraryAccessError):
            reader.read_file("../secret.txt")


def test_read_file_rejects_absolute_path_outside():
    """read_file rejects an absolute path that lies outside the library root."""
    with tempfile.TemporaryDirectory() as tmp:
        reader = LibraryReader(tmp)
        outside = Path(tempfile.gettempdir()) / "outside.txt"
        with pytest.raises(LibraryAccessError):
            reader.read_file(str(outside))


def test_read_file_missing_file():
    """read_file raises LibraryAccessError for a non-existent relative path."""
    with tempfile.TemporaryDirectory() as tmp:
        reader = LibraryReader(tmp)
        with pytest.raises(LibraryAccessError):
            reader.read_file("does_not_exist.md")


# ---------------------------------------------------------------------------
# No write API exposed
# ---------------------------------------------------------------------------

def test_no_write_api_exposed():
    """
    LibraryReader must not expose methods that can write, delete, rename,
    or modify files.  Verify that only safe, read-oriented public names exist.
    """
    reader = LibraryReader(tempfile.gettempdir())
    public = {name for name in dir(reader) if not name.startswith("_")}

    # Allow only the documented read-only API members plus Python dunder/mro
    allowed = {"root", "list_files", "read_file"}
    unexpected = public - allowed

    # exclude anything Python always adds on every object
    unexpected.discard("__class__")
    unexpected.discard("__dict__")
    unexpected.discard("__doc__")
    unexpected.discard("__init__")
    unexpected.discard("__module__")
    unexpected.discard("__new__")
    unexpected.discard("__weakref__")
    unexpected.discard("__dir__")
    unexpected.discard("__format__")
    unexpected.discard("__getattribute__")
    unexpected.discard("__hash__")
    unexpected.discard("__reduce__")
    unexpected.discard("__reduce_ex__")
    unexpected.discard("__repr__")
    unexpected.discard("__setattr__")
    unexpected.discard("__sizeof__")
    unexpected.discard("__str__")
    unexpected.discard("__subclasshook__")
    unexpected.discard("__delattr__")
    unexpected.discard("__eq__")
    unexpected.discard("__ge__")
    unexpected.discard("__gt__")
    unexpected.discard("__le__")
    unexpected.discard("__lt__")
    unexpected.discard("__ne__")

    assert unexpected == set(), (
        f"LibraryReader exposes unexpected public names: {unexpected}. "
        "It must only expose read-only operations."
    )


# ---------------------------------------------------------------------------
# Convenience functions (module-level)
# ---------------------------------------------------------------------------

def test_list_library_files_convenience():
    """list_library_files() delegates to the default LibraryReader."""
    from src.library import list_library_files
    from src.config import READ_ONLY_LIBRARY_PATH

    result = list_library_files()
    expected = LibraryReader(READ_ONLY_LIBRARY_PATH).list_files()
    assert result == [str(p) for p in expected]


