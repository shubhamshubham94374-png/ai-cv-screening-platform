from app.db.session import SessionLocal
from app.services.matching.supporting_scorers import score_certifications, score_projects

db = SessionLocal()

job_skills = ["SQL", "Python", "Django", "React"]

cert_score = score_certifications(db, candidate_id=1, relevant_skill_names=job_skills)
print(f"Certification score: {cert_score}")

project_score = score_projects(db, candidate_id=1, relevant_skill_names=job_skills)
print(f"Project score: {project_score}")

db.close()
