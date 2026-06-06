## Platform Scout Decision

Status: accepted scout result.

Current near-term platform:
GitHub Copilot Agent in VS Code, constrained by Markdown-only directory mode.

Reason:
The current project already has empirical run data from Runs 001–008. Although Copilot has strong coding-agent bias, the Markdown-only / no-executable / source-as-soil condition currently provides the best practical balance between real directory traces and reduced utility collapse.

High-priority contrast platform:
Claude Code.

Reason:
Claude Code remains a coding agent, but its explicit permission model and proximity to the Karpathy/Claude-style environment make it the most valuable same-prompt comparison target. It should be tested later with the same Markdown-only Source-as-Soil prompt before any platform migration decision.

Modifiable candidate:
Charmbracelet Crush.

Reason:
Crush is open source and provider-flexible, but its default identity is still coding assistant. Treat it as a possible future modifiable harness source, not as an ideal default platform.

Long-term direction:
Minimal custom harness.

Reason:
Most existing platforms are coding-agent first. If source-as-soil / ghost-continuity experiments require stable non-coding directory behavior, a minimal custom harness may eventually be needed.