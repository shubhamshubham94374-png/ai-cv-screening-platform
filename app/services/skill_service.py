from sqlalchemy.orm import Session
from app.db.models import Skill, CandidateSkill, SkillSource, Job, JobSkill, RequirementType

from rapidfuzz import fuzz, process


from app.services.parsing.skill_aliases import normalize_skill_name


def get_or_create_skill(db: Session, skill_name: str, fuzzy_threshold: int = 85) -> Skill:
    skill_name = normalize_skill_name(skill_name)

    skill = db.query(Skill).filter(Skill.name == skill_name).first()
    if skill:
        return skill

    all_skills = db.query(Skill).all()
    if all_skills:
        existing_names = [s.name for s in all_skills]
        best_match = process.extractOne(skill_name, existing_names, scorer=fuzz.ratio)

        if best_match and best_match[1] >= fuzzy_threshold:
            matched_name = best_match[0]
            return next(s for s in all_skills if s.name == matched_name)

    skill = Skill(name=skill_name)
    db.add(skill)
    db.flush()
    return skill

def link_skills_to_candidate(db: Session, candidate_id: int, skill_names: list[str]) -> None:
    """Create Skill rows (if needed) and link them to a candidate via CandidateSkill."""
    seen_skill_ids = set()

    for skill_name in skill_names:
        skill = get_or_create_skill(db, skill_name)

        if skill.id in seen_skill_ids:
            continue  # already processed this skill_id in this same batch

        seen_skill_ids.add(skill.id)

        existing_link = (
            db.query(CandidateSkill)
            .filter(
                CandidateSkill.candidate_id == candidate_id,
                CandidateSkill.skill_id == skill.id,
            )
            .first()
        )
        if existing_link:
            continue

        link = CandidateSkill(
            candidate_id=candidate_id,
            skill_id=skill.id,
            source=SkillSource.listed,
        )
        db.add(link)


def link_skills_to_job(db: Session, job_id: int, required_skills: list[str], preferred_skills: list[str]) -> None:
    """Create Skill rows (if needed) and link them to a job, tagged as required or preferred."""
    for skill_name in required_skills:
        skill = get_or_create_skill(db, skill_name)
        _link_job_skill(db, job_id, skill.id, RequirementType.required)

    for skill_name in preferred_skills:
        skill = get_or_create_skill(db, skill_name)
        _link_job_skill(db, job_id, skill.id, RequirementType.preferred)


def _link_job_skill(db: Session, job_id: int, skill_id: int, requirement_type: RequirementType) -> None:
    existing_link = (
        db.query(JobSkill)
        .filter(JobSkill.job_id == job_id, JobSkill.skill_id == skill_id)
        .first()
    )
    if existing_link:
        return

    link = JobSkill(job_id=job_id, skill_id=skill_id, requirement_type=requirement_type)
    db.add(link)