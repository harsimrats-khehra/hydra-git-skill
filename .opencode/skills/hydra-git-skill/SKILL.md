---
name: hydra-git-skill
description: Universally isolates, diagnoses, and repairs bugs across local Git repositories or code sandboxes using safe temporary worktrees and local AI inference loops.
license: MIT
compatibility: ollama, git, python3.10+, node, gcc, cargo, go
---

# Hydra-Git Task Protocol

## Intended Triggers
- "Deploy isolated worktree repairs over a target codebase directory"
- "Fix a bug in a local repository without changing my current branch state"
- "Auto-correct syntax or run unit tests on a sandbox layout completely offline"

## Instructions
1. Inspect the incoming request parameters to dynamically choose between Workflow A (Text Sandbox Canvas) or Workflow B (Local Git Repository Engine).
2. For Workflow B, validate the directory root and ensure the target framework matches supported language parameters (`Python`, `JavaScript`, `Java`, `C`, `C++`, `Go`, `Rust`).
3. Spawns an isolated Git Worktree in the host computer's temporary cache folder (`tempfile`). This guarantees the user's active editor files remain entirely safe and untouched.
4. Route context parameters to the configurable local Ollama model instance to parse minimal code diff modifications.
5. Execute targeted compilation validation checks and custom user-provided verification shell commands.
6. Return high-fidelity verification signals: `Syntax Valid`, `Tests Passed`, `Tests Failed`, or `Not Verified`.
7. Auto-author descriptive Git commit updates using the AI model, and instruct the user on how to cleanly review or merge the patch branch when ready.
