import os
from app.services.parsing.pdf_parser import extract_text_from_pdf
from app.services.parsing.docx_parser import extract_text_from_docx
from app.services.parsing.jd_extractors import (
    extract_min_experience,
    extract_degree_requirement,
    split_required_preferred_skills,
)


def _get_raw_text(file_path: str) -> str:
    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".pdf":
        return extract_text_from_pdf(file_path)
    elif ext == ".docx":
        return extract_text_from_docx(file_path)
    else:
        raise ValueError(f"Unsupported file type for parsing: {ext}")


def parse_job_description(text: str = None, file_path: str = None) -> dict:
    """
    Accepts EITHER raw pasted text OR a file path (PDF/DOCX) — exactly one should be provided.
    """
    if file_path:
        text = _get_raw_text(file_path)
    elif text is None:
        raise ValueError("Either 'text' or 'file_path' must be provided.")

    skills = split_required_preferred_skills(text)

    return {
        "min_experience_years": extract_min_experience(text),
        "degree_requirement": extract_degree_requirement(text),
        "required_skills": skills["required"],
        "preferred_skills": skills["preferred"],
        "raw_description": text,
    }