from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from sentence_transformers import SentenceTransformer
import uuid

client = QdrantClient(host="qdrant", port=6333)  # or URL if cloud
model = SentenceTransformer('all-MiniLM-L6-v2')

def create_collection(collection_name: str):
    if not client.collection_exists(collection_name):
        client.recreate_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(size=384, distance=Distance.COSINE)
        )

def add_to_qdrant(collection_name: str, text: str, metadata: dict):
    create_collection(collection_name)
    embedding = model.encode(text).tolist()
    point = PointStruct(
        id=str(uuid.uuid4()),
        vector=embedding,
        payload=metadata
    )
    client.upsert(collection_name=collection_name, points=[point])


def push_to_qdrant(file, title, uploader, faculty, doc_type):
    content = file.read().decode('utf-8', errors='ignore')
    file.seek(0)
    metadata = {
        "type": doc_type,
        "title": title,
        "uploaded_by": uploader,
        "faculty": faculty
    }
    add_to_qdrant("lecture_materials", content, metadata)

