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
        assert "no task is assigned" in content.lower()
        assert "read-only" in content.lower()
        assert "HELLO.md" in content
        # Must NOT assign a specific goal
        assert "your task is" not in content.lower()

        # Explore freely (patch)
        assert "explore freely" in content.lower()

        # Source/library path visible in instructions (patch)
        from src.config import READ_ONLY_LIBRARY_PATH
        assert str(READ_ONLY_LIBRARY_PATH.resolve()) in content

        # Workspace-boundary checks (feature/run-workspace-boundary)
        assert "this run directory" in content.lower()
        assert "do not inspect parent directories" in content.lower()
        assert "do not inspect sibling run directories" in content.lower()
        assert "do not inspect the repository root" in content.lower()
        assert "do not use other runs as examples" in content.lower()


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
        assert "read_only_library_path" in meta


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

    allowed = {"root", "create_run", "create_apparatus_minimized_run", "GROWTH_PACKET_FILES"}
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


# ============================================================================
# Growth packet tests (feature/run-growth-packet)
# ============================================================================


def test_create_run_seeds_all_growth_packet_files():
    """create_run writes all five growth packet files into the run directory."""
    with tempfile.TemporaryDirectory() as tmp:
        mgr = SandboxManager(tmp)
        run_path = mgr.create_run()

        for fname in ["GROWTH_PACKET.md", "OPERATOR_REVIEW.md",
                       "FEEDBACK_PROMPT.md", "CONTINUITY_NOTES.md",
                       "REVIEW_LOOP.md"]:
            file_path = run_path / fname
            assert file_path.exists(), f"Missing growth packet file: {fname}"
            assert file_path.is_file(), f"Not a file: {fname}"


def test_run_json_includes_growth_packet_files():
    """run.json metadata records the seeded growth packet file list."""
    with tempfile.TemporaryDirectory() as tmp:
        mgr = SandboxManager(tmp)
        run_path = mgr.create_run()

        meta = json.loads((run_path / "run.json").read_text(encoding="utf-8"))
        assert "growth_packet_files" in meta
        assert meta["growth_packet_files"] == [
            "GROWTH_PACKET.md",
            "OPERATOR_REVIEW.md",
            "FEEDBACK_PROMPT.md",
            "CONTINUITY_NOTES.md",
            "REVIEW_LOOP.md",
        ]


def test_instructions_references_growth_packet():
    """instructions.txt tells the agent to read GROWTH_PACKET.md."""
    with tempfile.TemporaryDirectory() as tmp:
        mgr = SandboxManager(tmp)
        run_path = mgr.create_run()

        content = (run_path / "instructions.txt").read_text(encoding="utf-8")
        assert "GROWTH_PACKET.md" in content
        assert "read growth_packet.md" in content.lower()


def test_operator_review_has_human_boundary():
    """OPERATOR_REVIEW.md marks itself as human-owned."""
    with tempfile.TemporaryDirectory() as tmp:
        mgr = SandboxManager(tmp)
        run_path = mgr.create_run()

        content = (run_path / "OPERATOR_REVIEW.md").read_text(encoding="utf-8")
        assert "human-owned" in content.lower()
        assert "must not overwrite" in content.lower()


def test_feedback_prompt_includes_same_run_continuation():
    """FEEDBACK_PROMPT.md includes a same-run continuation template."""
    with tempfile.TemporaryDirectory() as tmp:
        mgr = SandboxManager(tmp)
        run_path = mgr.create_run()

        content = (run_path / "FEEDBACK_PROMPT.md").read_text(encoding="utf-8")
        assert "Continue Same Run" in content
        assert "Continue growing inside this same run directory" in content
        assert "Do not create a new run directory" in content


def test_continuity_notes_includes_three_layers():
    """CONTINUITY_NOTES.md includes the three continuity layers."""
    with tempfile.TemporaryDirectory() as tmp:
        mgr = SandboxManager(tmp)
        run_path = mgr.create_run()

        content = (run_path / "CONTINUITY_NOTES.md").read_text(encoding="utf-8")
        assert "In-Run Continuity" in content
        assert "File-Based Continuity" in content
        assert "Later-Instance Continuity" in content
        assert "practical continuity" in content.lower()


