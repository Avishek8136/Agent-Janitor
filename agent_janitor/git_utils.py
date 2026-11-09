import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional, Tuple

def is_git_repo(path: Path) -> bool:
    try:
        res = subprocess.run(
            ["git", "rev-parse", "--is-inside-work-tree"],
            cwd=path if path.is_dir() else path.parent,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=False,
        )
        return res.returncode == 0 and res.stdout.strip() == "true"
    except Exception:
        return False

def get_git_blame_info(file_path: Path, line_number: int) -> Tuple[Optional[str], Optional[str], Optional[str], Optional[int]]:
    """
    Returns (commit_hash, author, commit_date_iso, age_days)
    """
    try:
        cmd = [
            "git", "blame",
            "-L", f"{line_number},{line_number}",
            "--porcelain",
            str(file_path.name)
        ]
        res = subprocess.run(
            cmd,
            cwd=file_path.parent,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=False,
        )
        if res.returncode != 0:
            return None, None, None, None

        lines = res.stdout.splitlines()
        if not lines:
            return None, None, None, None

        commit_hash = lines[0].split()[0]
        author = None
        author_time_epoch = None

        for line in lines[1:]:
            if line.startswith("author "):
                author = line[7:].strip()
            elif line.startswith("author-time "):
                try:
                    author_time_epoch = int(line[12:].strip())
                except ValueError:
                    pass

        commit_date_iso = None
        age_days = None

        if author_time_epoch:
            commit_dt = datetime.fromtimestamp(author_time_epoch, tz=timezone.utc)
            commit_date_iso = commit_dt.strftime("%Y-%m-%d")
            now_dt = datetime.now(timezone.utc)
            age_days = (now_dt - commit_dt).days

        return commit_hash, author, commit_date_iso, age_days
    except Exception:
        return None, None, None, None
