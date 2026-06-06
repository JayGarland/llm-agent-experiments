# Platform Fit Summary

This document captures the Platform Scout assessment of which AI agent
platforms are best suited for Version A + read-only source/library experiments.

---

## Key Insight

**Platform choice is a run condition, not just an implementation detail.**
Different platforms have different default identities, tool sets, and output
attractors. These shape the experiment as much as the prompt does.

> **Warning:** Most existing AI agent platforms are **coding-agent first**.
> They default to producing software, tools, and executable artifacts even
> when the experiment does not demand them.

---

## Current Near-Term Platform

### GitHub Copilot Agent in VS Code (Markdown-Only Directory Mode)

**Status:** Current near-term default.

**Strengths:**
- Existing empirical data from Runs 001–008 provides a proven baseline.
- Low friction in the current workflow — no new tool adoption needed.
- Markdown-only / no-executable / source-as-soil constraints effectively
  reduce coding collapse.

**Weaknesses:**
- Strong coding-agent bias by default — requires explicit constraints.
- Full-tools mode produces the strongest coding/utility collapse.

**Recommendation:** Continue as primary platform with Markdown-only +
source-as-soil constraints. Use full-tools mode only as a baseline
contrast condition.

---

## High-Priority Contrast Platform

### Claude Code

**Status:** High-priority same-prompt contrast — **not** confirmed as best.

**Why it matters:**
- Claude Code has a more explicit permission system than Copilot, which
  may interact differently with workspace-boundary constraints.
- It is closer to the original Karpathy/Claude environment, making it a
  meaningful contrast for same-prompt comparison.
- Still a coding agent — not a neutral free-directory platform.

**Recommendation:** Test later with the exact same prompt used in Run 008
(Markdown-only source-as-soil). Compare HELLO.md, TRACE.md, and output
attractor against the Copilot baseline.

---

## Modifiable Open-Source Candidate

### Crush (Charmbracelet)

**Status:** Modifiable candidate — **not** ideal default.

**Why it matters:**
- Open source — can be modified and adapted.
- Provider-flexible — not locked to a single model vendor.
- Terminal-first — closer to a minimal directory environment.

**Limitations:**
- Default identity remains coding assistant.
- Smaller community and fewer existing experiments.

**Recommendation:** Treat as a modifiable candidate. Consider after
establishing a solid baseline on Copilot and a contrast on Claude Code.

---

## Future Direction

### Minimal Custom Harness

**Status:** Long-term direction.

**Why:**
- Most existing platforms are coding-agent first.
- A custom harness could provide:
  - Configurable tool sets (read-only, write-only, no-exec, etc.).
  - Neutral system identity (not "coding assistant").
  - Stable reproducible run conditions across providers.
  - Full control over workspace boundary enforcement.

**Recommendation:** Defer until empirical patterns are well-established.
Do not build a custom harness prematurely — let the experiments inform
what the harness needs to be.

---

## Platform Comparison

| Platform | Coding bias | Permission model | Open source | Current use |
|---|---|---|---|---|
| GitHub Copilot Agent | High | Implicit / tool-based | No | Near-term default |
| Claude Code | High | Explicit | No | High-priority contrast |
| Crush | High | Configurable | Yes | Modifiable candidate |
| Custom harness | Configurable | Full control | Yes | Long-term direction |
