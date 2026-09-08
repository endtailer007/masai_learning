knowledge_base = [
    "Linear regression finds the best line through data points",
    "Decision trees make predictions by asking a series of questions",
    "Random forests combine hundreds of decision trees and let them vote",
    "Overfitting happens when a model memorizes training data including noise",
    "Cosine similarity measures the angle between two vectors",
]
vocab = sorted(set(word.lower()for fact in knowledge_base for word in fact.split()))
def mock_embed(text):
    """
    Mock embedding function that returns a vector representation of the text.
    For simplicity, we will use a simple hash-based approach to generate a vector.
    In a real scenario, you would use a proper embedding model.
    """
    words = text.lower().split()
    return [words.count(v) for v in vocab]
def cosine_similarity(vec1,vec2):
    """
    Compute the cosine similarity between two vectors.
    """
    dot_product = sum(a*b for a,b in zip(vec1,vec2))
    norm1 = sum(a*a for a in vec1) ** 0.5
    norm2 = sum(b*b for b in vec2) ** 0.5
    if norm1 == 0 or norm2 == 0:
        return 0.0
    return dot_product / (norm1 * norm2)

kb_embeddings = [mock_embed(fact) for fact in knowledge_base]

def retrieve_(query, k = 3):
    """
    Retrieve the top k most relevant knowledge base entries for the given query.
    """
    query_vec = mock_embed(query)
    scored = [(fact, cosine_similarity(query_vec, kb_vec))for fact,kb_vec in zip(knowledge_base, kb_embeddings)]
    scored.sort(key = lambda x: x[1], reverse = True)
    k = min(k, len(scored))
    return scored[:k]
def mock_generate_answer(query, retrieved_chunks):
    """
    Mock answer generation function that combines the query with retrieved facts.
    In a real scenario, you would use a language model to generate a coherent answer.
    """
    context = " ".join(chunk for chunk,score in retrieved_chunks)
    return f"Based on retrieved facts : {context}"
query = "What happens when a model memorizes training data including noise?"
top_chunks = retrieve_(query, 1)
answer = mock_generate_answer(query, top_chunks)
print("Retrieved Chunks:", top_chunks)
print("Answers: ", answer)


