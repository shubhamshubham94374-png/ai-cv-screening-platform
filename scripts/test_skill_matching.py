from app.db.session import SessionLocal
from app.services.matching.skill_matcher import match_skills

db = SessionLocal()

result = match_skills(db, candidate_id=1, job_id=1)
print(result)

db.close()