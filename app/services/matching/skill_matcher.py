from sqlalchemy.orm import Session
from app.db.models import CandidateSkill, JobSkill, RequirementType, Skill


def match_skills(db: Session, candidate_id: int, job_id: int) -> dict:
    """
    Compares a candidate's skills against a job's required and preferred skills,
    based on shared skill_id (exact match via the normalized skills table).
    """
    candidate_skill_ids = {
        cs.skill_id for cs in db.query(CandidateSkill).filter(CandidateSkill.candidate_id == candidate_id).all()
    }

    job_skills = db.query(JobSkill).filter(JobSkill.job_id == job_id).all()

    required_skill_ids = {js.skill_id for js in job_skills if js.requirement_type == RequirementType.required}
    preferred_skill_ids = {js.skill_id for js in job_skills if js.requirement_type == RequirementType.preferred}

    matched_required = candidate_skill_ids & required_skill_ids
    matched_preferred = candidate_skill_ids & preferred_skill_ids
    missing_required = required_skill_ids - candidate_skill_ids
    missing_preferred = preferred_skill_ids - candidate_skill_ids

    required_match_pct = (len(matched_required) / len(required_skill_ids) * 100) if required_skill_ids else 100.0
    preferred_match_pct = (len(matched_preferred) / len(preferred_skill_ids) * 100) if preferred_skill_ids else 100.0

    def _names(skill_ids: set[int]) -> list[str]:
        if not skill_ids:
            return []
        skills = db.query(Skill).filter(Skill.id.in_(skill_ids)).all()
        return sorted(s.name for s in skills)

    return {
        "matched_required_skills": _names(matched_required),
        "matched_preferred_skills": _names(matched_preferred),
        "missing_required_skills": _names(missing_required),
        "missing_preferred_skills": _names(missing_preferred),
        "required_match_percentage": round(required_match_pct, 2),
        "preferred_match_percentage": round(preferred_match_pct, 2),
    }