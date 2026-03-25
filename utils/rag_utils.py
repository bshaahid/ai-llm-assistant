import numpy as np


def cosine_similarity(vec1, vec2):
    vec1 = np.array(vec1)
    vec2 = np.array(vec2)

    denominator = np.linalg.norm(vec1) * np.linalg.norm(vec2)
    if denominator == 0:
        return 0.0

    return np.dot(vec1, vec2) / denominator


def get_top_k_chunks(question_embedding, chunk_embeddings, chunks, k=3):
    similarities = []

    for i, chunk_embedding in enumerate(chunk_embeddings):
        score = cosine_similarity(question_embedding, chunk_embedding)
        similarities.append((score, chunks[i]))

    similarities.sort(reverse=True, key=lambda x: x[0])

    top_chunks = [chunk for score, chunk in similarities[:k]]
    return top_chunks