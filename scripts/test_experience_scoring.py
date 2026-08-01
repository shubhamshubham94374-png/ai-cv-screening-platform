from app.db.session import SessionLocal
from app.services.matching.experience_scorer import calculate_total_experience_years, score_experience

db = SessionLocal()

years = calculate_total_experience_years(db, candidate_id=1)
print(f"Candidate 1 total experience: {years} years")

score = score_experience(years, required_years=3)
print(f"Experience score (vs 3 years required): {score}")

db.close()