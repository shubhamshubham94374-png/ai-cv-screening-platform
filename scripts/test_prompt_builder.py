from app.services.ai_insights.prompt_builder import build_recommendation_prompt

prompt = build_recommendation_prompt(
    candidate_name="Shubham Malik",
    job_title="Backend Developer",
    resume_text="Software Engineering student with DSA and Java experience...",
    job_description="Hiring a Backend Developer with 3+ years experience in Python, Django...",
    total_score=46.8,
    required_skills_score=40.0,
    preferred_skills_score=25.0,
    experience_score=100.0,
    education_score=100.0,
    missing_required_skills=["Django", "Python", "REST API"],
    missing_preferred_skills=["AWS", "Docker", "Kubernetes"],
)

print(prompt)
