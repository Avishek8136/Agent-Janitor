from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Optional

class TicketStatus(str, Enum):
    OPEN = "OPEN"
    CLOSED = "CLOSED"
    RESOLVED = "RESOLVED"
    WONT_FIX = "WONT_FIX"
    NOT_FOUND = "NOT_FOUND"
    UNKNOWN = "UNKNOWN"

class TrapClassification(str, Enum):
    # 41% of distractions: Ticket is closed/fixed/wontfix, agent chases ghosts
    DEAD_END = "DEAD_END"
    # 57% of distractions: Ticket is still open, agent attempts unprompted fix/scope creep
    SCOPE_CREEP_RISK = "SCOPE_CREEP_RISK"
    # Untracked TODO that has been untouched for > 1 year
    FOSSIL = "FOSSIL"
    # Valid active TODO
    ACTIVE = "ACTIVE"
    # Cannot be determined without tracker connection
    UNKNOWN = "UNKNOWN"

@dataclass
class TodoItem:
    file_path: Path
    line_number: int
    raw_line: str
    kind: str  # TODO, FIXME, BUG, HACK
    bug_id: Optional[str] = None
    bug_system: str = "generic"  # github, jira, buganizer, generic
    description: str = ""
    age_days: Optional[int] = None
    commit_date: Optional[str] = None
    commit_hash: Optional[str] = None
    author: Optional[str] = None
    ticket_status: TicketStatus = TicketStatus.UNKNOWN
    classification: TrapClassification = TrapClassification.UNKNOWN

    @property
    def display_tag(self) -> str:
        if self.bug_id:
            return f"{self.kind}({self.bug_id})"
        return self.kind
