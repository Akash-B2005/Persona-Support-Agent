import os
from pathlib import Path

import chromadb
from dotenv import load_dotenv
from pypdf import PdfReader
from google import genai
from langchain_text_splitters import RecursiveCharacterTextSplitter

# =====================================
# Load Environment Variables
# =====================================

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError(
        "GEMINI_API_KEY not found. Please add it to your .env file."
    )

# =====================================
# Gemini Client
# =====================================

client = genai.Client(api_key=GEMINI_API_KEY)

# =====================================
# ChromaDB Setup
# =====================================

chroma_client = chromadb.PersistentClient(
    path="./chroma_db"
)

collection = chroma_client.get_or_create_collection(
    name="support_kb"
)

# =====================================
# Read Text Files
# =====================================

def read_text_file(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return ""

# =====================================
# Read PDF Files
# =====================================

def read_pdf(file_path):
    text = ""

    try:
        reader = PdfReader(file_path)

        for page in reader.pages:
            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

    except Exception as e:
        print(f"PDF Error ({file_path}): {e}")

    return text

# =====================================
# Split Text
# =====================================

def split_text(text):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=400,
        chunk_overlap=40
    )

    return splitter.split_text(text)

# =====================================
# Generate Embeddings
# =====================================

def get_embedding(text):
    try:
        response = client.models.embed_content(
            model="text-embedding-004",
            contents=text
        )

        return response.embeddings[0].values

    except Exception as e:
        print(f"Embedding Error: {e}")
        return None

# =====================================
# Load Documents
# =====================================

def load_documents(data_folder="data"):

    all_chunks = []

    data_path = Path(data_folder)

    if not data_path.exists():
        print(f"Folder not found: {data_folder}")
        return []

    for file_path in data_path.iterdir():

        if file_path.suffix.lower() in [".txt", ".md"]:

            print(f"Reading: {file_path.name}")

            text = read_text_file(file_path)

        elif file_path.suffix.lower() == ".pdf":

            print(f"Reading: {file_path.name}")

            text = read_pdf(file_path)

        else:
            continue

        if not text.strip():
            continue

        chunks = split_text(text)

        all_chunks.extend(chunks)

    return all_chunks

# =====================================
# Build Vector Database
# =====================================

def build_vector_db():

    chunks = load_documents()

    if not chunks:
        print("No chunks found.")
        return

    print(f"\nTotal chunks: {len(chunks)}")

    existing_ids = set()

    try:
        existing = collection.get()

        if existing and existing["ids"]:
            existing_ids = set(existing["ids"])

    except Exception:
        pass

    stored_count = 0

    for idx, chunk in enumerate(chunks):

        chunk_id = f"chunk_{idx}"

        if chunk_id in existing_ids:
            continue

        vector = get_embedding(chunk)

        if vector is None:
            continue

        try:
            collection.add(
                ids=[chunk_id],
                embeddings=[vector],
                documents=[chunk]
            )

            stored_count += 1

        except Exception as e:
            print(f"Failed to store {chunk_id}: {e}")

    print(f"\nStored {stored_count} chunks successfully.")
    print("Knowledge Base Ready!")

# =====================================
# Search Knowledge Base
# =====================================

def search_knowledge_base(query, n_results=3):

    query_vector = get_embedding(query)

    if query_vector is None:
        return []

    try:

        results = collection.query(
            query_embeddings=[query_vector],
            n_results=n_results
        )

        if not results["documents"]:
            return []

        return results["documents"][0]

    except Exception as e:
        print(f"Search Error: {e}")
        return []

# =====================================
# Main Test
# =====================================

if __name__ == "__main__":

    print("\n===== BUILDING VECTOR DATABASE =====\n")

    build_vector_db()

    print("\n===== TEST SEARCH =====\n")

    query = "How can I reset my password?"

    docs = search_knowledge_base(query)

    if not docs:
        print("No results found.")

    else:
        for i, doc in enumerate(docs, start=1):
            print(f"\nResult {i}")
            print("-" * 50)
            print(doc)

