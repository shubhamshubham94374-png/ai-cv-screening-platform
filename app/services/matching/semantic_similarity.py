from sentence_transformers import SentenceTransformer, util

_model = SentenceTransformer("all-MiniLM-L6-v2")


def compute_semantic_similarity(text_a: str, text_b: str) -> float:
    """
    Computes cosine similarity between two texts using sentence embeddings,
    capturing conceptual/meaning-level similarity rather than just word overlap.
    Returns a score between 0.0 and 1.0.
    """
    if not text_a.strip() or not text_b.strip():
        return 0.0

    embeddings = _model.encode([text_a, text_b])
    similarity = util.cos_sim(embeddings[0], embeddings[1])
    return round(float(similarity[0][0]), 4)