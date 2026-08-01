from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models import Job
from app.schemas.job_schemas import JobCreateRequest
from app.services.parsing.jd_parser import parse_job_description
from app.services.skill_service import link_skills_to_job

router = APIRouter(prefix="/jobs", tags=["Jobs"])


@router.post("/")
def create_job(payload: JobCreateRequest, db: Session = Depends(get_db)):
    parsed = parse_job_description(text=payload.description)

    job = Job(
        title=payload.title,
        company=payload.company,
        raw_description=payload.description,
        min_experience_years=parsed["min_experience_years"],
        degree_requirement=parsed["degree_requirement"],
    )
    db.add(job)
    db.commit()
    db.refresh(job)

    link_skills_to_job(db, job.id, parsed["required_skills"], parsed["preferred_skills"])
    db.commit()

    return {
        "job_id": job.id,
        "title": job.title,
        "company": job.company,
        "min_experience_years": job.min_experience_years,
        "degree_requirement": job.degree_requirement,
        "required_skills": parsed["required_skills"],
        "preferred_skills": parsed["preferred_skills"],
    }