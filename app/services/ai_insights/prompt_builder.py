import json


def build_recommendation_prompt(
    candidate_name: str,
    job_title: str,
    resume_text: str,
    job_description: str,
    total_score: float,
    required_skills_score: float,
    preferred_skills_score: float,
    experience_score: float,
    education_score: float,
    missing_required_skills: list[str],
    missing_preferred_skills: list[str],
) -> str:
    prompt = f"""
You are an expert technical recruiter assistant. Analyze the following candidate against the job posting and provide a structured hiring assessment.

CANDIDATE: {candidate_name}
JOB TITLE: {job_title}

RESUME TEXT:
{resume_text[:2000]}

JOB DESCRIPTION:
{job_description[:2000]}

COMPUTED MATCH SCORES (0-100 scale):
- Overall Match Score: {total_score}
- Required Skills Match: {required_skills_score}%
- Preferred Skills Match: {preferred_skills_score}%
- Experience Match: {experience_score}%
- Education Match: {education_score}%

MISSING REQUIRED SKILLS: {', '.join(missing_required_skills) if missing_required_skills else 'None'}
MISSING PREFERRED SKILLS: {', '.join(missing_preferred_skills) if missing_preferred_skills else 'None'}

Based on ALL of the above, respond with ONLY a valid JSON object (no markdown formatting, no extra text) matching this exact structure:

{{
  "summary": "2-3 sentence overview of the candidate's fit for this role",
  "strengths": ["strength 1", "strength 2", "strength 3"],
  "weaknesses": ["weakness 1", "weakness 2"],
  "interview_questions": ["question 1 targeting a specific gap", "question 2", "question 3"],
  "recommendation": "Strong Match" or "Possible Match" or "Not a Match",
  "recommendation_justification": "1-2 sentence explanation tying back to the computed score and specific evidence"
}}

Base the "recommendation" field on the overall match score: 70+ = "Strong Match", 40-69 = "Possible Match", below 40 = "Not a Match". Do not contradict the computed score.
"""
    return prompt.strip()