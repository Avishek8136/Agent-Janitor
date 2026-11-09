from abc import ABC, abstractmethod
from ..models import TicketStatus

class BaseTracker(ABC):
    @abstractmethod
    def check_status(self, bug_id: str) -> TicketStatus:
        pass
