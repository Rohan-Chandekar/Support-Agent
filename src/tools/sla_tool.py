from datetime import datetime, timedelta

# Response-time SLA in hours, keyed by (category, priority)
SLA_RULES = {
    ("billing", "high"): 4,
    ("billing", "medium"): 24,
    ("billing", "low"): 48,
    ("bug", "high"): 2,
    ("bug", "medium"): 12,
    ("bug", "low"): 48,
    ("how_to", "high"): 12,
    ("how_to", "medium"): 24,
    ("how_to", "low"): 72,
    ("other", "high"): 12,
    ("other", "medium"): 24,
    ("other", "low"): 72,
}

def calculate_sla(category: str, priority: str) -> dict:
    """Pure business-logic function: given a category and priority,
    return the SLA deadline. No LLM, no state — fully unit-testable."""
    hours = SLA_RULES.get((category, priority), 48)  # default fallback
    deadline = datetime.utcnow() + timedelta(hours=hours)
    return {
        "sla_hours": hours,
        "sla_deadline": deadline.isoformat(),
    }