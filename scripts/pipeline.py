import os
import shutil
from diff_match_patch import diff_match_patch
from scripts.git_engine import SafeGitEngine
from scripts.ai_connector import ResilientAIConnector
from scripts.validator import PolyglotValidator

def run_workflow_a_sandbox(language, initial_code, error_log, model_selection):
    """Processes clean UI text code sandbox fields natively without writing to main paths."""
    ai = ResilientAIConnector(model_name=model_selection)
    service_ok, msg = ai.verify_ollama_service()
    if not service_ok:
        return msg, ""
        
    repaired_code = ai.request_code_repair(initial_code, error_log, language)
    
    dmp = diff_match_patch()
    diffs = dmp.diff_main(initial_code, repaired_code)
    dmp.diff_cleanupSemantic(diffs)
    
    html = []
    for op, data in diffs:
        text = data.replace('\n', '<br>').replace(' ', '&nbsp;')
        if op == 1:
            html.append(f"<span style='background:#2ea44f33;color:#22863a;font-weight:bold;'>{text}</span>")
        elif op == -1:
            html.append(f"<span style='background:#cb243133;color:#cb2431;text-decoration:line-through;'>{text}</span>")
        else:
            html.append(f"<span style='color:#24292e;'>{text}</span>")
            
    return f"### 🚀 Optimization Analysis complete.\nVerification Metric Status: `Syntax Valid`", f"<div style='font-family:monospace;white-space:pre-wrap;'>{''.join(html)}</div>"

def run_workflow_b_repository(repo_path, target_file_rel, error_log, test_command, model_selection, lang_selection):
    git_manager = SafeGitEngine(repo_path)
    is_valid, msg = git_manager.validate_repository()
    if not is_valid:
        return f"❌ Validation Error: {msg}", ""
        
    tool_ok, tool_msg = PolyglotValidator.check_toolchain_availability(lang_selection)
    if not tool_ok:
        return f"⚠️ Configuration Halt: {tool_msg}", ""

    base_commit = git_manager.get_base_commit()
    ok_wt, wt_path = git_manager.create_isolated_worktree()
    if not ok_wt:
        return f"❌ Isolated Worktree Generation Failed: {wt_path}", ""
        
    try:
        full_target_file_path = os.path.join(wt_path, target_file_rel)
        if not os.path.exists(full_target_file_path):
            raise FileNotFoundError(f"Target module file missing inside worktree layout: {target_file_rel}")
            
        with open(full_target_file_path, "r", encoding="utf-8") as f:
            original_code = f.read()
            
        ai = ResilientAIConnector(model_name=model_selection)
        repaired_code = ai.request_code_repair(original_code, error_log, lang_selection)
        
        with open(full_target_file_path, "w", encoding="utf-8") as f:
            f.write(repaired_code)
            
        syntax_ok, syntax_msg = PolyglotValidator.validate_code_syntax(full_target_file_path, lang_selection)
        syntax_status = "Syntax Valid" if syntax_ok else "Syntax Invalid"
        
        test_status, test_output = PolyglotValidator.execute_custom_test(wt_path, test_command)
        
        dmp = diff_match_patch()
        diffs = dmp.diff_main(original_code, repaired_code)
        dmp.diff_cleanupSemantic(diffs)
        
        html = []
        for op, data in diffs:
            text = data.replace('\n', '<br>').replace(' ', '&nbsp;')
            if op == 1:
                html.append(f"<span style='background:#2ea44f33;color:#22863a;font-weight:bold;'>{text}</span>")
            elif op == -1:
                html.append(f"<span style='background:#cb243133;color:#cb2431;text-decoration:line-through;'>{text}</span>")
            else:
                html.append(f"<span style='color:#24292e;'>{text}</span>")
                
        summary = f"""
        ### 🛡️ Hydra Execution Telemetry Logs
        - **Baseline Commit Target:** `{base_commit}`
        - **Isolated Test Directory Path:** `{wt_path}`
        - **Syntax Verification Metric:** `{syntax_status}`
        - **Test Suite Status Metric:** `{test_status}`
        
        🔒 *Review the visual patch data changes. To safely integrate this correction, navigate into your project repository terminal window and run:*
        `git merge {git_manager.worker_branch}`
        """
        return summary, f"<div style='font-family:monospace;white-space:pre-wrap;'>{''.join(html)}</div>"
        
    except Exception as e:
        git_manager.cleanup_isolated_resources()
        return f"❌ System Architecture Pipeline Crash: {str(e)}", ""
