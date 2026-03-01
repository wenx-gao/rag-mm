from qdrant_client import QdrantClient
from sentence_transformers import CrossEncoder
from app.core.config import settings

class RAGRetriever:
    def __init__(self):
        self.client = QdrantClient(
            host=settings.QDRANT_HOST, 
            port=settings.QDRANT_PORT
        )
        # Requirement 3: Local Reranker
        self.reranker = CrossEncoder('BAAI/bge-reranker-base')

    async def search(self, query: str, limit=5):
        # 1. Perform Hybrid Search (Vector + BM25)
        # Qdrant supports this natively via 'prefetch'
        results = self.client.query_points(...) 
        
        # 2. Rerank results
        passages = [res.payload['text'] for res in results.points]
        scores = self.reranker.predict([(query, p) for p in passages])
        
        # Combine and sort
        combined = sorted(zip(results.points, scores), key=lambda x: x[1], reverse=True)
        return combined[:3]

# app/services/vector_store.py (Update)

def index_documents(self, chunks: list[dict]):
    points = []
    for i, chunk in enumerate(chunks):
        # Generate embedding for the text
        vector = self.embedding_model.encode(chunk["text"])
        
        points.append(
            PointStruct(
                id=str(uuid.uuid4()),
                vector=vector.tolist(),
                payload={
                    "text": chunk["text"],
                    "metadata": chunk["metadata"] # This contains source, page_no, type
                }
            )
        )
    self.client.upsert(collection_name="docs", points=points)
