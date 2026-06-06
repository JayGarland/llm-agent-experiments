"""
Unit Tests for the Base Experiment Framework (Repaired Scaffolding).
"""

import pytest
from pathlib import Path
import tempfile
from src.library import verify_and_resolve_path, LibraryAccessError, list_library_files, read_library_file
from src.sandbox import SandboxManager
from src.agent import AgentRunner
from src.config import validate_config

def test_robust_path_verification():
    """
    Verifies that the path verification containment utility correctly prevents directory traversal.
    """
    with tempfile.TemporaryDirectory() as temp_dir:
        base_dir = Path(temp_dir).resolve()
        
        # Create a nested file and directory
        nested_dir = base_dir / "nested"
        nested_dir.mkdir()
        nested_file = nested_dir / "test.txt"
        nested_file.write_text("content", encoding="utf-8")
        
        # Verify valid resolves succeed
        resolved = verify_and_resolve_path("nested/test.txt", base_dir)
        assert resolved == nested_file
        
        # Verify path escape attempts raise LibraryAccessError
        with pytest.raises(LibraryAccessError):
            verify_and_resolve_path("../escape.txt", nested_dir)

def test_non_operational_scaffolding_stubs():
    """
    Verifies that all operational methods in the base scaffolding raise NotImplementedError.
    This guarantees that the base branch is strictly non-operational.
    """
    # Config stubs
    with pytest.raises(NotImplementedError):
        validate_config()
        
    # Library stubs
    with pytest.raises(NotImplementedError):
        list_library_files()
        
    with pytest.raises(NotImplementedError):
        read_library_file("index.md")
        
    # Sandbox stubs
    manager = SandboxManager()
    with pytest.raises(NotImplementedError):
        manager.create_run_directory()
        
    with pytest.raises(NotImplementedError):
        manager.populate_run_directory(Path("dummy"))
        
    with pytest.raises(NotImplementedError):
        manager.log_run_metadata(Path("dummy"))
        
    with pytest.raises(NotImplementedError):
        manager.execute_new_run()
        
    # Agent stubs
    runner = AgentRunner(Path("dummy"))
    with pytest.raises(NotImplementedError):
        runner.gather_system_context()
        
    with pytest.raises(NotImplementedError):
        runner.build_system_prompt("dummy_summary")
        
    with pytest.raises(NotImplementedError):
        runner.run_agent_turn()

