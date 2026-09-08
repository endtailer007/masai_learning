import numpy as np

knowledge_base = [
    "Linear regression finds the best fit line through the data points.",
    "Decision trees make predictions by asking a series of yes/no questions.",
    "Random forest combines hundreds of decision trees and lets them vote, reducing overfitting and improving accuracy.",
    "Overfitting happens when a model memorizes the training data, including noise.",
]

kb_embeddings = [
    [0.10, 0.85, -0.05, 0.20],
    [0.30, 0.10, 0.60, -0.15],
    [0.28, 0.15, 0.58, -0.10],
    [0.05, -0.20, 0.10, 0.90],
]

query_embedding = [0.06, -0.18, 0.12, 0.88]


def cosine_similarity(vector_1, vector_2):
    # TODO: convert both inputs to numpy arrays, compute the dot product,
    # and divide by the product of the two vector norms
    v1 = np.array(vector_1)
    v2 = np.array(vector_2)
    dot_product = np.dot(v1,v2)
    norm_v1 = np.linalg.norm(v1)
    norm_v2 = np.linalg.norm(v2)
    denominator = norm_v1 * norm_v2
    return dot_product / denominator if denominator != 0 else 0.0


def semantic_search(query_embedding, kb_embeddings, knowledge_base, top_k=2):
    # TODO: compute cosine_similarity between query_embedding and every
    # entry in kb_embeddings, sort descending, return top_k (score, index, text) tuples
    result = []
    for i, kb_embedding in enumerate(kb_embeddings):
        score = cosine_similarity(query_embedding, kb_embedding)
        result.append((float(score), i, knowledge_base[i]))

    result.sort(key=lambda item: item[0], reverse=True)
    return result[:top_k]


if __name__ == "__main__":
    print(semantic_search(query_embedding, kb_embeddings, knowledge_base, top_k=2))