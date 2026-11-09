import json
import shutil
import subprocess
from .base import BaseTracker
from ..models import TicketStatus

class GitHubTracker(BaseTracker):
    """
    Queries GitHub issue status via GitHub CLI (`gh`) if available,
    or falls back to UNKNOWN.
    """
    def __init__(self, repo_override: str = None):
        self.gh_available = shutil.which("gh") is not None
        self.repo_override = repo_override
        self._cache = {}

    def check_status(self, bug_id: str) -> TicketStatus:
        # Strip # or leading non-digits if strictly numeric
        clean_id = bug_id.lstrip("#")
        if clean_id in self._cache:
            return self._cache[clean_id]

        if not self.gh_available:
            return TicketStatus.UNKNOWN

        cmd = ["gh", "issue", "view", clean_id, "--json", "state,stateReason"]
        if self.repo_override:
            cmd.extend(["-R", self.repo_override])

        try:
            res = subprocess.run(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=False,
            )
            if res.returncode != 0:
                self._cache[clean_id] = TicketStatus.NOT_FOUND
                return TicketStatus.NOT_FOUND

            data = json.loads(res.stdout)
            state = data.get("state", "").upper()
            state_reason = (data.get("stateReason") or "").upper()

            if state == "CLOSED":
                if state_reason == "NOT_PLANNED":
                    status = TicketStatus.WONT_FIX
                else:
                    status = TicketStatus.RESOLVED
            elif state == "OPEN":
                status = TicketStatus.OPEN
            else:
                status = TicketStatus.UNKNOWN

            self._cache[clean_id] = status
            return status

        except Exception:
            return TicketStatus.UNKNOWN
