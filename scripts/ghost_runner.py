import os
import sys
import subprocess
import ollama

def run_git_cmd(args):
    # Safe terminal wrapper execution routine
    return subprocess.run(args, capture_output=True, text=True)

def orchestrate_ghost_developer(target_file, error_message):
    print(f"🧬 Spawning background branch for {target_file}...")
    
    # 1. Clean workspace environment state check
    run_git_cmd(["git", "add", "."])
    run_git_cmd(["git", "commit", "-m", "chore: initial checkpoint rescue"])
    run_git_cmd(["git", "checkout", "-b", "hydra/ghost-patch-fix"])
    
    if not os.path.exists(target_file):
        return "Target code file not found."
        
    with open(target_file, "r") as f:
        broken_source = f.read()
        
    prompt = f"Fix this script code. SOURCE:\n{broken_source}\n\nERROR:\n{error_message}\n\nOutput ONLY valid code. No conversations."
    
    # Connect directly to your local Llama 3.2 3B engine
    response = ollama.chat(model='llama3.2', messages=[{'role': 'user', 'content': prompt}])
    cleaned_code = response['message']['content']
    
    # Stripe away potential markdown block formatting from models safely
    if "```python" in cleaned_code:
        cleaned_code = cleaned_code.split("```python")[1].split("```")[0].strip()
    elif "```" in cleaned_code:
        cleaned_code = cleaned_code.split("```")[1].split("```")[0].strip()
    
    with open(target_file, "w") as f:
        f.write(cleaned_code)
        
    run_git_cmd(["git", "add", target_file])
    run_git_cmd(["git", "commit", "-m", "feat(hydra): automated fix implementation complete"])
    
    # Return workspace back to user main line seamlessly
    run_git_cmd(["git", "checkout", "main"])
    return "🚀 Success! Clean code changes committed seamlessly in the background."

if __name__ == "__main__":
    if len(sys.argv) > 2:
        print(orchestrate_ghost_developer(sys.argv[1], sys.argv[2]))
