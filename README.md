# 🧬 Hydra-Git: Universal Polyglot Self-Healing Developer Agent

An offline, open-source AI developer agent framework that listens to terminal runtime stack traces, isolates bugs on dynamic background Git worker branches, and executes an automated, multi-pass **Universal Polyglot Self-Healing Compilation Loop** without disrupting the main workspace environment.

---

## 🚀 Key Innovation Pillars

* **Polyglot Compiler Integrations:** Leverages native system validation pipelines for **Python, JavaScript, Java, C, C++, Rust, and Go**.
* **Self-Healing Loop Architecture:** Compiles patch code using the chosen language runner and loops back to the AI up to **3 iterations** if compiler syntax failures occur.
* **Contextual AI Commit Autoring:** Generates explanatory engineering git logs automatically.
* **Interactive Code Sandbox:** Implements a web sandbox terminal layer via Gradio for real-time tracking.
* **100% Secure Local Execution:** Fully functional offline using [Ollama](https://ollama.com) with `llama3.2:3b`.

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
   pip install gradio ollama diff-match-patch
   ```
4. **Launch the Local Core Server App Engine:**
   ```bash
   python app.py
   ```
