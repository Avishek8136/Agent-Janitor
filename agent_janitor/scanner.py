import re
from pathlib import Path
from typing import Generator, List, Optional
from .models import TodoItem

# Common directories to ignore
DEFAULT_IGNORE_DIRS = {
    ".git",
    ".hg",
    ".svn",
    "node_modules",
    "vendor",
    "venv",
    ".venv",
    "env",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    "dist",
    "build",
    "target",
    "bin",
    "obj",
    ".idea",
    ".vscode",
}

# Supported file extensions
SUPPORTED_EXTENSIONS = {
    ".py", ".pyw", ".js", ".jsx", ".ts", ".tsx", ".java", ".c", ".cpp",
    ".h", ".hpp", ".cs", ".go", ".rs", ".rb", ".php", ".swift", ".kt",
    ".kts", ".scala", ".m", ".mm", ".sh", ".bash", ".zsh", ".sql", ".html",
    ".css", ".scss", ".vue", ".svelte", ".dart", ".yaml", ".yml"
}

# Regex pattern for TODO/FIXME variants
# Matches:
# // TODO(bug/12345): description
# // TODO(#123): description
# // TODO(JIRA-123): description
# // FIXME: description
# # BUG(b/999): description
# https://github.com/org/repo/issues/123
TODO_REGEX = re.compile(
    r"""(?xi)
    (?P<kind>TODO|FIXME|BUG|HACK|XXX)
    (?:
        \s* \(\s* (?P<target>[^)]+) \s*\)       # e.g. (b/12345) or (#123) or (username)
      | \s* \[\s* (?P<target_sq>[^\]]+) \s*\]   # e.g. [#123]
    )?
    \s* [: \-]? \s*
    (?P<desc>[^\r\n]*)
    """
)

# Detect ticket format inside target or description
GITHUB_ISSUE_RE = re.compile(r"""(?:#|GH-)(?P<id>\d+)|github\.com/[^/]+/[^/]+/issues/(?P<url_id>\d+)""", re.IGNORECASE)
JIRA_ISSUE_RE = re.compile(r"""\b(?P<id>[A-Z][A-Z0-9]+-\d+)\b""")
BUGANIZER_RE = re.compile(r"""\b(?:b/|bug/)(?P<id>\d+)\b""", re.IGNORECASE)

class Scanner:
    def __init__(self, root_dir: Path, ignore_dirs: Optional[set] = None):
        self.root_dir = Path(root_dir)
        self.ignore_dirs = ignore_dirs or DEFAULT_IGNORE_DIRS

    def is_ignored(self, path: Path) -> bool:
        for part in path.parts:
            if part in self.ignore_dirs:
                return True
        return False

    def scan_file(self, file_path: Path) -> List[TodoItem]:
        items: List[TodoItem] = []
        if file_path.suffix.lower() not in SUPPORTED_EXTENSIONS:
            return items

        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                lines = f.readlines()
        except Exception:
            return items

        for idx, line in enumerate(lines, start=1):
            match = TODO_REGEX.search(line)
            if not match:
                continue

            kind = match.group("kind").upper()
            target = match.group("target") or match.group("target_sq") or ""
            desc = (match.group("desc") or "").strip()

            combined_text = f"{target} {desc}".strip()
            bug_id = None
            bug_system = "generic"

            # Check for GitHub issue
            gh_match = GITHUB_ISSUE_RE.search(combined_text)
            if gh_match:
                bug_id = gh_match.group("id") or gh_match.group("url_id")
                bug_system = "github"
            else:
                # Check for Jira
                jira_match = JIRA_ISSUE_RE.search(combined_text)
                if jira_match:
                    bug_id = jira_match.group("id")
                    bug_system = "jira"
                else:
                    # Check for Google Buganizer/b/ format
                    bug_match = BUGANIZER_RE.search(combined_text)
                    if bug_match:
                        bug_id = bug_match.group("id")
                        bug_system = "buganizer"
                    elif target:
                        # Raw target identifier (e.g. username or ticket)
                        bug_id = target
                        bug_system = "generic"

            items.append(
                TodoItem(
                    file_path=file_path,
                    line_number=idx,
                    raw_line=line,
                    kind=kind,
                    bug_id=bug_id,
                    bug_system=bug_system,
                    description=desc,
                )
            )

        return items

    def scan_all(self) -> Generator[TodoItem, None, None]:
        for path in self.root_dir.rglob("*"):
            if path.is_file() and not self.is_ignored(path):
                for item in self.scan_file(path):
                    yield item
