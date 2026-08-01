from sqlalchemy.orm import Session
from app.db.models import Candidate, Job
from app.services.matching.skill_matcher import match_skills
from app.services.matching.text_similarity import compute_tfidf_similarity
from app.services.matching.semantic_similarity import compute_semantic_similarity
from app.services.matching.experience_scorer import calculate_total_experience_years, score_experience
from app.services.matching.education_scorer import get_highest_candidate_degree, score_education
from app.services.matching.supporting_scorers import score_certifications, score_projects

WEIGHTS = {
    "required_skills": 0.35,
    "preferred_skills": 0.15,
    "experience": 0.20,
    "competencies": 0.10,
    "education": 0.05,
    "certifications": 0.05,
    "projects": 0.05,
    "domain_experience": 0.05,
}


def calculate_final_score(db: Session, candidate_id: int, job_id: int) -> dict:
    candidate = db.query(Candidate).filter(Candidate.id == candidate_id).first()
    job = db.query(Job).filter(Job.id == job_id).first()

    if not candidate:
        raise ValueError(f"Candidate {candidate_id} not found")
    if not job:
        raise ValueError(f"Job {job_id} not found")

    # Skill matching (required/preferred)
    skill_results = match_skills(db, candidate_id, job_id)
    required_skills_score = skill_results["required_match_percentage"]
    preferred_skills_score = skill_results["preferred_match_percentage"]

    # Text similarity signals
    candidate_text = candidate.raw_text or ""
    job_text = job.raw_description or ""
    semantic_score = compute_semantic_similarity(candidate_text, job_text) * 100
    tfidf_score = compute_tfidf_similarity(candidate_text, job_text) * 100

    # Experience
    candidate_years = calculate_total_experience_years(db, candidate_id)
    experience_score = score_experience(candidate_years, job.min_experience_years)

    # Education
    candidate_degree = get_highest_candidate_degree(db, candidate_id)
    education_score = score_education(candidate_degree, job.degree_requirement)

    # Certifications & Projects (scored against all job-relevant skills)
    all_job_skills = [s.skill.name for s in job.skills]
    certifications_score = score_certifications(db, candidate_id, all_job_skills)
    projects_score = score_projects(db, candidate_id, all_job_skills)

    # Competencies -> proxied by semantic similarity
    competencies_score = semantic_score

    # Domain experience -> proxied by TF-IDF similarity
    domain_experience_score = tfidf_score

    total_score = round(
        required_skills_score * WEIGHTS["required_skills"]
        + preferred_skills_score * WEIGHTS["preferred_skills"]
        + experience_score * WEIGHTS["experience"]
        + competencies_score * WEIGHTS["competencies"]
        + education_score * WEIGHTS["education"]
        + certifications_score * WEIGHTS["certifications"]
        + projects_score * WEIGHTS["projects"]
        + domain_experience_score * WEIGHTS["domain_experience"],
        2,
    )

    return {
        "candidate_id": candidate_id,
        "job_id": job_id,
        "required_skills_score": required_skills_score,
        "preferred_skills_score": preferred_skills_score,
        "experience_score": experience_score,
        "competencies_score": competencies_score,
        "education_score": education_score,
        "certifications_score": certifications_score,
        "projects_score": projects_score,
        "domain_experience_score": domain_experience_score,
        "total_score": total_score,
        "missing_required_skills": skill_results["missing_required_skills"],
        "missing_preferred_skills": skill_results["missing_preferred_skills"],
    }
from app.db.models import MatchScore


def calculate_and_save_score(db: Session, candidate_id: int, job_id: int) -> MatchScore:
    result = calculate_final_score(db, candidate_id, job_id)

    existing = (
        db.query(MatchScore)
        .filter(MatchScore.candidate_id == candidate_id, MatchScore.job_id == job_id)
        .first()
    )

    if existing:
        for key, value in result.items():
            if hasattr(existing, key):
                setattr(existing, key, value)
        existing.missing_required_skills = result["missing_required_skills"]
        existing.missing_preferred_skills = result["missing_preferred_skills"]
        match_score = existing
    else:
        match_score = MatchScore(
            candidate_id=candidate_id,
            job_id=job_id,
            required_skills_score=result["required_skills_score"],
            preferred_skills_score=result["preferred_skills_score"],
            experience_score=result["experience_score"],
            competencies_score=result["competencies_score"],
            education_score=result["education_score"],
            certifications_score=result["certifications_score"],
            projects_score=result["projects_score"],
            domain_experience_score=result["domain_experience_score"],
            total_score=result["total_score"],
            missing_required_skills=result["missing_required_skills"],
            missing_preferred_skills=result["missing_preferred_skills"],
        )
        db.add(match_score)

    db.commit()
    db.refresh(match_score)
    return match_score