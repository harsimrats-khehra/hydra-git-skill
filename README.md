# 🧬 Hydra-Git: Autonomous Self-Healing Developer Agent

An offline, open-source AI developer agent framework that listens to terminal runtime stack traces, isolates bugs on dynamic background Git worker branches, and executes an automated, multi-pass **Self-Healing Code Compilation Loop** without disrupting the main workspace. 

Built entirely to comply with the **Agent Skill Open Standard**, this solution leverages highly optimized local Small Language Models (SLMs) to deliver enterprise-grade automation safely inside low-memory local hardware environments.

---

## 🚀 Key Innovation Pillars

* **Self-Healing Compilation Engine:** The agent doesn't just guess a fix; it actively tests its own code using a background python compiler check (`py_compile`). If the code fails syntax validation, it feeds the new error logs back into the AI model, looping up to **3 iterations** until the code is verified clean.
* **Zero Workspace Disruption:** Avoids application thread freezes by running inference workflows on isolated `hydra/` Git branch configurations.
* **100% Data Privacy:** Processes data completely offline using local hardware frameworks—zero external API keys or remote server connections required.
* **Snappy UX Dashboard:** Packaged inside a browser interface layer using Gradio to display real-time self-healing attempt loops and code streaming windows.
* **Hardware Calibrated:** Engineered from the ground up to fit within restricted GPU environments (e.g., NVIDIA RTX 3050 4GB VRAM) without spilling over into sluggish system RAM offloads.

---

## 🛠️ Architecture & Specifications

This repository strictly conforms to the portable, bundle-based directory setup demanded by the Open Agent Skill Specifications:
* `.opencode/skills/hydra-git-skill/SKILL.md`: Core Natural Language protocol mapping, capability anchors, and system frontmatter definitions.
* `app.py`: Integrated single-layer execution pipeline, visual browser interface, and the **Self-Healing core logic**.
* `scripts/`: Production-grade helper logic arrays for managing Git workspace states.

---

## 💻 Technical Prerequisites

Before deploying the pipeline workspace, ensure your laptop environment satisfies these software runtime baselines:
* **Operating System:** Windows 11 / Linux
* **AI Core Backend:** [Ollama Framework](https://ollama.com) running the `llama3.2:3b` model weights.
* **Language Runtime:** Python 3.10+ and standard Git command-line interfaces.

---

## 📦 Local Deployment Instructions

1. **Clone the Core Workspace Artifacts:**
   ```bash
   git clone https://github.com
   cd hydra-git-skill
   ```

2. **Boot the AI Model Backbone Server:**
   ```bash
   ollama run llama3.2
   ```

3. **Install Visual UI Dependencies:**
   ```bash
   pip install gradio ollama
   ```

4. **Launch the Local Core Server App Engine:**
   ```bash
   python app.py
   ```
   *Navigate to your local browser network link (typically `http://127.0.0.1:7860`) to deploy your agent hooks manually.*

---

## 📝 Open-Source Licensing
Distributed under the permissive open-source **MIT License**. Check the root `LICENSE` file metadata details for terms of compliance guidelines.