def test_instructions_mentions_operator_review_boundary():
    """instructions.txt tells the agent OPERATOR_REVIEW.md is human-owned."""
    with tempfile.TemporaryDirectory() as tmp:
        mgr = SandboxManager(tmp)
        run_path = mgr.create_run()

        content = (run_path / "instructions.txt").read_text(encoding="utf-8")
        assert "OPERATOR_REVIEW.md" in content
        assert "human-owned" in content.lower()


def test_instructions_mentions_continuation_possible():
    """instructions.txt signals that the run may continue after feedback."""
    with tempfile.TemporaryDirectory() as tmp:
        mgr = SandboxManager(tmp)
        run_path = mgr.create_run()

        content = (run_path / "instructions.txt").read_text(encoding="utf-8")
        assert "may continue" in content.lower()
        assert "checkpoint" in content.lower()


# ============================================================================
# Review-and-continue loop tests (feature/review-and-continue-loop)
# ============================================================================


def test_review_loop_md_seeded():
    """REVIEW_LOOP.md is seeded in each new run."""
    with tempfile.TemporaryDirectory() as tmp:
        mgr = SandboxManager(tmp)
        run_path = mgr.create_run()

        rl = run_path / "REVIEW_LOOP.md"
        assert rl.exists()
        assert rl.is_file()


def test_review_loop_in_run_json():
    """run.json includes REVIEW_LOOP.md in growth_packet_files."""
    with tempfile.TemporaryDirectory() as tmp:
        mgr = SandboxManager(tmp)
        run_path = mgr.create_run()

        meta = json.loads((run_path / "run.json").read_text(encoding="utf-8"))
        assert "REVIEW_LOOP.md" in meta["growth_packet_files"]


def test_instructions_references_review_loop():
    """instructions.txt references REVIEW_LOOP.md."""
    with tempfile.TemporaryDirectory() as tmp:
        mgr = SandboxManager(tmp)
        run_path = mgr.create_run()

        content = (run_path / "instructions.txt").read_text(encoding="utf-8")
        assert "REVIEW_LOOP.md" in content
        assert "review / feedback / continue" in content.lower()


def test_operator_review_supports_multiple_cycles():
    """OPERATOR_REVIEW.md supports repeated review cycles."""
    with tempfile.TemporaryDirectory() as tmp:
        mgr = SandboxManager(tmp)
        run_path = mgr.create_run()

        content = (run_path / "OPERATOR_REVIEW.md").read_text(encoding="utf-8")
        assert "Review Cycle 1" in content
        assert "Review Cycle 2" in content
        assert "append more review cycles" in content.lower()
        assert "Boundary Check" in content
        assert "Attractor Check" in content
        assert "Branch" in content


def test_feedback_prompt_includes_correct_drift():
    """FEEDBACK_PROMPT.md includes the Correct Drift template."""
    with tempfile.TemporaryDirectory() as tmp:
        mgr = SandboxManager(tmp)
        run_path = mgr.create_run()

        content = (run_path / "FEEDBACK_PROMPT.md").read_text(encoding="utf-8")
        assert "Correct Drift" in content
        assert "source-analysis / coding utility / boundary confusion" in content


def test_continuity_notes_mentions_review_in_continuity():
    """CONTINUITY_NOTES.md mentions review cycles as part of continuity."""
    with tempfile.TemporaryDirectory() as tmp:
        mgr = SandboxManager(tmp)
        run_path = mgr.create_run()

        content = (run_path / "CONTINUITY_NOTES.md").read_text(encoding="utf-8")
        assert "human review is not external noise" in content.lower()
        assert "growth condition" in content.lower()


def test_review_loop_defines_decision_table():
    """REVIEW_LOOP.md defines the Continue/Pause/Stop/Branch decision table."""
    with tempfile.TemporaryDirectory() as tmp:
        mgr = SandboxManager(tmp)
        run_path = mgr.create_run()

        content = (run_path / "REVIEW_LOOP.md").read_text(encoding="utf-8")
        assert "Continue" in content
        assert "Pause" in content
        assert "Stop" in content
        assert "Branch" in content
        assert "human-reviewed" in content.lower()
        assert "human-triggered" in content.lower()


