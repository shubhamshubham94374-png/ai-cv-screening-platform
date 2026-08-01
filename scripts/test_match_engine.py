from app.db.session import SessionLocal
from app.services.matching.match_engine import match_candidate_to_job

db = SessionLocal()

result = match_candidate_to_job(db, candidate_id=1, job_id=1)

for key, value in result.items():
    print(f"{key}: {value}")

db.close()