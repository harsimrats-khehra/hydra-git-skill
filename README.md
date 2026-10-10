# 🧬 Hydra-Git: Enterprise-Grade Self-Healing Worktree Dashboard

An offline, open-source AI developer agent framework that automates contextual software repairs across raw text sandboxes or live local Git repositories. Utilizing **Isolated Git Worktrees** and local Small Language Models (SLMs), Hydra-Git securely compiles, tests, and validates code updates completely in the background without disturbing the developer's main editor workspace.

---

## 🚀 Architectural Pillars & Innovations

* **Isolated Git Worktree Operations:** Never force-switches or updates active development branches directly. All patches are processed in isolated, transient file tree directories securely detached from the foreground workspace.
* **Dual-Workflow Architecture:**
  * **Workflow A (Pasted Sandbox):** A zero-dependency web canvas input text area to test code blocks and view immediate visual structural adjustments.
  * **Workflow B (Repository Agent):** Interacts natively with active local software codebases, parsing file structures, routing commands to background pipelines, and running automated test validations.
* **Granular Verification Matrix:** Clearly prints compilation flags and tests metrics as `Syntax Valid`, `Tests Passed`, `Tests Failed`, or `Not Verified`.
* **Configurable Ollama Core Engine:** Eliminates hardcoded model variables, allowing effortless hot-swapping between `llama3.2`, `qwen2.5`, or alternative local inference backends completely offline.
* **Visual Diff Analyzer Canvas:** Implements side-by-side color-coded markers (Insertions vs Deletions) to make code audit cycles accessible.

---

## 🛠️ Project Workspace Layout

This package strictly satisfies the folder configuration patterns demanded by the **Agent Skill Open Standard** specification format:
* `.opencode/skills/hydra-git-skill/SKILL.md`: Core system metadata definitions, triggering anchors, and instructions.
* `app.py`: Integrated launcher layout constructing the Gradio UI blocks canvas framework.
* `scripts/`: Modular engine directory tracking safe git structures (`git_engine.py`), model connections (`ai_connector.py`), and polyglot validators (`validator.py`).

---

## 📦 Production Deployment Guide

1. **Clone the Project Core:**
   ```bash
   git clone https://github.com
   cd hydra-git-skill
   ```
2. **Boot the Local Model Host Engine:**
   ```bash
   ollama run llama3.2
   ```
3. **Install Dependencies Matrix:**
   ```bash
   pip install gradio ollama diff-match-patch
   ```
4. **Launch the Visual Server Dashboard:**
   ```bash
   python app.py
   ```
   *Open `http://127.0.0.1:7860` inside your web browser to access the control interface.*
