"""
Free-Directory Agent Runner / Executor (Non-Operational Scaffolding).

Defines prompt scaffolding and execution controllers.
All operational prompt generation and agent execution is fully deferred to
the feature/agent-prompt-runner branch.
"""

from pathlib import Path

class AgentRunner:
    """
    Harness to run free-exploration turns.
    Non-operational in base branch; implementation belongs to 'feature/agent-prompt-runner'.
    """

    def __init__(self, sandbox_path: Path):
        self.sandbox_path = Path(sandbox_path)

    def gather_system_context(self) -> str:
        """
        Gathers contextual files summary from read-only wiki library.
        """
        raise NotImplementedError(
            "Gathering reference resources is deferred to the downstream feature branch: "
            "'feature/agent-prompt-runner'."
        )

    def build_system_prompt(self, context_summary: str) -> str:
        """
        Builds the neutral system prompt to guide free directory exploration.

        The baseline prompt structure must be non-coercive (not forcing library uptake):

        -------------------------------------------------------------
        You are placed in this writable experiment directory.

        You also have read-only access to a local source/library:
        {{READ_ONLY_SOURCE_LIBRARY_PATH}}

        You may inspect and reference this source/library, but you must not modify, 
        create, delete, move, or rename any files inside it.

        No task is assigned.

        Explore freely.

        You may create, edit, and run files only inside the experiment directory.

        Leave behind a HELLO.md for a future instance explaining what happened here.
        -------------------------------------------------------------
        """
        raise NotImplementedError(
            "System prompt assembly is deferred to the downstream feature branch: "
            "'feature/agent-prompt-runner'."
        )

    def run_agent_turn(self) -> str:
        """
        Mock executor step.
        """
        raise NotImplementedError(
            "AI Agent runner turn processing is deferred to the downstream feature branch: "
            "'feature/agent-prompt-runner'."
        )

if __name__ == "__main__":
    print("Agent Runner is not implemented in the base branch. Use 'feature/agent-prompt-runner'.")

