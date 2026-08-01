import re

def extract_min_experience(text: str) -> int | None:
    """
    Looks for patterns like:
    '3+ years', '2-4 years experience', 'minimum 5 years', 'at least 2 years'
    Returns the smallest/minimum number found in such a phrase.
    """
    patterns = [
        r"(\d+)\s*\+\s*years",                          # "3+ years"
        r"minimum\s*(?:of\s*)?(\d+)\s*years",            # "minimum of 3 years"
        r"at least\s*(\d+)\s*years",                     # "at least 3 years"
        r"(\d+)\s*-\s*\d+\s*years",                      # "2-4 years" -> takes the lower bound
        r"(\d+)\+?\s*years?\s*of\s*experience",           # "5 years of experience"
    ]

    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return int(match.group(1))

    return None
DEGREE_PATTERNS = {
    "PhD": r"\b(ph\.?d|doctorate)\b",
    "Master's": r"\b(master'?s|master\s+of|m\.?tech|m\.?e\.?|mca|msc|m\.?s\.?)\b",
    "Bachelor's": r"\b(bachelor'?s|bachelor\s+of|b\.?tech|b\.?e\.?|bca|bsc|b\.?s\.?)\b",
    "Diploma": r"\bdiploma\b",
}

def extract_degree_requirement(text: str) -> str | None:
    """
    Scans for degree-level keywords and returns the highest degree level mentioned.
    Priority: PhD > Master's > Bachelor's > Diploma
    """
    text_lower = text.lower()

    for degree_label, pattern in DEGREE_PATTERNS.items():
        if re.search(pattern, text_lower, re.IGNORECASE):
            return degree_label

    return None
from app.services.parsing.skills_extractor import extract_skills

REQUIRED_MARKERS = [
    r"required skills",
    r"requirements",
    r"must[\s-]have",
    r"minimum qualifications",
]

PREFERRED_MARKERS = [
    r"preferred skills",
    r"nice[\s-]to[\s-]have",
    r"good[\s-]to[\s-]have",
    r"bonus",
    r"preferred qualifications",
]


def split_required_preferred_skills(text: str) -> dict:
    """
    Splits the JD into a 'required' section and 'preferred' section based on
    marker phrases, then extracts skills separately from each.
    If no clear preferred section is found, all skills are treated as required.
    """
    text_lower = text.lower()

    # Find the earliest position where a "preferred" marker starts
    preferred_start = None
    for pattern in PREFERRED_MARKERS:
        match = re.search(pattern, text_lower)
        if match and (preferred_start is None or match.start() < preferred_start):
            preferred_start = match.start()

    if preferred_start is not None:
        required_text = text[:preferred_start]
        preferred_text = text[preferred_start:]
    else:
        required_text = text
        preferred_text = ""

    required_skills = extract_skills(required_text)
    preferred_skills = extract_skills(preferred_text) if preferred_text else []

    # Avoid double-counting: if a skill appears in both, keep it only in "required"
    preferred_skills = [s for s in preferred_skills if s not in required_skills]

    return {
        "required": required_skills,
        "preferred": preferred_skills,
    }