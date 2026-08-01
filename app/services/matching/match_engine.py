from sqlalchemy.orm import Session
from app.db.models import Candidate, Job
from app.services.matching.skill_matcher import match_skills
from app.services.matching.text_similarity import compute_tfidf_similarity
from app.services.matching.semantic_similarity import compute_semantic_similarity


def match_candidate_to_job(db: Session, candidate_id: int, job_id: int) -> dict:
    candidate = db.query(Candidate).filter(Candidate.id == candidate_id).first()
    job = db.query(Job).filter(Job.id == job_id).first()

    if not candidate:
        raise ValueError(f"Candidate {candidate_id} not found")
    if not job:
        raise ValueError(f"Job {job_id} not found")

    skill_results = match_skills(db, candidate_id, job_id)

    candidate_text = candidate.raw_text or ""
    job_text = job.raw_description or ""

    tfidf_score = compute_tfidf_similarity(candidate_text, job_text)
    semantic_score = compute_semantic_similarity(candidate_text, job_text)

    return {
        "candidate_id": candidate_id,
        "job_id": job_id,
        "candidate_name": candidate.name,
        "job_title": job.title,
        **skill_results,
        "tfidf_similarity": tfidf_score,
        "semantic_similarity": semantic_score,
    }