from app.db.session import SessionLocal
from app.services.matching.education_scorer import get_highest_candidate_degree, score_education

db = SessionLocal()

highest_degree = get_highest_candidate_degree(db, candidate_id=1)
print(f"Candidate's highest degree level: {highest_degree}")

score_vs_bachelors = score_education(highest_degree, "Bachelor's")
print(f"Score vs 'Bachelor's' requirement: {score_vs_bachelors}")

score_vs_masters = score_education(highest_degree, "Master's")
print(f"Score vs 'Master's' requirement: {score_vs_masters}")

db.close()