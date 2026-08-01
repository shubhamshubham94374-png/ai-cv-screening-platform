from app.services.parsing.resume_parser import parse_resume
import json

result = parse_resume(r"C:\Users\shubh\Downloads\22BCS17074_Shubham_Malik_2026.pdf")

# Print everything except raw_text (too long for terminal readability)
for key, value in result.items():
    if key != "raw_text":
        print(f"{key}: {value}")

print(f"\nraw_text length: {len(result['raw_text'])} characters")
