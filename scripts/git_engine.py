
import subprocess
import tempfile
from pathlib import Path
from uuid import uuid4


class SafeGitEngine:
    """Manage isolated Git worktrees safely."""

    def __init__(self, repo_path):
        self.repo_path = Path(repo_path).resolve()
        self.worker_branch = f"hydra-worker-{uuid4().hex[:8]}"
        self.worktree_path = None

    def _git(self, *args):
        return subprocess.run(
            ["git", *args],
            cwd=str(self.repo_path),
            capture_output=True,
            text=True,
            timeout=30,
            check=False,
        )

    def validate_repository(self):
        if not self.repo_path.is_dir():
            return False, "Repository directory does not exist."

        result = self._git("rev-parse", "--is-inside-work-tree")

        if result.returncode != 0:
            return False, "Invalid Git repository."

        return True, "Git repository validated."

    def get_base_commit(self):
        result = self._git("rev-parse", "--verify", "HEAD")

        if result.returncode != 0:
            raise RuntimeError(result.stderr.strip())

        return result.stdout.strip()

    def create_isolated_worktree(self):
        valid, message = self.validate_repository()

        if not valid:
            return False, message

        base_commit = self.get_base_commit()
        temp_dir = Path(tempfile.mkdtemp(prefix="hydra-worktree-"))
        temp_dir.rmdir()

        result = self._git(
            "worktree",
            "add",
            "-b",
            self.worker_branch,
            str(temp_dir),
            base_commit,
        )

        if result.returncode != 0:
            return False, result.stderr.strip()

        self.worktree_path = temp_dir
        return True, str(temp_dir)

    def cleanup_isolated_resources(self):
        if self.worktree_path is None:
            return

        result = self._git(
            "worktree",
            "remove",
            "--force",
            str(self.worktree_path),
        )

        if result.returncode != 0:
            raise RuntimeError(result.stderr.strip())

        self._git("worktree", "prune")
        self.worktree_path = None
