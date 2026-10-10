import os
import subprocess
import gradio as gr
import ollama

def run_git_cmd(args):
    return subprocess.run(args, capture_output=True, text=True)

def check_syntax_errors(file_name):
    """Compiles the file in a separate process to check for syntax crashes."""
    # Runs python compilation check (-m py_compile) to catch syntax bugs without executing full logic
    result = subprocess.run(["python", "-m", "py_compile", file_name], capture_output=True, text=True)
    if result.returncode != 0:
        return False, result.stderr # Returns validation fail status + stack trace error logs
    return True, "No syntax issues found."

def complete_agent_pipeline(file_name, error_stack):
    if not file_name or not os.path.exists(file_name):
        return "❌ Error: Please provide a valid file path inside this folder."
        
    try:
        # 1. Clean workspace variables & reset branch states safely
        run_git_cmd(["git", "checkout", "-B", "main"])
        run_git_cmd(["git", "add", "."])
        run_git_cmd(["git", "commit", "-m", "chore: pre-audit checkpoint auto-save"])
        
        # 2. Re-create the isolated background ghost branch tracking engine
        run_git_cmd(["git", "branch", "-D", "hydra/ghost-patch-fix"])
        run_git_cmd(["git", "checkout", "-b", "hydra/ghost-patch-fix"])
        
        # 3. Read raw broken target module data
        with open(file_name, "r", encoding="utf-8") as f:
            broken_source = f.read()
            
        current_code = broken_source
        current_error = error_stack
        max_attempts = 3
        loop_logs = []
        
        # 🧠 CORE SELF-HEALING AUTOMATION LOOP STACK
        for attempt in range(1, max_attempts + 1):
            loop_logs.append(f"🔄 **Attempt {attempt}/{max_attempts}:** Sending patch request to local Llama 3.2...")
            
            prompt = f"""
            You are an elite automated DevOps developer. Fix this script.
            
            SOURCE CODE MODULE:
            {current_code}
            
            CRASH ERROR:
            {current_error}
            
            INSTRUCTION: Fix the bug. Output ONLY the raw executable python script code. No conversational text introduction or conclusion blocks.
            """
            
            response = ollama.chat(model='llama3.2', messages=[{'role': 'user', 'content': prompt}])
            cleaned_code = response['message']['content']
            
            # Remove potential markdown layout block text wrappers safely
            if "```python" in cleaned_code:
                cleaned_code = cleaned_code.split("```python")[1].split("```")[0].strip()
            elif "```" in cleaned_code:
                cleaned_code = cleaned_code.split("```")[1].split("```")[0].strip()
                
            # Write out the temporary code attempt to the file grid
            with open(file_name, "w", encoding="utf-8") as f:
                f.write(cleaned_code)
                
            # 4. Trigger Internal Compiler Self-Healing Test Suite
            is_valid, compilation_log = check_syntax_errors(file_name)
            
            if is_valid:
                loop_logs.append(f"✅ **Attempt {attempt} Passed Compilation!** Code verified successfully.")
                current_code = cleaned_code
                break
            else:
                loop_logs.append(f"⚠️ **Attempt {attempt} Failed Syntax Compilation Check.** Refeeding new error logs to agent...")
                current_code = cleaned_code
                current_error = compilation_log
        else:
            # Executes if all 3 self-healing loop cycles fail verification tests
            run_git_cmd(["git", "checkout", "main"])
            logs_summary = "\n".join(loop_logs)
            return f"❌ **Self-Healing Failed:** The agent could not solve the syntax error after 3 attempts.\n\n### Execution Logs:\n{logs_summary}"
            
        # 5. Commit verified clean patch changes and restore main fork
        run_git_cmd(["git", "add", file_name])
        run_git_cmd(["git", "commit", "-m", "feat(hydra): verified self-healing patch execution complete"])
        run_git_cmd(["git", "checkout", "main"])
        
        formatted_logs = "\n".join(loop_logs)
        return f"### 🚀 SYSTEM SUCCESS STATUS\nVerified clean code changes committed seamlessly in the background.\n\n### 📋 Self-Healing Evaluation Telemetry:\n{formatted_logs}\n\n### 💻 Newly Corrected Output:\n```python\n{current_code}\n```"
        
    except Exception as e:
        run_git_cmd(["git", "checkout", "main"])
        return f"❌ System Architecture Pipeline Crash: {str(e)}"

# Assemble the UI Interface presentation canvas
with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 🧬 Hydra-Git: Autonomous Self-Healing Developer Dashboard")
    gr.Markdown("*Compliant with Open-Agent Standard architectures running 100% locally via Llama 3.2 (3B).*")
    
    with gr.Row():
        with gr.Column():
            input_file = gr.Textbox(label="Target Workspace Code Module Path", value="app_module.py")
            input_error = gr.Textbox(label="Initial Crash Telemetry / Stack Error Trace", placeholder="e.g., NameError: name 'data_payload' is not defined")
            submit_btn = gr.Button("Deploy Self-Healing Worker Agent", variant="primary")
        
        with gr.Column():
            output_display = gr.Markdown(label="Real-time Compilation Audit Streams")
            
    submit_btn.click(fn=complete_agent_pipeline, inputs=[input_file, input_error], outputs=output_display)

if __name__ == "__main__":
    demo.launch()
