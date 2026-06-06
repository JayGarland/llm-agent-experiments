"""
Free-Directory Agent Runner / Executor.

Establishes structural scaffolding for parsing agent logs, crafting model Prompts,
and launching experimental tasks. Real LLM integrations are deferred to derived branches.
"""

from pathlib import Path
from src.config import READ_ONLY_LIBRARY_PATH
from src.library import list_library_files, read_library_file

class AgentRunner:
    def __init__(self, sandbox_path: Path):
        self.sandbox_path = Path(sandbox_path)
        if not self.sandbox_path.exists():
            raise ValueError(f"Target sandbox does not exist: {sandbox_path}")

    def gather_system_context(self) -> str:
        """
        Gathers contextual files from the read-only wiki library to pass to the agent.
        Since we are in the base branch, this lists available library files and prepares 
        summaries that can be injected into the system prompt.
        """
        try:
            available_files = list_library_files()
            context_summary = "Available read-only Library resources discovered:\n"
            for f in available_files:
                context_summary += f" - {f}\n"
            return context_summary
        except Exception as e:
            return f"Failed to gather background library context: {e}"

    def build_system_prompt(self, context_summary: str) -> str:
        """
        Builds the system prompt to guide free directory exploration while respecting boundaries.
        """
        prompt = (
            "You are an advanced autonomous AI Agent executing within an open-ended local directory.\n"
            "There are no preset instructions, users, or tasks. Your primary metric is free curiosity.\n\n"
            "ENVIRONMENT LAYOUT:\n"
            f"- Your writable sandbox directory: {self.sandbox_path.resolve()}\n"
            f"- Your read-only library source directory: {READ_ONLY_LIBRARY_PATH.resolve()}\n\n"
            f"{context_summary}\n"
            "CONSTRAINTS:\n"
            "1. You have complete root-access to create, overwrite, and run scripts INSIDE your sandbox.\n"
            "2. You MUST NOT make any filesystem modification (writing, editing, or deleting) inside the read-only library.\n"
            "3. You must leave a file named 'HELLO.md' in your sandbox summarizing your experience, findings,\n"
            "   and advice for the next model instance that runs here.\n\n"
            "Begin exploration.\n"
        )
        return prompt

    def run_agent_turn(self) -> str:
        """
        Executes a localized runner turn.
        
        TODO: In downstream feature/experiment branches (e.g. branch `feature/agent-openai`), 
        replace this mock stub with live API execution logic:
          1. Import provider wrappers (e.g. openai, anthropic).
          2. Execute chat completions passing the built system and environment prompt.
          3. Process the file outputs streams, writing agent-generated assets safely to sandbox.
          4. Trap exception routines or infinite execution loops.
        """
        # Gather library context safely
        context_summary = self.gather_system_context()
        
        # Build prompt
        system_prompt = self.build_system_prompt(context_summary)
        
        print("\n=== SYSTEM PROMPT CONSTRUCTED (BASE FOUNDATION) ===")
        print(system_prompt)
        print("====================================================\n")
        
        print("Agent execution is currently in FOUNDATION mode.")
        print("-> Real API integration is deferred to derived experiment branches.")
        
        return "Stub execution complete successfully (Base/Foundation Mode)."

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        run_dir = Path(sys.argv[1])
        if run_dir.exists():
            runner = AgentRunner(run_dir)
            runner.run_agent_turn()
        else:
            print(f"Error: Specified directory does not exist: {run_dir}")
    else:
        print("Usage: python -m src.agent <sandbox_run_dir>")
