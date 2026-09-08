import os
from pathlib import Path
from google import genai
from dotenv import load_dotenv
import chromadb
from google.genai import types

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"

load_dotenv(dotenv_path=Path(__file__).with_name(".env"))
def call_gemini_api(content,question):
    """
    Calls gemini API to generate content based on the provided input,parm is content
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY was not found. Make sure it is set in the .env file.")
    client = genai.Client(api_key=api_key)

    user_payload = f"""
    Context from the documents: 
    {content}
    
    User question: 
    {question}
    """
    system_prompt = ("You are a helpful assistant that provides information based only on the provided context."
        "If the context does not contain enough information to answer the question"
        "Say 'I don't have enough information to answer this question.'"
        "Do not make up an answer or provide information that is not in the context.")

    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=user_payload,
        config=types.GenerateContentConfig(
            system_instruction=system_prompt,
            temperature=0.2
        )
    )
    answers = response.text
    return answers

def call_gemini_api_chat(system_prompt, user_payload, model_name="gemini-3.5-flash", temperature=0.2):
    """
    Calls Gemini using a chat session and send_message() with API-key auth.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY was not found. Make sure it is set in the .env file.")

    client = genai.Client(api_key=api_key)
    chat = client.chats.create(
        model=model_name,
        config=types.GenerateContentConfig(
            system_instruction=system_prompt,
            temperature=temperature,
        ),
    )
    response = chat.send_message(user_payload)
    answers = response.text
    return answers
#Load and chunk the documents
def load_documents(file_path):
    """
    Loads the documents from the specified file path and returns the content as a string.
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        source_name = f.read()
    return source_name
def chunk_documents(text, source_name):
    """
    Splits the text into paragraphs, filters out short fragments, and returns a list of chunks with source information.
    """
    paragraphs = text.strip().split("\n\n")
    chunks = []
    for para in paragraphs:
        if len(para) < 50:
            continue
        if para.startswith("======"):
            continue
        chunks.append({
            "text" : para,
            "source" : source_name
        })
    return chunks

def get_chroma_collections(name="Company_docs",persist_dir= "./chroma_store"):
    """
    Initializes and returns a ChromaDB collection with the specified name and persistence directory.
    """
    persist_path = BASE_DIR / persist_dir
    client = chromadb.PersistentClient(path=str(persist_path))
    collections = client.get_or_create_collection(name=name)
    return collections

def vectorize_text(chunks,collection):
    """
    Converts the input text into a word-frequency vector.
    """
    documents = []
    ids = []
    metadata = []
    for i, chunk in enumerate(chunks):
        documents.append(chunk['text'])
        ids.append(f"chunk_{i}")
        metadata.append({"source": chunk["source"]})
    collection.upsert(
        documents = documents,
        ids = ids,
        metadatas = metadata
    )
def retrieve_chunks(query_text,collection,n_results=3):
    """
    Retrieves the top n_results chunks from the collection based on the query text.
    """
    results = collection.query(
        query_texts = [query_text],
        n_results = n_results
    )
    docs = results. get("documents",[[]])[0]
    metas = results.get("metadatas", [[]])[0]
    formatted = []
    for doc,meta in zip(docs,metas):
        formatted.append({
            "text": doc,
            "source": (meta or {}).get("source")
        })
    return formatted

hr_documents = load_documents(DATA_DIR / "company_hr_policy.txt")
security_documents = load_documents(DATA_DIR / "security_policy.txt")
engineering_standards = load_documents(DATA_DIR / "engineering_standards.txt")
onboarding_guide = load_documents(DATA_DIR / "onboarding_guide.txt")
product_knowledge_base = load_documents(DATA_DIR / "product_knowledge_base.txt")
hr_chunks = chunk_documents(hr_documents, "HR policy")
security_chunks = chunk_documents(security_documents, "Security policy")
engineering_chunks = chunk_documents(engineering_standards, "Engineering policy")
onboarding_chunks = chunk_documents(onboarding_guide, "Onboarding policy")
product_knowledge_chunks = chunk_documents(product_knowledge_base, "Product_Knowledge policy")
all_chunks = hr_chunks + security_chunks + engineering_chunks + onboarding_chunks + product_knowledge_chunks
print("completed chunking")
collect = get_chroma_collections("Company_docs")
vectorize_text(all_chunks, collect)
print("Completed vectorization")
def ask_rag(question, n_results=3, verbose = True):
    """
    Retrieves relevant chunks based on the question and generates a response using the Gemini API.
    """
    hits = retrieve_chunks(question, collect, n_results)
    if verbose:
        print("\n" + "=" * 60)
        print(f"❓ Question: {question}")
        print("=" * 60)
        print(f"Retrieved {len(hits)} chunks")
        for i, hit in enumerate(hits,1):
            preview = hit['text'][:100].replace("\n", " ") + "..."
            print(f"[{i}] [{hit['source']}] {preview}")
        print("=" * 60 + "\n")
    content = "\n\n".join(hit["text"] for hit in hits)
    system_prompt = (
        "You are a helpful assistant that provides information based only on the provided context. "
        "If the context does not contain enough information to answer the question, "
        "say 'I don't have enough information to answer this question.' "
        "Do not make up an answer or provide information that is not in the context."
    )
    user_payload = f"""
Context from the documents:
{content}

User question:
{question}
"""
    return call_gemini_api_chat(system_prompt, user_payload)
answer = ask_rag("What is the work from home policy?", 3)
print(answer)


