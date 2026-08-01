from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.services.matching.match_engine import match_candidate_to_job
from app.services.matching.final_scorer import calculate_and_save_score
from app.services.ai_insights.insight_service import generate_and_save_insight

router = APIRouter(prefix="/matching", tags=["Matching"])


@router.get("/{candidate_id}/{job_id}")
def get_match(candidate_id: int, job_id: int, db: Session = Depends(get_db)):
    try:
        return match_candidate_to_job(db, candidate_id, job_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/{candidate_id}/{job_id}/score")
def score_match(candidate_id: int, job_id: int, db: Session = Depends(get_db)):
    try:
        match_score = calculate_and_save_score(db, candidate_id, job_id)
        return {
            "candidate_id": match_score.candidate_id,
            "job_id": match_score.job_id,
            "required_skills_score": match_score.required_skills_score,
            "preferred_skills_score": match_score.preferred_skills_score,
            "experience_score": match_score.experience_score,
            "competencies_score": match_score.competencies_score,
            "education_score": match_score.education_score,
            "certifications_score": match_score.certifications_score,
            "projects_score": match_score.projects_score,
            "domain_experience_score": match_score.domain_experience_score,
            "total_score": match_score.total_score,
            "missing_required_skills": match_score.missing_required_skills,
            "missing_preferred_skills": match_score.missing_preferred_skills,
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/{candidate_id}/{job_id}/insights")
def get_insights(candidate_id: int, job_id: int, db: Session = Depends(get_db)):
    try:
        insight = generate_and_save_insight(db, candidate_id, job_id)
        return {
            "candidate_id": insight.candidate_id,
            "job_id": insight.job_id,
            "summary": insight.summary,
            "strengths": insight.strengths,
            "weaknesses": insight.weaknesses,
            "interview_questions": insight.interview_questions,
            "recommendation": insight.recommendation,
            "recommendation_justification": insight.recommendation_justification,
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))