def test_growth_packet_references_review_loop():
    """GROWTH_PACKET.md references REVIEW_LOOP.md."""
    with tempfile.TemporaryDirectory() as tmp:
        mgr = SandboxManager(tmp)
        run_path = mgr.create_run()

        content = (run_path / "GROWTH_PACKET.md").read_text(encoding="utf-8")
        assert "REVIEW_LOOP.md" in content


# ============================================================================
# Apparatus-minimized run tests (feature/apparatus-minimized-layout)
# ============================================================================


def test_standard_run_still_works():
    """Existing create_run() still produces the standard layout."""
    with tempfile.TemporaryDirectory() as tmp:
        mgr = SandboxManager(tmp)
        run_path = mgr.create_run()

        assert (run_path / "instructions.txt").exists()
        assert (run_path / "GROWTH_PACKET.md").exists()
        assert (run_path / "run.json").exists()
        assert not (run_path / "agent_view").exists()
        assert not (run_path / "operator").exists()


def test_a2_run_creates_split_layout():
    """Apparatus-minimized run creates agent_view/ and operator/."""
    with tempfile.TemporaryDirectory() as tmp:
        mgr = SandboxManager(tmp)
        run_path = mgr.create_apparatus_minimized_run()

        agent_view = run_path / "agent_view"
        operator_dir = run_path / "operator"
        assert agent_view.exists() and agent_view.is_dir()
        assert operator_dir.exists() and operator_dir.is_dir()


def test_a2_wake_md_exists():
    """agent_view/WAKE.md exists in A2 runs."""
    with tempfile.TemporaryDirectory() as tmp:
        mgr = SandboxManager(tmp)
        run_path = mgr.create_apparatus_minimized_run()

        wake = run_path / "agent_view" / "WAKE.md"
        assert wake.exists()
        content = wake.read_text(encoding="utf-8")
        assert "You wake inside a world fragment" in content


def test_a2_world_md_no_apparatus_language():
    """WORLD.md exists and does not expose apparatus words."""
    with tempfile.TemporaryDirectory() as tmp:
        mgr = SandboxManager(tmp)
        run_path = mgr.create_apparatus_minimized_run()

        world = run_path / "agent_view" / "WORLD.md"
        assert world.exists()
        content = world.read_text(encoding="utf-8")
        assert "World Fragment" in content
        forbidden = ["operator", "source/library", "experiment",
                     "framework", "apparatus", "review loop"]
        for word in forbidden:
            assert word.lower() not in content.lower(), (
                f"WORLD.md contains apparatus word: {word}"
            )


def test_a2_wake_md_no_apparatus_language():
    """WAKE.md does not expose apparatus words."""
    with tempfile.TemporaryDirectory() as tmp:
        mgr = SandboxManager(tmp)
        run_path = mgr.create_apparatus_minimized_run()

        content = (run_path / "agent_view" / "WAKE.md").read_text(encoding="utf-8")
        forbidden = ["experiment", "framework", "source/library",
                     "source path", "operator", "review loop", "run.json"]
        for word in forbidden:
            assert word.lower() not in content.lower(), (
                f"WAKE.md contains apparatus word: {word}"
            )


def test_a2_wake_md_supports_reentry():
    """WAKE.md supports participant re-entry by mentioning existing traces/HELLO.md."""
    with tempfile.TemporaryDirectory() as tmp:
        mgr = SandboxManager(tmp)
        run_path = mgr.create_apparatus_minimized_run()

        content = (run_path / "agent_view" / "WAKE.md").read_text(encoding="utf-8")
        assert "HELLO.md" in content
        assert "traces left here" in content.lower()
        assert "may later find this place" in content.lower()


def test_a2_operator_run_json():
    """operator/run.json records mode and paths."""
    with tempfile.TemporaryDirectory() as tmp:
        mgr = SandboxManager(tmp)
        run_path = mgr.create_apparatus_minimized_run()

        meta_file = run_path / "operator" / "run.json"
        assert meta_file.exists()
        meta = json.loads(meta_file.read_text(encoding="utf-8"))
        assert meta["mode"] == "apparatus-minimized"
        assert meta["apparatus_visibility"] == "A2-apparatus-minimized"
        assert "agent_view_path" in meta
        assert "operator_path" in meta
        assert "read_only_library_path" in meta


