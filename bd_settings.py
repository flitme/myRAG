from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams

client = QdrantClient(url="http://localhost:6333")

if not client.collection_exists(collection_name="docs"):
    client.create_collection(
        collection_name="docs",
        vectors_config=VectorParams(size=1024, distance=Distance.COSINE),
    )