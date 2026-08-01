from app.services.parsing.pdf_parser import extract_text_from_pdf

text = extract_text_from_pdf(r"C:\Users\shubh\Downloads\22BCS17074_Shubham_Malik_2026.pdf")
print(text)