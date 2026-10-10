import ollama

class ResilientAIConnector:
    def __init__(self, model_name="llama3.2"):
        self.model_name = model_name
        
    def verify_ollama_service(self):
        """Checks if the background engine is active and reachable via standard protocols."""
        try:
            # Pings the local server registry to check reachability
            ollama.list()
            return True, "Ollama environment status: Operational."
        except Exception as e:
            return False, f"Ollama unreachable. Ensure server is active (`ollama serve`). Error: {str(e)}"

    def request_code_repair(self, source_code, error_context, language):
        """Queries the model for targeted patches, avoiding full-file overrides."""
        prompt = f"""
        You are an expert software verification engineering agent. Fix this bug in the {language} file.
        
        ORIGINAL SCRIPT CONTENT:
        {source_code}
        
        CRASH RUNTIME TELEMETRY LOGS:
        {error_context}
        
        INSTRUCTION: Rewrite the code to resolve the error. Avoid unrelated modifications. 
        Output ONLY the raw functional source code inside a single code block wrapper. Do not add chat text.
        """
        try:
            response = ollama.chat(
                model=self.model_name,
                messages=[{'role': 'user', 'content': prompt}]
            )
            raw_text = response['message']['content']
            
            # Bulletproof extraction algorithm that handles multiple markdown wrapper patterns
            if "```" in raw_text:
                parts = raw_text.split("```")
                for part in parts:
                    lines = part.strip().split('\n')
                    if len(lines) > 0 and ("python" in lines[0] or "js" in lines[0] or "go" in lines[0] or "rust" in lines[0] or "java" in lines[0] or "cpp" in lines[0]):
                        return part.replace(lines[0], "", 1).strip()
                return raw_text.split("```")[1].strip()
            return raw_text.strip()
        except Exception as e:
            return f"AI Connection Failure: {str(e)}"
