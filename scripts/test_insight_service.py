from app.db.session import SessionLocal
from app.services.ai_insights.insight_service import generate_and_save_insight

db = SessionLocal()

insight = generate_and_save_insight(db, candidate_id=1, job_id=1)

print(f"Recommendation: {insight.recommendation}")
print(f"Summary: {insight.summary}")
print(f"Strengths: {insight.strengths}")

db.close()