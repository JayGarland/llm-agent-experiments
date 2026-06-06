"""
Unit Tests for the Base Experiment Framework.
"""

import os
import pytest
from pathlib import Path
import tempfile
import json
from src.sandbox import SandboxManager
from src.library import _resolve_safe_path, list_library_files, LibraryAccessError
from src.config import READ_ONLY_LIBRARY_PATH

def test_sandbox_creation_and_population():
    """
    Verifies that SandboxManager correctly makes a unique directory,
    populates instructions, and registers log metadata.
    """
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_root = Path(temp_dir)
        manager = SandboxManager(sandbox_root=temp_root)
        
        # Test creation of run directory
        run_path = manager.create_run_directory()
        assert run_path.exists()
        assert run_path.is_dir()
        assert "run-" in run_path.name
        
        # Test population
        prompt_file = manager.populate_run_directory(run_path)
        assert prompt_file.exists()
        assert "LLM AGENT FREE-DIRECTORY EXPERIMENT INSTRUCTIONS" in prompt_file.read_text(encoding="utf-8")

def test_library_safe_path_resolution():
    """
    Verifies that safe path resolution raises errors if an escape is attempted.
    """
    # Safe sub-path relative to library base
    safe_path = _resolve_safe_path("index.md")
    assert safe_path.exists()
    assert safe_path.is_file()

    # Escape attempt: outside of library path should throw a LibraryAccessError
    with pytest.raises(LibraryAccessError):
        _resolve_safe_path("../../../etc/passwd")

def test_list_library_files():
    """
    Verifies that library file loading lists files within sample structures.
    """
    files = list_library_files()
    assert len(files) > 0
    # Ensure standard files are matched
    assert "index.md" in files
    assert "current_state.md" in files
    assert "trace.md" in files
