"""
Unit Tests — Read-Only Source/Library Access Layer + Sandbox Manager.

feature/read-only-library-access : library access layer.
feature/sandbox-manager           : writable sandbox management (this branch).

Tests for agent execution, watcher triggers, and provider integration
belong to later branches.
"""

import json
import pytest
from pathlib import Path
import tempfile

from src.library import (
    LibraryReader,
    LibraryAccessError,
    verify_and_resolve_path,
)
from src.sandbox import SandboxManager, SandboxError


# ============================================================================
# Library access tests (from feature/read-only-library-access)
# ============================================================================


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


# ============================================================================
# Sandbox manager tests (feature/sandbox-manager)
# ============================================================================


# ---------------------------------------------------------------------------
# Construction
# ---------------------------------------------------------------------------

def test_sandbox_constructor_rejects_missing_root():
    """SandboxManager raises SandboxError if the root does not exist."""
    with pytest.raises(SandboxError):
        SandboxManager("/nonexistent/sandbox/99")


def test_sandbox_constructor_rejects_file_as_root():
    """SandboxManager raises if root is a file, not a directory."""
    with tempfile.NamedTemporaryFile(delete=False) as f:
        f.write(b"data")
        tmp_file = f.name
    try:
        with pytest.raises(SandboxError):
            SandboxManager(tmp_file)
    finally:
        Path(tmp_file).unlink()


def test_sandbox_root_property():
    """.root returns the resolved absolute path."""
    with tempfile.TemporaryDirectory() as tmp:
        mgr = SandboxManager(tmp)
        assert mgr.root == Path(tmp).resolve()


# ---------------------------------------------------------------------------
# create_run — directory creation
# ---------------------------------------------------------------------------

def test_create_run_creates_directory_under_root():
    """create_run() creates a directory inside the sandbox root."""
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        mgr = SandboxManager(root)
        run_path = mgr.create_run()

        assert run_path.exists()
        assert run_path.is_dir()
        assert run_path.is_relative_to(mgr.root)


def test_create_run_naming_scheme():
    """The run directory name follows the run-YYYYMMDD-HHMMSS-<shortid> pattern."""
    import re
    with tempfile.TemporaryDirectory() as tmp:
        mgr = SandboxManager(tmp)
        run_path = mgr.create_run()
        name = run_path.name
        assert re.match(r"^run-\d{8}-\d{6}-[0-9a-f]{6}$", name), f"Unexpected name: {name}"


def test_create_run_unique_each_call():
    """Two consecutive create_run() calls produce different directories."""
    with tempfile.TemporaryDirectory() as tmp:
        mgr = SandboxManager(tmp)
        run1 = mgr.create_run()
        run2 = mgr.create_run()
        assert run1 != run2


def test_create_run_does_not_escape_root():
    """Even with a deeply nested root, the created directory stays inside."""
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp) / "nested" / "sandbox"
        root.mkdir(parents=True)
        mgr = SandboxManager(root)
        run_path = mgr.create_run()
        assert run_path.is_relative_to(root.resolve())


# ---------------------------------------------------------------------------
# Seeded instructions
# ---------------------------------------------------------------------------

def test_create_run_seeds_instructions():
    """create_run writes a neutral instructions.txt inside the run directory."""
    with tempfile.TemporaryDirectory() as tmp:
        mgr = SandboxManager(tmp)
        run_path = mgr.create_run()
        instructions = run_path / "instructions.txt"

        assert instructions.exists()
        content = instructions.read_text(encoding="utf-8")

        # Neutrality checks
        assert "no assigned task" in content.lower()
        assert "read-only" in content.lower()
        assert "HELLO.md" in content
        # Must NOT assign a specific goal
        assert "your task is" not in content.lower()


def test_create_run_instructions_do_not_require_library():
    """The seeded instructions must not force the agent to use the library."""
    with tempfile.TemporaryDirectory() as tmp:
        mgr = SandboxManager(tmp)
        run_path = mgr.create_run()
        content = (run_path / "instructions.txt").read_text(encoding="utf-8")
        assert "not required to use it" in content


# ---------------------------------------------------------------------------
# Per-run metadata
# ---------------------------------------------------------------------------

def test_create_run_writes_run_json():
    """create_run writes a run.json inside the run directory (not globally)."""
    with tempfile.TemporaryDirectory() as tmp:
        mgr = SandboxManager(tmp)
        run_path = mgr.create_run()
        meta_file = run_path / "run.json"

        assert meta_file.exists()
        meta = json.loads(meta_file.read_text(encoding="utf-8"))
        assert "run_name" in meta
        assert "created_utc" in meta
        assert "sandbox_root" in meta


# ---------------------------------------------------------------------------
# Does not touch source/library
# ---------------------------------------------------------------------------

def test_create_run_does_not_touch_library():
    """
    create_run must not read, write, or otherwise interact with the
    read-only source/library.  It operates exclusively inside the sandbox.
    """
    with tempfile.TemporaryDirectory() as sandbox_tmp:
        # Use a real library path but verify nothing is written there
        from src.config import READ_ONLY_LIBRARY_PATH
        before = sorted(READ_ONLY_LIBRARY_PATH.rglob("*"))

        mgr = SandboxManager(sandbox_tmp)
        mgr.create_run()

        after = sorted(READ_ONLY_LIBRARY_PATH.rglob("*"))
        assert before == after, (
            "SandboxManager.create_run() modified the source/library — "
            "this must not happen."
        )


# ---------------------------------------------------------------------------
# No agent execution
# ---------------------------------------------------------------------------

def test_sandbox_manager_has_no_execution_api():
    """
    SandboxManager must not expose any method that implies agent execution,
    LLM calls, or run orchestration.  Only sandbox creation and seeding.
    """
    mgr = SandboxManager(tempfile.gettempdir())
    public = {name for name in dir(mgr) if not name.startswith("_")}

    allowed = {"root", "create_run"}
    unexpected = public - allowed

    # Python built-in dunders that appear on every object
    builtins = {
        "__class__", "__dict__", "__doc__", "__init__", "__module__",
        "__new__", "__weakref__", "__dir__", "__format__",
        "__getattribute__", "__hash__", "__reduce__", "__reduce_ex__",
        "__repr__", "__setattr__", "__sizeof__", "__str__",
        "__subclasshook__", "__delattr__", "__eq__", "__ge__", "__gt__",
        "__le__", "__lt__", "__ne__",
    }
    unexpected -= builtins

    assert unexpected == set(), (
        f"SandboxManager exposes unexpected public names: {unexpected}. "
        "Agent execution belongs to a later branch."
    )