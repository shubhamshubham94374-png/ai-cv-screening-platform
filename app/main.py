from fastapi import FastAPI
from app.db.session import Base, engine
from app.api import resumes
from app.api import resumes, jobs, matching

app = FastAPI(title="AI-Powered CV Screening Platform")

Base.metadata.create_all(bind=engine)

app.include_router(resumes.router)

app.include_router(matching.router)

app.include_router(jobs.router)

@app.get("/")
def root():
    return {"message": "CV Screening Platform API is running"}
