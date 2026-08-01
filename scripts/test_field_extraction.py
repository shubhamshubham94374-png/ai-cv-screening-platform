from app.services.parsing.pdf_parser import extract_text_from_pdf
from app.services.parsing.field_extractors import (
    extract_email,
    extract_phone,
    extract_linkedin,
    extract_github,
    extract_portfolio_links,
)
from app.services.parsing.name_extractor import extract_name
from app.services.parsing.skills_extractor import extract_skills

text = extract_text_from_pdf(r"C:\Users\shubh\Downloads\22BCS17074_Shubham_Malik_2026.pdf")

print(f"Name: {extract_name(text)}")
print(f"Email: {extract_email(text)}")
print(f"Phone: {extract_phone(text)}")
print(f"LinkedIn: {extract_linkedin(text)}")
print(f"GitHub: {extract_github(text)}")
print(f"Portfolio Links: {extract_portfolio_links(text)}")
print(f"Skills: {extract_skills(text)}")