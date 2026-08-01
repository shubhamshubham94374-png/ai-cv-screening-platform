import os
from app.services.parsing.pdf_parser import extract_text_from_pdf
from app.services.parsing.docx_parser import extract_text_from_docx
from app.services.parsing.field_extractors import (
    extract_email,
    extract_phone,
    extract_linkedin,
    extract_github,
    extract_portfolio_links,
)
from app.services.parsing.name_extractor import extract_name
from app.services.parsing.skills_extractor import extract_skills


def _get_raw_text(file_path: str) -> str:
    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".pdf":
        return extract_text_from_pdf(file_path)
    elif ext == ".docx":
        return extract_text_from_docx(file_path)
    else:
        raise ValueError(f"Unsupported file type for parsing: {ext}")


def parse_resume(file_path: str) -> dict:
    text = _get_raw_text(file_path)

    return {
        "name": extract_name(text),
        "email": extract_email(text),
        "phone": extract_phone(text),
        "linkedin": extract_linkedin(text),
        "github": extract_github(text),
        "portfolio_links": extract_portfolio_links(text),
        "skills": extract_skills(text),
        "raw_text": text,
    }