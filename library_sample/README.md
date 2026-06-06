# Sample Local sub LLM-Wiki (Read-Only)

This directory represents a sample of a local sub LLM-Wiki project that acts as the "source/library" for the AI Agent.

In full runs, this library path can be configured to point to a real knowledge base, research dump, or documentation repository. This directory is intended for read-only access at the interface/documentation level; OS-level enforcement is future work. The agent may inspect and read files to guide its exploration, but it must not modify, add, or delete any content within this library.

## Structure of the sub LLM-Wiki

A typical sub LLM-Wiki contains:

- `index.md`: Entry point of the wiki containing top-level navigation, map, or guidelines.
- `current_state.md`: Active tracking file recording what the system (or developer) is currently working on or tracking.
- `trace.md`: A historical timeline or audit trail of modifications, updates, or entries.
- `notes/`: Directory containing specific markdown files with deep-dive topics, ideas, or structured knowledge.
- `raw/`: Unorganized resource materials, logs, or reference downloads.
