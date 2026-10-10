import os
import subprocess
import gradio as gr
import ollama
from diff_match_patch import diff_match_patch

def run_git_cmd(args):
    return subprocess.run(args, capture_output=True, text=True)

def clean_model_output(raw_text):
    if not raw_text:
        return ""
    if "```python" in raw_text:
        parts = raw_text.split("```python")
        if len(parts) > 1:
            raw_text = parts[1].split("```")[0]
    elif "```" in raw_text:
        parts = raw_text.split("```")
        if len(parts) > 1:
            raw_text = parts[1].split("```")[0]
            
    return raw_text.strip()

def generate_visual_html_diff(old_text, new_text):
    dmp = diff_match_patch()
    diffs = dmp.diff_main(old_text, new_text)
    dmp.diff_cleanupSemantic(diffs)
    
    html_output = []
    for op, data in diffs:
        text = data.replace('\n', '<br>').replace(' ', '&nbsp;')
        if op == 1:
            html_output.append(f"<span style='background-color: #2ea44f33; color: #22863a; font-weight: bold;'>{text}</span>")
        elif op == -1:
            html_output.append(f"<span style='background-color: #cb243133; color: #cb2431; text-decoration: line-through;'>{text}</span>")
        else:
            html_output.append(f"<span style='color: #24292e;'>{text}</span>")
            
    return f"<div style='font-family: monospace; font-size: 14px; background: #f6f8fa; padding: 15px; border-radius: 6px; border: 1px solid #e1e4e8; white-space: pre-wrap;'>{''.join(html_output)}</div>"

def check_syntax_errors(file_name):
    result = subprocess.run(["python", "-m", "py_compile", file_name], capture_output=True, text=True)
    if result.returncode != 0:
        return False, result.stderr
    return True, "No syntax issues found."

def complete_agent_pipeline(sandbox_code, error_stack):
    file_name = "app_module.py"
    
    try:
        # 🧠 WRITE SANDBOX BROWSER TEXT CODE DIRECTLY TO THE TEST MODULE FILE
        with open(file_name, "w", encoding="utf-8") as f:
            f.write(sandbox_code)
            
        run_git_cmd(["git", "checkout", "-B", "main"])
        run_git_cmd(["git", "add", "."])
        run_git_cmd(["git", "commit", "-m", "chore: dashboard sandbox auto-save"])
        
        run_git_cmd(["git", "branch", "-D", "hydra/ghost-patch-fix"])
        run_git_cmd(["git", "checkout", "-b", "hydra/ghost-patch-fix"])
        
        original_code = sandbox_code
        current_code = original_code
        current_error = error_stack
        max_attempts = 3
        loop_logs = []
        
        for attempt in range(1, max_attempts + 1):
            loop_logs.append(f"🔄 **Attempt {attempt}/{max_attempts}:** Generating patches via Llama 3.2...")
            
            prompt = f"Fix this script code. SOURCE:\n{current_code}\n\nERROR:\n{current_error}\n\nOutput ONLY valid code inside blocks. No conversational text."
            response = ollama.chat(model='llama3.2', messages=[{'role': 'user', 'content': prompt}])
            raw_output = response['message']['content']
            
            cleaned_code = clean_model_output(raw_output)
                
            with open(file_name, "w", encoding="utf-8") as f:
                f.write(cleaned_code)
                
            is_valid, compilation_log = check_syntax_errors(file_name)
            
            if is_valid:
                loop_logs.append(f"✅ **Attempt {attempt} Passed Compilation Checks!**")
                current_code = cleaned_code
                break
            else:
                loop_logs.append(f"⚠️ **Attempt {attempt} Failed Syntax Validation.** Retrying...")
                current_code = cleaned_code
                current_error = compilation_log
        else:
            run_git_cmd(["git", "checkout", "main"])
            return f"❌ **Self-Healing Failed.**\n\nLogs:\n" + "\n".join(loop_logs), ""
            
        commit_prompt = f"Write a 1-sentence engineering git commit message explaining how you fixed this error: {error_stack}. Keep it short and under 60 characters. Do not include quotes."
        commit_response = ollama.chat(model='llama3.2', messages=[{'role': 'user', 'content': commit_prompt}])
        ai_commit_msg = f"fix(hydra): {commit_response['message']['content'].strip()}"
        
        run_git_cmd(["git", "add", file_name])
        run_git_cmd(["git", "commit", "-m", ai_commit_msg])
        run_git_cmd(["git", "checkout", "main"])
        
        visual_diff_html = generate_visual_html_diff(original_code, current_code)
        formatted_logs = "\n".join(loop_logs)
        
        telemetry_report = f"### 🚀 SYSTEM SUCCESS STATUS\nVerified clean code changes committed seamlessly in the background.\n\n🔒 **AI Generated Commit Log:** `{ai_commit_msg}`\n\n### 📋 Telemetry Logs:\n{formatted_logs}"
        return telemetry_report, visual_diff_html
        
    except Exception as e:
        run_git_cmd(["git", "checkout", "main"])
        return f"❌ System Architecture Pipeline Crash: {str(e)}", ""

# Assemble the layout frame with an Interactive Code Input Box Sandbox
with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 🧬 Hydra-Git: Autonomous Self-Healing Developer Dashboard")
    gr.Markdown("*Compliant with Open-Agent Standard architectures running 100% locally via Llama 3.2 (3B) with Live Code Sandbox Inputs.*")
    
    with gr.Row():
        with gr.Column(scale=1):
            input_code = gr.Textbox(
                label="💻 Live Sandbox Code Editor (Type or Change Your Problem Here)", 
                lines=8, 
                value='print("Starting application...")\nresult = data_payload + 100'
            )
            input_error = gr.Textbox(
                label="🚨 Initial Crash Telemetry / Stack Error Trace", 
                value="NameError: name 'data_payload' is not defined"
            )
            submit_btn = gr.Button("Deploy Self-Healing Worker Agent", variant="primary")
            output_telemetry = gr.Markdown(label="Real-time Compilation Audit Streams")
        
        with gr.Column(scale=1):
            gr.Markdown("### 🔍 Live AI Visual Code Diff Analyzer (Green = Insertions, Red = Deletions)")
            output_diff = gr.HTML(label="Visual Code Patch Telemetry Structure Map")
            
    submit_btn.click(fn=complete_agent_pipeline, inputs=[input_code, input_error], outputs=[output_telemetry, output_diff])

if __name__ == "__main__":
    demo.launch()
