# Local Multimodal RAG

A private, local RAG system that processes PDF, Excel, and Images using Docling and Ollama.

## Features
- **Multimodal:** Handles tables and diagrams via Docling v2.
- **Local LLM:** Uses Ollama (Llama 3 8B) for private inference.
- **Reranking:** Implements BGE-Reranker for high accuracy.
- **Async Processing:** Background indexing with Celery and Redis.

## Setup
1. Clone the repo.
2. Ensure Docker Desktop is running.
3. Run `docker-compose up -d --build`.
4. Download the LLM: `docker exec -it rag-ollama ollama run llama3:8b`.
5. Access the API at `http://localhost:8000/docs`.

## How to Run
1. Start the system: `docker-compose up -d --build`
2. Download the model: `docker exec -it rag-ollama ollama run llama3:8b`
3. **Frontend:** Open `http://localhost:5173`
4. **API Docs:** Open `http://localhost:8000/docs`
