# app/services/vector_store.py
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from sentence_transformers import SentenceTransformer
from app.core.config import settings
import uuid

class RAGRetriever:
    def __init__(self):
        # Connect to the Qdrant container
        self.client = QdrantClient(host=settings.QDRANT_HOST, port=settings.QDRANT_PORT)
        
        # Load the local embedding model (same one used for indexing)
        self.model = SentenceTransformer("BAAI/bge-small-en-v1.5")
        self.collection_name = "docs"
        
        # Ensure the bucket (collection) exists
        self._ensure_collection()

    def _ensure_collection(self):
        try:
            collections = self.client.get_collections().collections
            exists = any(c.name == self.collection_name for c in collections)
            if not exists:
                self.client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=VectorParams(size=384, distance=Distance.COSINE),
                )
        except Exception as e:
            print(f"Error connecting to Qdrant: {e}")

    def index_documents(self, chunks: list[dict]):
        points = []
        for chunk in chunks:
            # Generate the numeric vector for the text
            vector = self.model.encode(chunk["text"]).tolist()
            
            points.append(PointStruct(
                id=str(uuid.uuid4()),
                vector=vector,
                payload={
                    "text": chunk["text"],
                    "metadata": chunk["metadata"]
                }
            ))
        
        self.client.upsert(collection_name=self.collection_name, points=points)

    async def search(self, query: str, limit: int = 5):
        """
        Takes a text query, converts it to a vector, and finds matches in Qdrant.
        """
        # 1. Convert the user's question into a vector
        query_vector = self.model.encode(query).tolist()

        # 2. Search Qdrant (using the CORRECT collection name 'docs')
        search_result = self.client.query_points(
            collection_name=self.collection_name,
            query=query_vector,
            limit=limit
        )

        # 3. Format the results so the Reranker can understand them
        formatted_results = []
        for point in search_result.points:
            formatted_results.append({
                "text": point.payload.get("text", ""),
                "metadata": point.payload.get("metadata", {}),
                "score": point.score
            })
            
        return formatted_results
