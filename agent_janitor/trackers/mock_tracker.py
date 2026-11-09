import json
from pathlib import Path
from typing import Dict, Union
from .base import BaseTracker
from ..models import TicketStatus

class MockTracker(BaseTracker):
    """
    Mock tracker for testing or supplying a local mapping file of ticket statuses.
    """
    def __init__(self, mapping: Union[Dict[str, str], Path, str] = None):
        self.mapping = {}
        if isinstance(mapping, (Path, str)):
            p = Path(mapping)
            if p.exists():
                try:
                    with open(p, "r", encoding="utf-8") as f:
                        self.mapping = json.load(f)
                except Exception:
                    pass
        elif isinstance(mapping, dict):
            self.mapping = mapping

    def check_status(self, bug_id: str) -> TicketStatus:
        clean_id = bug_id.lstrip("#")
        val = self.mapping.get(clean_id) or self.mapping.get(bug_id)
        if not val:
            return TicketStatus.UNKNOWN

        val_upper = str(val).upper()
        try:
            return TicketStatus(val_upper)
        except ValueError:
            if "CLOSE" in val_upper or "RESOLV" in val_upper or "FIX" in val_upper:
                return TicketStatus.RESOLVED
            elif "WONT" in val_upper:
                return TicketStatus.WONT_FIX
            elif "OPEN" in val_upper:
                return TicketStatus.OPEN
            return TicketStatus.UNKNOWN