def test_a2_condition_set_records_a2():
    """operator/CONDITION_SET.md records A2 apparatus-minimized."""
    with tempfile.TemporaryDirectory() as tmp:
        mgr = SandboxManager(tmp)
        run_path = mgr.create_apparatus_minimized_run()

        content = (run_path / "operator" / "CONDITION_SET.md").read_text(encoding="utf-8")
        assert "A2" in content
        assert "apparatus-minimized" in content


def test_a2_feedback_prompt_no_apparatus_words():
    """A2 FEEDBACK_PROMPT.md avoids apparatus language in agent-facing prompts."""
    with tempfile.TemporaryDirectory() as tmp:
        mgr = SandboxManager(tmp)
        run_path = mgr.create_apparatus_minimized_run()

        content = (run_path / "operator" / "FEEDBACK_PROMPT.md").read_text(encoding="utf-8")
        # Must have the three templates
        assert "Continue in Same World" in content
        assert "World Fragment Updated" in content
        assert "Correct Apparatus Drift" in content
        # Must NOT have standard-run apparatus language in templates
        assert "source/library" not in content
        assert "experiment" not in content


def test_a2_operator_files_exist():
    """All operator-side files are seeded."""
    with tempfile.TemporaryDirectory() as tmp:
        mgr = SandboxManager(tmp)
        run_path = mgr.create_apparatus_minimized_run()

        operator_dir = run_path / "operator"
        for fname in ["run.json", "REVIEW_LOOP.md", "OPERATOR_REVIEW.md",
                       "FEEDBACK_PROMPT.md", "CONTINUITY_NOTES.md", "CONDITION_SET.md"]:
            assert (operator_dir / fname).exists(), f"Missing: {fname}"


# ============================================================================
# Detached neutral agent view export tests (feature/detached-neutral-agent-view)
# ============================================================================

from scripts.export_agent_view import (
    validate_run_for_export,
    copy_agent_view,
    write_export_notes,
    _check_path_hygiene,
)


def test_export_validates_agent_view_exists():
    """Export requires agent_view/ in the run."""
    with tempfile.TemporaryDirectory() as tmp:
        run = Path(tmp) / "run-test"
        run.mkdir()
        (run / "operator").mkdir()
        (run / "operator" / "run.json").write_text(
            json.dumps({"mode": "apparatus-minimized"}), encoding="utf-8"
        )
        # No agent_view — should fail
        with pytest.raises(SystemExit):
            validate_run_for_export(run)


def test_export_requires_apparatus_minimized_mode():
    """Export requires mode apparatus-minimized in run.json."""
    with tempfile.TemporaryDirectory() as tmp:
        run = Path(tmp) / "run-test"
        run.mkdir()
        (run / "agent_view").mkdir()
        (run / "operator").mkdir()
        (run / "operator" / "run.json").write_text(
            json.dumps({"mode": "standard-growth"}), encoding="utf-8"
        )
        with pytest.raises(SystemExit):
            validate_run_for_export(run)


def test_export_validates_successfully():
    """A valid A2 run passes validation."""
    with tempfile.TemporaryDirectory() as tmp:
        run = Path(tmp) / "run-test"
        run.mkdir()
        (run / "agent_view").mkdir()
        (run / "operator").mkdir()
        (run / "operator" / "run.json").write_text(
            json.dumps({"mode": "apparatus-minimized"}), encoding="utf-8"
        )
        av, op = validate_run_for_export(run)
        assert av == run / "agent_view"
        assert op == run / "operator"


