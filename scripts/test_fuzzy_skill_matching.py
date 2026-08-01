from app.db.session import SessionLocal
from app.services.skill_service import get_or_create_skill

db = SessionLocal()

# First call creates "Postgres" as a new skill (if it doesn't already exist)
skill1 = get_or_create_skill(db, "Postgres")
print(f"First call: id={skill1.id}, name={skill1.name}")

# Second call with a similar-but-different spelling should reuse the same skill
skill2 = get_or_create_skill(db, "PostgreSQL")
print(f"Second call: id={skill2.id}, name={skill2.name}")

print(f"Same skill reused: {skill1.id == skill2.id}")

db.commit()
db.close()