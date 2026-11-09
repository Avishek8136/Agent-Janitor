from .models import TodoItem, TicketStatus, TrapClassification

def classify_todo(item: TodoItem, fossil_age_days: int = 365) -> TrapClassification:
    # 1. Closed or resolved tickets = Dead End traps
    if item.ticket_status in (TicketStatus.CLOSED, TicketStatus.RESOLVED, TicketStatus.WONT_FIX):
        return TrapClassification.DEAD_END

    # 2. Open tickets = Scope Creep risk (eager agents might try to fix them unprompted)
    if item.ticket_status == TicketStatus.OPEN:
        return TrapClassification.SCOPE_CREEP_RISK

    # 3. Ancient unlinked or untracked TODOs
    if item.age_days is not None and item.age_days >= fossil_age_days:
        return TrapClassification.FOSSIL

    return TrapClassification.UNKNOWN
