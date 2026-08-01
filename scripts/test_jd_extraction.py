from app.services.parsing.jd_parser import parse_job_description

sample_jd = """
We are hiring a Backend Developer with 3+ years of experience.
Bachelor's degree in Computer Science required.

Required Skills:
Python, SQL, Django, REST API, Git

Preferred Skills:
Docker, AWS, Kubernetes, React
"""

result = parse_job_description(text=sample_jd)

for key, value in result.items():
    if key != "raw_description":
        print(f"{key}: {value}")