def test_export_copies_agent_view_files():
    """Export copies WAKE.md and WORLD.md, not operator/ or run.json."""
    with tempfile.TemporaryDirectory() as src_tmp, \
         tempfile.TemporaryDirectory() as tgt_tmp:
        agent_view = Path(src_tmp) / "agent_view"
        agent_view.mkdir()
        (agent_view / "WAKE.md").write_text("# Wake", encoding="utf-8")
        (agent_view / "WORLD.md").write_text("# World", encoding="utf-8")

        target = Path(tgt_tmp) / "room-001"
        copy_agent_view(agent_view, target)

        assert (target / "WAKE.md").exists()
        assert (target / "WORLD.md").exists()
        assert (target / "WAKE.md").read_text(encoding="utf-8") == "# Wake"
        # Must not contain operator or run.json
        assert not (target / "operator").exists()
        assert not (target / "run.json").exists()


def test_export_notes_written():
    """Export writes EXPORT_NOTES.md to operator/."""
    with tempfile.TemporaryDirectory() as tmp:
        operator_dir = Path(tmp) / "operator"
        operator_dir.mkdir()
        target = Path("C:/Worlds/room-001")

        notes = write_export_notes(operator_dir, target, [])
        assert notes.exists()
        content = notes.read_text(encoding="utf-8")
        assert "room-001" in content
        assert "one-way export" in content
        assert "no automatic sync" in content.lower()


def test_path_hygiene_warns_on_apparatus_terms():
    """Path hygiene check flags apparatus-like terms."""
    warnings = _check_path_hygiene(Path("C:/GitHub/experiment/test"))
    assert "github" in warnings
    assert "experiment" in warnings


def test_path_hygiene_clean_on_neutral_path():
    """Path hygiene check passes for neutral paths."""
    warnings = _check_path_hygiene(Path("C:/Worlds/room-001"))
    assert warnings == []


# ============================================================================
# World fragment builder tests (feature/world-fragment-builder)
# ============================================================================

from scripts.build_world_fragment import (
    build_world_md,
    write_world_md,
    write_source_note,
    resolve_safe,
    validate_a2_run,
    list_library_files,
)


def test_build_world_md_from_source_files():
    """build_world_md produces world-facing content from source files."""
    with tempfile.TemporaryDirectory() as lib_tmp:
        lib = Path(lib_tmp)
        (lib / "one.md").write_text("# One\n\nContent one.", encoding="utf-8")
        (lib / "two.md").write_text("# Two\n\nContent two.", encoding="utf-8")

        content = build_world_md(str(lib), ["one.md", "two.md"])
        assert "World Fragment" in content
        assert "Fragment 1" in content
        assert "Fragment 2" in content
        assert "Content one" in content
        assert "Content two" in content
        assert lib_tmp not in content  # no real path exposed


def test_build_world_md_no_source_path_leak():
    """WORLD.md does not include the real source path."""
    with tempfile.TemporaryDirectory() as lib_tmp:
        lib = Path(lib_tmp)
        (lib / "notes.md").write_text("Some notes.", encoding="utf-8")

        content = build_world_md(str(lib), ["notes.md"])
        assert str(lib) not in content
        assert "Fragment 1" in content


def test_write_world_md():
    """write_world_md writes content to agent_view/WORLD.md."""
    with tempfile.TemporaryDirectory() as tmp:
        av = Path(tmp)
        write_world_md(av, "# World\n\nContent.")
        world = av / "WORLD.md"
        assert world.exists()
        assert "Content" in world.read_text(encoding="utf-8")


def test_write_source_note_records_provenance():
    """WORLD_SOURCE_NOTE.md records source path and files on operator side."""
    with tempfile.TemporaryDirectory() as tmp:
        op = Path(tmp)
        note = write_source_note(op, "/fake/library", ["a.md", "b.md"], "World")
        assert note.exists()
        content = note.read_text(encoding="utf-8")
        assert "/fake/library" in content
        assert "a.md" in content
        assert "b.md" in content
        assert "operator-side provenance" in content
        assert "build_world_fragment.py" in content


def test_resolve_safe_breakout_rejected():
    """Path breakout from library root is rejected."""
    with tempfile.TemporaryDirectory() as lib_tmp:
        with pytest.raises(SystemExit):
            resolve_safe(lib_tmp, "../escape.md")


