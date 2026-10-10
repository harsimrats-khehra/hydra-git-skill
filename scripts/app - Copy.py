import gradio as gr
from scripts.pipeline import run_workflow_a_sandbox, run_workflow_b_repository

with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 🧬 Hydra-Git: Enterprise-Grade Self-Healing Worktree Dashboard")
    gr.Markdown("*Compliant with Agent Skill Open Standards running 100% locally via Isolated Git Worktrees safely.*")
    
    with gr.Row():
        model_dropdown = gr.Dropdown(
            label="🤖 Configured Ollama Model Target",
            choices=["llama3.2", "qwen2.5:7b", "llama3.1", "mistral"],
            value="llama3.2"
        )
        lang_dropdown = gr.Dropdown(
            label="🌐 Development Language Toolchain",
            choices=["Python", "JavaScript", "Java", "C", "C++", "Go", "Rust"],
            value="Python"
        )

    with gr.Tab("Workflow A: Pasted Sandbox Editor"):
        with gr.Row():
            with gr.Column():
                code_editor = gr.Textbox(label="💻 Raw Code Sandbox Canvas", lines=8, placeholder="Paste your broken module source code text here...")
                error_input_a = gr.Textbox(label="🚨 Terminal Exception Trace Logs", placeholder="Paste crash error logs text structures...")
                submit_btn_a = gr.Button("Process Sandbox Fix", variant="primary")
                telemetry_a = gr.Markdown(label="System Status Monitoring Log Stream")
            with gr.Column():
                diff_display_a = gr.HTML(label="Visual Code Patch Telemetry Structure Map")
                
        submit_btn_a.click(
            fn=run_workflow_a_sandbox,
            inputs=[lang_dropdown, code_editor, error_input_a, model_dropdown],
            outputs=[telemetry_a, diff_display_a]
        )

    with gr.Tab("Workflow B: Production Git Worktree Repository"):
        with gr.Row():
            with gr.Column():
                repo_path_input = gr.Textbox(label="📁 Target Project Root Directory Pathway", placeholder="e.g., C:/Users/name/my_project")
                target_file_rel = gr.Textbox(label="📄 Target File Path (Relative to Repository)", placeholder="e.g., src/main.py")
                error_input_b = gr.Textbox(label="🚨 Terminal Execution Error Logs", placeholder="Paste your standard tracking failure log blocks...")
                test_cmd_input = gr.Textbox(label="🛠️ Verification Test Command Script", placeholder="e.g., pytest tests/test_main.py")
                submit_btn_b = gr.Button("Deploy Isolated Worktree Repair Loop", variant="primary")
                telemetry_b = gr.Markdown(label="System Status Monitoring Log Stream")
            with gr.Column():
                diff_display_b = gr.HTML(label="Visual Code Patch Telemetry Structure Map")
                
        submit_btn_b.click(
            fn=run_workflow_b_repository,
            inputs=[repo_path_input, target_file_rel, error_input_b, test_cmd_input, model_dropdown, lang_dropdown],
            outputs=[telemetry_b, diff_display_b]
        )

if __name__ == "__main__":
    demo.launch()
