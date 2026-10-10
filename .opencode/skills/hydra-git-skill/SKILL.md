\---

name: hydra-git-skill

description: Asynchronously fixes code errors on background git branches completely offline.

license: MIT

compatibility: ollama-llama3.2, git, python3.10+

\---



\# Hydra-Git Task Protocol



\## Intended Triggers

\- "Fix the exception thrown in file project.py"

\- "Auto-fix code without disrupting my current workspace"



\## Instructions

1\. Cache the current project files inside standard Git staging environments.

2\. Initialize an isolated worker branch prefixed with `hydra/`.

3\. Pass the code anomalies downstream to `scripts/ghost\_runner.py` for inference correction.