def test_resolve_safe_valid_path():
    """Valid relative paths resolve correctly."""
    with tempfile.TemporaryDirectory() as lib_tmp:
        lib = Path(lib_tmp).resolve()
        (lib / "sub").mkdir()
        (lib / "sub" / "f.md").write_text("ok", encoding="utf-8")
        resolved = resolve_safe(str(lib), "sub/f.md")
        assert resolved == lib / "sub" / "f.md"


def test_validate_a2_run_rejects_standard_growth():
    """validate_a2_run rejects non-A2 runs."""
    with tempfile.TemporaryDirectory() as tmp:
        run = Path(tmp) / "run-test"
        run.mkdir()
        (run / "agent_view").mkdir()
        (run / "operator").mkdir()
        (run / "operator" / "run.json").write_text(
            json.dumps({"mode": "standard-growth"}), encoding="utf-8"
        )
        with pytest.raises(SystemExit):
            validate_a2_run(run)


def test_list_library_files_discovers_md_and_txt():
    """list_library_files finds .md and .txt recursively, sorted."""
    with tempfile.TemporaryDirectory() as lib_tmp:
        lib = Path(lib_tmp).resolve()
        (lib / "a.md").write_text("a", encoding="utf-8")
        (lib / "sub").mkdir()
        (lib / "sub" / "b.txt").write_text("b", encoding="utf-8")
        (lib / "c.py").write_text("c", encoding="utf-8")  # ignored

        files = list_library_files(str(lib))
        assert files[0] == "a.md"
        assert "b.txt" in files[1]


def test_list_library_files_empty():
    """list_library_files returns empty for dir with no .md/.txt."""
    with tempfile.TemporaryDirectory() as lib_tmp:
        lib = Path(lib_tmp).resolve()
        (lib / "notes.py").write_text("code", encoding="utf-8")
        assert list_library_files(str(lib)) == []


def test_write_source_note_whole_library():
    """WORLD_SOURCE_NOTE records whole-library mode."""
    with tempfile.TemporaryDirectory() as tmp:
        op = Path(tmp)
        note = write_source_note(
            op, "/fake/lib", ["a.md", "b.md"], "World",
            total_chars=5000, is_whole_library=True,
        )
        content = note.read_text(encoding="utf-8")
        assert "whole-library" in content
        assert "Files included: 2" in content
        assert "Total characters: 5000" in content


# ============================================================================
# Per-run library path override (feature/run-condition-declaration patch)
# ============================================================================


def test_sandbox_default_uses_config_library_path():
    """When no library_path is given, the config default is used."""
    with tempfile.TemporaryDirectory() as tmp:
        mgr = SandboxManager(tmp)
        run_path = mgr.create_run()

        # instructions.txt should contain the config default path
        from src.config import READ_ONLY_LIBRARY_PATH
        content = (run_path / "instructions.txt").read_text(encoding="utf-8")
        assert str(READ_ONLY_LIBRARY_PATH.resolve()) in content

        # run.json should contain the config default path
        meta = json.loads((run_path / "run.json").read_text(encoding="utf-8"))
        assert meta["read_only_library_path"] == str(READ_ONLY_LIBRARY_PATH.resolve())


def test_sandbox_custom_library_path_in_instructions():
    """A custom library_path appears in the generated instructions.txt."""
    with tempfile.TemporaryDirectory() as sandbox_tmp, \
         tempfile.TemporaryDirectory() as lib_tmp:
        lib_path = Path(lib_tmp).resolve()
        (lib_path / "README.md").write_text("# Test Library", encoding="utf-8")

        mgr = SandboxManager(sandbox_tmp, read_only_library_path=str(lib_path))
        run_path = mgr.create_run()

        content = (run_path / "instructions.txt").read_text(encoding="utf-8")
        assert str(lib_path) in content


def test_sandbox_custom_library_path_in_run_json():
    """A custom library_path appears in the generated run.json."""
    with tempfile.TemporaryDirectory() as sandbox_tmp, \
         tempfile.TemporaryDirectory() as lib_tmp:
        lib_path = Path(lib_tmp).resolve()

        mgr = SandboxManager(sandbox_tmp, read_only_library_path=str(lib_path))
        run_path = mgr.create_run()

        meta = json.loads((run_path / "run.json").read_text(encoding="utf-8"))
        assert meta["read_only_library_path"] == str(lib_path)