import os
import subprocess
import gradio as gr
import ollama

def run_git_cmd(args):
    # Safely executes git operations behind the scenes
    return subprocess.run(args, capture_output=True, text=True)

def complete_agent_pipeline(file_name, error_stack):
    if not file_name or not os.path.exists(file_name):
        return "❌ Error: Please provide a valid file path inside this folder."
        
    try:
        # 1. Clean workspace & handle Git branches locally 
        run_git_cmd(["git", "checkout", "-B", "main"])
        run_git_cmd(["git", "add", "."])
        run_git_cmd(["git", "commit", "-m", "chore: dashboard auto-save"])
        
        # 2. Re-create the background ghost branch cleanly
        run_git_cmd(["git", "branch", "-D", "hydra/ghost-patch-fix"])
        run_git_cmd(["git", "checkout", "-b", "hydra/ghost-patch-fix"])
        
        # 3. Read the code file content
        with open(file_name, "r", encoding="utf-8") as f:
            broken_source = f.read()
            
        # 4. Generate precision fix via your local Llama 3.2 model
        prompt = f"Fix this script code. SOURCE:\n{broken_source}\n\nERROR:\n{error_stack}\n\nOutput ONLY valid code inside blocks. No conversations."
        response = ollama.chat(model='llama3.2', messages=[{'role': 'user', 'content': prompt}])
        cleaned_code = response['message']['content']
        
        # Clean standard model wrapper markers safely
        if "```python" in cleaned_code:
            cleaned_code = cleaned_code.split("```python")[1].split("```")[0].strip()
        elif "```" in cleaned_code:
            cleaned_code = cleaned_code.split("```")[1].split("```")[0].strip()
            
        # 5. Overwrite with the corrected version
        with open(file_name, "w", encoding="utf-8") as f:
            f.write(cleaned_code)
            
        # 6. Commit the fixes to the background branch and restore main
        run_git_cmd(["git", "add", file_name])
        run_git_cmd(["git", "commit", "-m", "feat(hydra): automated browser interface patch complete"])
        run_git_cmd(["git", "checkout", "main"])
        
        return f"🚀 Success! Clean code changes committed seamlessly in the background.\n\n### 💻 Newly Repaired Code Content:\n```python\n{cleaned_code}\n```"
        
    except Exception as e:
        # Fallback tracking if anything locks up
        run_git_cmd(["git", "checkout", "main"])
        return f"❌ Pipeline Execution Failure: {str(e)}"

# Assemble the UI layout presentation blocks
with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 🧬 Hydra-Git: Autonomous Ghost-Developer Dashboard")
    gr.Markdown("*Compliant with Agent Skill Open Standards running 100% locally via Llama 3.2 (3B).*")
    
    with gr.Row():
        with gr.Column():
            input_file = gr.Textbox(label="Target Code File Path", value="app_module.py")
            input_error = gr.Textbox(label="Terminal Error Message", placeholder="e.g., NameError: name 'data_payload' is not defined")
            submit_btn = gr.Button("Deploy Background Developer Agent", variant="primary")
        
        with gr.Column():
            output_display = gr.Markdown(label="Real-time Agent Telemetry")
            
    submit_btn.click(fn=complete_agent_pipeline, inputs=[input_file, input_error], outputs=output_display)

if __name__ == "__main__":
    demo.launch()
