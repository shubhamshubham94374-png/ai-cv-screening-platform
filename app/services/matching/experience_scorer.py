from datetime import datetime
from dateutil import parser as date_parser
from sqlalchemy.orm import Session
from app.db.models import Experience


def _parse_date_safe(date_str: str | None) -> datetime | None:
    """Attempts to parse a messy date string; returns None if it can't be parsed."""
    if not date_str or date_str.strip().lower() in ("present", "current", "ongoing", ""):
        return datetime.now() if date_str and date_str.strip().lower() in ("present", "current", "ongoing") else None

    try:
        return date_parser.parse(date_str, fuzzy=True, default=datetime(2000, 1, 1))
    except (ValueError, OverflowError):
        return None


def calculate_total_experience_years(db: Session, candidate_id: int) -> float:
    """
    Sums up total years of experience across all of a candidate's work experience entries,
    based on start_date/end_date strings (parsed flexibly).
    """
    experiences = db.query(Experience).filter(Experience.candidate_id == candidate_id).all()

    total_days = 0
    for exp in experiences:
        start = _parse_date_safe(exp.start_date)
        end = _parse_date_safe(exp.end_date)

        if start and end and end > start:
            total_days += (end - start).days

    return round(total_days / 365.25, 2)


def score_experience(candidate_years: float, required_years: int | None) -> float:
    """
    Scores 0-100 based on how candidate's experience compares to the job's requirement.
    Meeting or exceeding the requirement scores 100; partial experience scores proportionally.
    """
    if not required_years or required_years == 0:
        return 100.0

    if candidate_years >= required_years:
        return 100.0

    return round((candidate_years / required_years) * 100, 2)