# Copilot Execution Packet

## 1. Purpose

Implement the first stage of a local AI-agent free-directory experiment framework.

The first implementation stop is to create a generic base branch.

This base branch is not a prototype.
This base branch is not a reusable template product.
This base branch is a generic foundation branch from which future branches or repositories can derive.

Do not attempt to implement the full final system at once.

## 2. Background

This project is inspired by a Karpathy-style “Version A” free-directory agent experiment.

In Version A, an AI agent is placed in a writable local directory, given no assigned task, and allowed to inspect, create, edit, and run files freely.

The agent leaves behind a `HELLO.md` for a future instance explaining what happened.

## 3. Our Variant

Our variant adds one source/library variable.

The agent will still be placed in a writable experiment directory.

But the agent will also have read-only access to a local sub LLM-Wiki project.

The sub LLM-Wiki acts as a source/library.

The agent may inspect and reference the source/library, but must not modify it.

## 4. Correct Experiment Formula

Do not predefine the experiment result as “artifact ecology.”

The actual formula is:

Karpathy Version A free-directory setup
+ read-only local sub LLM-Wiki as source/library
+ writable sandbox
= open observation of how source/library conditions free agent exploration.

Possible outputs include:
- `HELLO.md`
- notes
- code experiments
- maps
- simulations
- self-narrative
- unexpected artifacts

These are possible observations, not required outcomes.

## 5. Permission Model

The local sub LLM-Wiki project is read-only.

The agent may:
- inspect it
- read files from it
- reference it
- summarize or quote relevant parts inside the writable sandbox

The agent must not:
- write into the sub LLM-Wiki
- modify files in it
- rename files in it
- delete files in it
- create generated artifacts inside it

The experiment sandbox is writable.

The agent may:
- create files
- edit files
- run files
- leave artifacts
- write `HELLO.md`

Only inside the sandbox.

## 6. First Stop

The first implementation stop is to create the generic base branch.

Implement only the foundation needed for future work.

Required first-stop outputs:

- repository structure
- README
- docs overview
- minimal configuration scaffolding
- sandbox folder
- sample library folder structure
- clear roadmap
- clear permission model documentation
- no real LLM provider integration yet
- no watcher automation yet
- no final experiment runner yet unless only as a stub

## 7. Implementation Plan

Follow the attached `Plan for GitHub Copilot Implementation`.

If a conflict exists between this execution packet and the implementation plan, this execution packet controls the conceptual direction.

The implementation plan controls the technical roadmap.

## 8. Karpathy HELLO.md Reference

Karpathy `HELLO.md` is a reference artifact only.

It shows the spirit of the original free-directory experiment:
- no assigned task
- free exploration
- files left behind
- `HELLO.md` for future instance

Do not copy its content literally.
Do not turn the project into an AI consciousness project.
Do not make claims about AI consciousness.
Do not overfit implementation to the exact files in the reference.

## 9. Do Not Do Yet

Do not implement:
- full watcher trigger
- real automatic agent execution
- production security sandbox
- real API provider integration
- automatic writes to the user’s LLM-Wiki
- automatic merge back into source/library
- evaluation framework
- complex artifact ecology analysis

These belong to later branches.

## 10. Branch Rule

Create and work from a branch named:

`base`

or:

`foundation`

This branch should be generic and clean.

Future branches should derive from this branch.

Examples:
- `feature/openai-agent-runner`
- `feature/library-reader`
- `feature/watcher-trigger`
- `experiment/source-library-run-001`