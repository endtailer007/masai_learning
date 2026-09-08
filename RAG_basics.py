import re
from collections import Counter
import numpy as np
hr_document = """Employees who have completed their first six months of probation are eligible to work from home for up to two days per week.

Yes.

All annual leave requests must be submitted at least two weeks in advance through the HR portal for manager approval."""

security_document = """Passwords must contain at least one uppercase letter, one lowercase letter, one number, and one special character.

N/A

Passwords must be changed every 90 days and cannot reuse any of the previous five passwords used on the account."""

sample_question = "What is the work from home policy?"

def chunk_documents(text, source_name):
    # TODO: split text into paragraphs on blank lines, skip fragments < 50 chars,
    # tag each kept chunk with source_name, return a list of {"text": ..., "source": ...}
    chunks = []
    text_chunks = text.split("\n\n")
    for i in text_chunks:
        if len(i) < 50:
            pass
        else:
            chunks.append({"text": i, "source": source_name})
    return chunks

def text_to_vector(text):
    # TODO: lower-case, extract alphanumeric words, return a word-frequency structure
        words = re.findall(r"\b\w+\b", text.lower())
        words_frequency = dict(Counter(words))
        return words_frequency

def cosine_similarity(vec1, vec2):
    # TODO: compute the cosine similarity between two word-frequency vectors,
    # guarding against a zero-magnitude vector
    vocabulary = sorted(set(vec1.keys()) | set(vec2.keys()))
    v1 = np.array([vec1.get(word,0) for word in vocabulary],dtype=float)
    v2 = np.array([vec2.get(word,0) for word in vocabulary],dtype=float)
    dot_product = float(np.dot(v1, v2))
    denominator = np.linalg.norm(v1) * np.linalg.norm(v2)
    return dot_product / denominator if denominator != 0 else 0.0
def retrieve(chunks, question, n_results=3):
    # TODO: score every chunk against the question's vector using cosine_similarity
    result = []
    question_vector = text_to_vector(question)

    for chunk in chunks:
        chunk_vector = text_to_vector(chunk['text'])
        score = cosine_similarity(chunk_vector, question_vector)
        result.append((chunk['text'], chunk['source'], round(float(score), 4)))
    result.sort(key=lambda item: item[2], reverse=True)
    return result[:n_results]
    # sort descending, return the top n_results as (text, source, score) tuples

if __name__ == "__main__":
    hr_chunks = chunk_documents(hr_document, "HR Policy")
    security_chunks = chunk_documents(security_document, "Security Policy")
    all_chunks = hr_chunks + security_chunks
    print(retrieve(hr_chunks, sample_question, n_results=1))