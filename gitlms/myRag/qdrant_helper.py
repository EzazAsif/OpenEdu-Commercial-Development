from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from sentence_transformers import SentenceTransformer
import uuid
import fitz  # PyMuPDF

client = QdrantClient(host="qdrant", port=6333)  # or URL if cloud
#model = SentenceTransformer('all-MiniLM-L6-v2')



def extract_pdf_text(uploaded_file, chunk_size=500, overlap=100):
    uploaded_file.seek(0)

    file_bytes = uploaded_file.read()
    if not file_bytes:
        raise ValueError("The uploaded file is empty or corrupted.")

    try:
        doc = fitz.open(stream=file_bytes, filetype="pdf")
    except Exception as e:
        raise ValueError(f"Failed to open PDF: {e}")

    full_text = ""
    for page in doc:
        full_text += page.get_text()

    uploaded_file.seek(0)  # Reset for Django DB save

    # Split into words
    words = full_text.split()
    chunks = []
    i = 0

    while i < len(words):
        chunk = words[i:i + chunk_size]
        chunks.append(" ".join(chunk))
        i += chunk_size - overlap  # Move forward with overlap

    return chunks


def push_to_qdrant(file, title, url, doc_type):
    chunks = extract_pdf_text(file)  # returns list of 500-word chunks

    for idx, chunk in enumerate(chunks):
        metadata = {
            "type": doc_type,
            "title": title,
            "chunk_index": idx,
            "url":url,
            "content": chunk
        }
        add_to_qdrant("lecture_materials", chunk, metadata)  # ✅ one string per call


def create_collection(collection_name: str):
    if not client.collection_exists(collection_name):
        client.recreate_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(size=384, distance=Distance.COSINE)
        )

        

def add_to_qdrant(collection_name: str, text: str, metadata: dict):
    create_collection(collection_name)

    # Ensure input is a single string
    if not isinstance(text, str):
        raise ValueError("Each input to add_to_qdrant must be a single string (chunk).")

    embedding = model.encode(text).tolist()

    if not isinstance(embedding, list) or not all(isinstance(x, float) for x in embedding):
        raise ValueError("Generated embedding is invalid or not a 1D list of floats.")

    point = PointStruct(
        id=str(uuid.uuid4()),
        vector=embedding,
        payload=metadata
    )
    client.upsert(collection_name=collection_name, points=[point])





def search_qdrant(collection_name: str, query: str, top_k: int = 5):
    query_vec = model.encode(query).tolist()
    results = client.search(
        collection_name=collection_name,
        query_vector=query_vec,
        limit=top_k
    )
    return results

