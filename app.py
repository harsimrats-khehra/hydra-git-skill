import os
import subprocess
import gradio as gr

def launch_agent_ui(file_name, error_stack):
    if not file_name or not os.path.exists(file_name):
        return "❌ Error: Please provide a valid file path inside this folder."
    try:
        cmd = ["python", "scripts/ghost_runner.py", file_name, error_stack]
        process = subprocess.run(cmd, capture_output=True, text=True, check=True)
        script_output = process.stdout
        with open(file_name, "r") as f:
            fixed_code = f.read()
        return f"### Agent Action Log:\n{script_output}\n\n### 💻 Updated Code:\n```python\n{fixed_code}\n```"
    except Exception as e:
        return f"❌ Pipeline Execution Failure: {str(e)}"

with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 🧬 Hydra-Git: Autonomous Ghost-Developer Dashboard")
    gr.Markdown("*Compliant with Agent Skill Open Standards running 100% locally via Llama 3.2 (3B).*")
    with gr.Row():
        with gr.Column():
            input_file = gr.Textbox(label="Target Code File Path", value="app_module.py")
            input_error = gr.Textbox(label="Terminal Error Message", placeholder="e.g., NameError: name 'payload' is not defined")
            submit_btn = gr.Button("Deploy Background Developer Agent", variant="primary")
        with gr.Column():
            output_display = gr.Markdown(label="Real-time Agent Telemetry")
    submit_btn.click(fn=launch_agent_ui, inputs=[input_file, input_error], outputs=output_display)

if __name__ == "__main__":
    demo.launch()
