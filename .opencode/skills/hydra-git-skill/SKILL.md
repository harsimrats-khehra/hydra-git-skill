---
name: hydra-git-skill
description: Asynchronously fixes code exceptions on isolated background git branches completely offline, utilizing a multi-pass compiler validation self-healing loop.
license: MIT
compatibility: ollama-llama3.2, git, python3.10+
---

# Hydra-Git Task Protocol

## Intended Triggers
- "Fix the exception thrown in file project.py"
- "Auto-fix code errors and run internal compiler safety checks"
- "Deploy the self-healing worker agent over a broken code file"

## Instructions
1. Securely stash any uncommitted changes in the foreground developer workspace.
2. Initialize an isolated worker branch track prefixed with `hydra/ghost-patch-fix`.
3. Pass the target code module and stack trace error logs downstream to the internal pipeline execution engine inside `app.py`.
4. Trigger the multi-pass compilation loop test suite using `py_compile`.
5. If syntax violations are caught, re-feed the compiler exception feedback directly back to the local `llama3.2` model up to 3 times until the code heals completely.
6. Commit the verified clean patch adjustments and safely restore the user's main branch workspace context.
