from sqlalchemy.orm import Session
from app.db.models import AIInsight, Candidate, Job, MatchScore
from app.services.ai_insights.prompt_builder import build_recommendation_prompt
from app.services.ai_insights.gemini_client import generate_recommendation


def generate_and_save_insight(db: Session, candidate_id: int, job_id: int) -> AIInsight:
    candidate = db.query(Candidate).filter(Candidate.id == candidate_id).first()
    job = db.query(Job).filter(Job.id == job_id).first()
    match_score = (
        db.query(MatchScore)
        .filter(MatchScore.candidate_id == candidate_id, MatchScore.job_id == job_id)
        .first()
    )

    if not candidate:
        raise ValueError(f"Candidate {candidate_id} not found")
    if not job:
        raise ValueError(f"Job {job_id} not found")
    if not match_score:
        raise ValueError(f"No match score found for candidate {candidate_id} and job {job_id}. Run scoring first.")

    prompt = build_recommendation_prompt(
        candidate_name=candidate.name or "Unknown Candidate",
        job_title=job.title,
        resume_text=candidate.raw_text or "",
        job_description=job.raw_description or "",
        total_score=match_score.total_score,
        required_skills_score=match_score.required_skills_score,
        preferred_skills_score=match_score.preferred_skills_score,
        experience_score=match_score.experience_score,
        education_score=match_score.education_score,
        missing_required_skills=match_score.missing_required_skills or [],
        missing_preferred_skills=match_score.missing_preferred_skills or [],
    )

    result = generate_recommendation(prompt)

    existing = (
        db.query(AIInsight)
        .filter(AIInsight.candidate_id == candidate_id, AIInsight.job_id == job_id)
        .first()
    )

    if existing:
        existing.summary = result["summary"]
        existing.strengths = result["strengths"]
        existing.weaknesses = result["weaknesses"]
        existing.interview_questions = result["interview_questions"]
        existing.recommendation = result["recommendation"]
        existing.recommendation_justification = result["recommendation_justification"]
        insight = existing
    else:
        insight = AIInsight(
            candidate_id=candidate_id,
            job_id=job_id,
            summary=result["summary"],
            strengths=result["strengths"],
            weaknesses=result["weaknesses"],
            interview_questions=result["interview_questions"],
            recommendation=result["recommendation"],
            recommendation_justification=result["recommendation_justification"],
        )
        db.add(insight)

    db.commit()
    db.refresh(insight)
    return insight