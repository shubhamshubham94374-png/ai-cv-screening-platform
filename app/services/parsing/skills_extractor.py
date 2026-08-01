import re
from rapidfuzz import fuzz
from app.services.parsing.skills_list import KNOWN_SKILLS

def extract_skills(text: str, threshold: int = 85) -> list[str]:
    text_lower = text.lower()
    found_skills = []

    for skill in KNOWN_SKILLS:
        skill_lower = skill.lower()

        # Word-boundary exact match (prevents "Go" matching inside "algorithm")
        pattern = r"\b" + re.escape(skill_lower) + r"\b"
        if re.search(pattern, text_lower):
            found_skills.append(skill)
            continue

        # Fuzzy fallback only for longer, multi-character skills
        if len(skill) > 3:
            score = fuzz.partial_ratio(skill_lower, text_lower)
            if score >= threshold:
                found_skills.append(skill)

    return sorted(set(found_skills))