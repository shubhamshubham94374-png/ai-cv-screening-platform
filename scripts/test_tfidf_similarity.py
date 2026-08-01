from app.services.matching.text_similarity import compute_tfidf_similarity
from app.services.matching.semantic_similarity import compute_semantic_similarity

resume_text = """
Software Engineering student with solid knowledge of Data Structures and Algorithms and practical
experience in Java-based application development. Built a responsive e-commerce website using
HTML, CSS, and JavaScript.
"""

job_description = """
We are hiring a Backend Developer with experience in Java development and web application development.
Experience with JavaScript and building responsive websites is a plus.
"""

unrelated_text = """
Looking for an experienced chef with knowledge of French cuisine and restaurant management.
"""

# Also test a conceptually related but differently-worded pair
paraphrased_jd = """
Seeking a candidate skilled in backend engineering using Java, along with frontend scripting abilities
and a track record of shipping user-facing web products.
"""

print("--- TF-IDF Similarity ---")
print(f"Resume vs Relevant JD: {compute_tfidf_similarity(resume_text, job_description)}")
print(f"Resume vs Unrelated JD: {compute_tfidf_similarity(resume_text, unrelated_text)}")
print(f"Resume vs Paraphrased JD: {compute_tfidf_similarity(resume_text, paraphrased_jd)}")

print("\n--- Semantic Similarity ---")
print(f"Resume vs Relevant JD: {compute_semantic_similarity(resume_text, job_description)}")
print(f"Resume vs Unrelated JD: {compute_semantic_similarity(resume_text, unrelated_text)}")
print(f"Resume vs Paraphrased JD: {compute_semantic_similarity(resume_text, paraphrased_jd)}")