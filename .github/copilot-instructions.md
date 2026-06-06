# Repository Instructions for Copilot

## Project Identity

This repository is a manual experimental framework for:

Karpathy Version A free-directory setup
+ read-only local source/library
+ writable sandbox
= open observation of how source/library conditions free agent exploration.

This is not:
- a production automation framework
- a watcher/trigger system
- an agent runner
- a provider integration project
- an automatic Obsidian updater
- an AI consciousness proof project

## Branch Discipline

Do not make feature changes directly on `base` unless explicitly asked.

Prefer derived branches:
- `feature/*`
- `docs/*`
- `scout/*`
- `experiment/*`
- `fix/*`

## Source/Library Boundary

The source/library is read-only.

The writable space is the current `sandbox/run-*` directory.

Do not design features that write into the source/library unless explicitly asked.

## Manual Sync Rule

Any operational behavior change requires a manual impact check.

Operational behavior includes:
- `scripts/prepare_manual_run.py`
- `src/sandbox.py`
- generated `instructions.txt`
- generated `run.json`
- `READ_ONLY_LIBRARY_PATH`
- `--library-path`
- `src/library.py`
- run directory isolation
- continuation prompt flow
- source/library path verification
- workspace boundary instructions

When operational behavior changes, inspect:

- `docs/manuals/user-manual.en.md`
- `docs/manuals/jie-personal-manual.zh.md`

Then either:
1. update the manuals in the same change, or
2. explicitly report why no manual update is needed.