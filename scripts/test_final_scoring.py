from app.db.session import SessionLocal
from app.services.matching.final_scorer import calculate_final_score

db = SessionLocal()

result = calculate_final_score(db, candidate_id=1, job_id=1)

for key, value in result.items():
    print(f"{key}: {value}")

db.close()