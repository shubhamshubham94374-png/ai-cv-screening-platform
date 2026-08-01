import re
from sqlalchemy.orm import Session
from app.db.models import Education
from app.services.parsing.jd_extractors import DEGREE_PATTERNS

DEGREE_RANK = {
    "Diploma": 1,
    "Bachelor's": 2,
    "Master's": 3,
    "PhD": 4,
}


def _detect_degree_level(degree_text: str) -> str | None:
    """Given a free-text degree string, returns its normalized level key (e.g. \"Bachelor's\")."""
    text_lower = degree_text.lower()
    for level, pattern in DEGREE_PATTERNS.items():
        if re.search(pattern, text_lower, re.IGNORECASE):
            return level
    return None


def get_highest_candidate_degree(db: Session, candidate_id: int) -> str | None:
    """Returns the highest-ranked degree level found among a candidate's education records."""
    education_entries = db.query(Education).filter(Education.candidate_id == candidate_id).all()

    highest_level = None
    highest_rank = 0

    for entry in education_entries:
        if not entry.degree:
            continue
        level = _detect_degree_level(entry.degree)
        if level and DEGREE_RANK[level] > highest_rank:
            highest_rank = DEGREE_RANK[level]
            highest_level = level

    return highest_level


def score_education(candidate_degree_level: str | None, required_degree_level: str | None) -> float:
    """
    Scores 0-100 based on whether candidate's degree meets the job's requirement.
    """
    if not required_degree_level:
        return 100.0

    required_rank = DEGREE_RANK.get(required_degree_level, 0)

    if not candidate_degree_level:
        return 0.0

    candidate_rank = DEGREE_RANK.get(candidate_degree_level, 0)

    if candidate_rank >= required_rank:
        return 100.0

    return round((candidate_rank / required_rank) * 100, 2) if required_rank else 100.0