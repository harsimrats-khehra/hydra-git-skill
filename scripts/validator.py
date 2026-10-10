import subprocess
import shutil

class PolyglotValidator:
    LANGUAGE_MATRIX = {
        "Python": {"ext": ".py", "check": ["python", "-m", "py_compile"], "test": ["pytest"]},
        "JavaScript": {"ext": ".js", "check": ["node", "--check"], "test": ["npm", "test"]},
        "Java": {"ext": ".java", "check": ["javac"], "test": ["mvn", "test"]},
        "C": {"ext": ".c", "check": ["gcc", "-fsyntax-only"], "test": ["make", "test"]},
        "C++": {"ext": ".cpp", "check": ["g++", "-fsyntax-only"], "test": ["make", "test"]},
        "Go": {"ext": ".go", "check": ["go", "vet"], "test": ["go", "test"]},
        "Rust": {"ext": ".rs", "check": ["cargo", "check"], "test": ["cargo", "test"]}
    }

    @classmethod
    def check_toolchain_availability(cls, language):
        config = cls.LANGUAGE_MATRIX.get(language)
        if not config:
            return False, "Unsupported target programming language."
        base_binary = config["check"][0]
        if shutil.which(base_binary) is None:
            return False, f"Missing compiler/runtime backend toolchain tracking references for: {base_binary}"
        return True, "Toolchain active."

    @classmethod
    def validate_code_syntax(cls, file_path, language):
        config = cls.LANGUAGE_MATRIX.get(language)
        cmd = list(config["check"]) + [file_path]
        try:
            res = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
            if res.returncode == 0:
                return True, "Syntax Valid"
            return False, res.stderr if res.stderr else res.stdout
        except subprocess.TimeoutExpired:
            return False, "Syntax validation check timed out."

    @classmethod
    def execute_custom_test(cls, working_dir, custom_cmd):
        """Runs testing routines safely within the isolated directory."""
        if not custom_cmd:
            return "Not Verified", "No testing commands provided."
        try:
            res = subprocess.run(
                custom_cmd, shell=True, cwd=working_dir,
                capture_output=True, text=True, timeout=30
            )
            if res.returncode == 0:
                return "Tests Passed", res.stdout
            return "Tests Failed", res.stderr if res.stderr else res.stdout
        except subprocess.TimeoutExpired:
            return "Tests Failed", "Execution test loop timed out safely."
