from app.services.parsing.docx_parser import extract_text_from_docx

text = extract_text_from_docx(r"C:\Users\shubh\Downloads\SHUBHAM_MALIK_RESUME_2025 word.docx")
print(text)