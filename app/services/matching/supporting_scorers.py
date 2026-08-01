from sqlalchemy.orm import Session
from app.db.models import Certification, Project


def score_certifications(db: Session, candidate_id: int, relevant_skill_names: list[str]) -> float:
    """
    Scores 0-100 based on how many of the job's relevant skills are mentioned
    across the candidate's certification names.
    """
    if not relevant_skill_names:
        return 100.0

    certifications = db.query(Certification).filter(Certification.candidate_id == candidate_id).all()
    if not certifications:
        return 0.0

    cert_text = " ".join(c.name for c in certifications).lower()

    matched = sum(1 for skill in relevant_skill_names if skill.lower() in cert_text)
    return round((matched / len(relevant_skill_names)) * 100, 2)


def score_projects(db: Session, candidate_id: int, relevant_skill_names: list[str]) -> float:
    """
    Scores 0-100 based on how many of the job's relevant skills are mentioned
    across the candidate's project titles/descriptions.
    """
    if not relevant_skill_names:
        return 100.0

    projects = db.query(Project).filter(Project.candidate_id == candidate_id).all()
    if not projects:
        return 0.0

    project_text = " ".join(f"{p.title} {p.description or ''}" for p in projects).lower()

    matched = sum(1 for skill in relevant_skill_names if skill.lower() in project_text)
    return round((matched / len(relevant_skill_names)) * 100, 2)