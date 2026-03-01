import torch
from sentence_transformers import CrossEncoder
from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)

class LocalReranker:
    def __init__(self, model_name: str = "BAAI/bge-reranker-base"):
        """
        Requirement 4: Runs locally on consumer hardware. 
        BGE-Reranker-Base is ~1GB and highly effective.
        """
        device = "cuda" if torch.cuda.is_available() else "cpu"
        logger.info(f"Loading Reranker ({model_name}) on {device}...")
        
        # Load the model once into VRAM/RAM
        self.model = CrossEncoder(model_name, device=device)

    def rerank(self, query: str, chunks: List[Dict[str, Any]], top_n: int = 3) -> List[Dict[str, Any]]:
        """
        Takes the query and a list of retrieved chunks (from Hybrid Search).
        Returns the top_n chunks sorted by relevance score.
        """
        if not chunks:
            return []

        # Prepare pairs for the CrossEncoder: [ [query, doc1], [query, doc2], ... ]
        # We use the 'text' content of the chunk for scoring
        sentence_pairs = [[query, chunk["text"]] for chunk in chunks]
        
        # Calculate scores (Higher is more relevant)
        scores = self.model.predict(sentence_pairs)

        # Attach scores to chunks and sort
        for i, score in enumerate(scores):
            chunks[i]["rerank_score"] = float(score)

        # Sort by score descending
        reranked_chunks = sorted(chunks, key=lambda x: x["rerank_score"], reverse=True)

        logger.info(f"Reranking complete. Top score: {reranked_chunks[0]['rerank_score']:.4f}")
        
        return reranked_chunks[:top_n]
