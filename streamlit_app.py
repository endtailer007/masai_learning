import os
from pathlib import Path

import chromadb
import streamlit as st
from dotenv import load_dotenv
from google import genai
from google.genai import types

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
CHROMA_DIR = BASE_DIR / "chroma_store"
COLLECTION_NAME = "Company_docs_streamlit"
DEFAULT_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.5-flash")

load_dotenv(BASE_DIR / ".env")
load_dotenv(BASE_DIR.parent / ".env")


def load_document(file_path: Path) -> str:
    """Read a single text document."""
    return file_path.read_text(encoding="utf-8")


def chunk_document(text: str, source_name: str) -> list[dict]:
    """Split a document into paragraph-sized chunks."""
    paragraphs = text.strip().split("\n\n")
    chunks = []
    for paragraph in paragraphs:
        cleaned = paragraph.strip()
        if len(cleaned) < 50:
            continue
        if cleaned.startswith("======"):
            continue
        chunks.append({"text": cleaned, "source": source_name})
    return chunks


def load_and_chunk_all_documents() -> tuple[list[dict], int]:
    """Load all .txt documents from the data folder and chunk them."""
    all_chunks = []
    document_paths = sorted(DATA_DIR.glob("*.txt"))
    for file_path in document_paths:
        text = load_document(file_path)
        source_name = file_path.stem.replace("_", " ").title()
        all_chunks.extend(chunk_document(text, source_name))
    return all_chunks, len(document_paths)


def get_collection(name: str = COLLECTION_NAME):
    """Create or return the persistent Chroma collection."""
    client = chromadb.PersistentClient(path=str(CHROMA_DIR))
    return client.get_or_create_collection(name=name)


def vectorize_chunks(chunks: list[dict], collection) -> None:
    """Store chunk text and metadata in Chroma. Chroma creates embeddings internally."""
    documents = []
    ids = []
    metadatas = []

    for index, chunk in enumerate(chunks):
        documents.append(chunk["text"])
        ids.append(f"{chunk['source'].replace(' ', '_').lower()}_{index}")
        metadatas.append({"source": chunk["source"]})

    collection.upsert(documents=documents, ids=ids, metadatas=metadatas)


@st.cache_resource(show_spinner=False)
def prepare_knowledge_base():
    """Load documents, chunk them, and upsert them into Chroma once per app session."""
    chunks, document_count = load_and_chunk_all_documents()
    collection = get_collection()
    vectorize_chunks(chunks, collection)
    return collection, document_count, len(chunks)


def retrieve_chunks(query_text: str, collection, n_results: int = 2) -> list[dict]:
    """Retrieve the top matching chunks for a user query.

    Passing query_texts lets Chroma convert the query into an embedding internally
    and compare it with the stored document vectors.
    """
    results = collection.query(query_texts=[query_text], n_results=n_results)
    documents = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]

    hits = []
    for document, metadata in zip(documents, metadatas):
        hits.append({
            "text": document,
            "source": (metadata or {}).get("source", "Unknown source"),
        })
    return hits


def call_gemini_api_chat(system_prompt: str, user_payload: str, model_name: str = DEFAULT_MODEL, temperature: float = 0.2) -> str:
    """Use Gemini chat with API-key authentication and return the text response."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY was not found. Add it to your .env file.")

    client = genai.Client(api_key=api_key)
    chat = client.chats.create(
        model=model_name,
        config=types.GenerateContentConfig(
            system_instruction=system_prompt,
            temperature=temperature,
        ),
    )
    response = chat.send_message(user_payload)
    return response.text or "I couldn't generate an answer right now."


def answer_question(question: str, hits: list[dict]) -> str:
    """Build the RAG prompt from retrieved chunks and ask Gemini for an answer."""
    context = "\n\n".join(hit["text"] for hit in hits)
    if not context.strip():
        return "I could not find relevant chunks in the documents."

    system_prompt = (
        "You are a helpful assistant that provides information based only on the provided context. "
        "If the context does not contain enough information to answer the question, "
        "say 'I don't have enough information to answer this question.' "
        "Do not make up an answer or provide information that is not in the context."
    )
    user_payload = f"""
Context from the documents:
{context}

User question:
{question}
"""
    return call_gemini_api_chat(system_prompt, user_payload)


st.set_page_config(page_title="NovaTech Solutions Internal Assistant", page_icon="📄", layout="centered")
st.title("📄 NovaTech Solutions Internal Assistant")
st.caption("I will answer your queries related to NovaTech Solutions policies.")

with st.spinner("Reading documents, chunking text, and vectorizing in ChromaDB..."):
    collection, document_count, chunk_count = prepare_knowledge_base()

st.success(f"Chunking completed. Vectorized {chunk_count} chunks from {document_count} documents.")

with st.form("rag_query_form", clear_on_submit=True):
    query = st.text_input("Ask a question about the company documents")
    submitted = st.form_submit_button("Get Answer")

if submitted:
    query_text = (query or "").strip()
    if not query_text:
        st.warning("Please enter a question.")
    else:
        hits = retrieve_chunks(query_text, collection, n_results=2)
        if not hits:
            st.warning("No matching chunks were found.")
        else:
            st.subheader("Top 2 retrieved chunks")
            for index, hit in enumerate(hits, start=1):
                st.write(f"Chunk {index} — Source: {hit['source']}")

            with st.spinner("Generating answer..."):
                answer = answer_question(query_text, hits)

            st.subheader("Answer")
            st.write(answer)

