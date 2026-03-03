from fastapi import APIRouter, UploadFile, File, HTTPException
from app.models.schemas import QueryRequest, QueryResponse, UploadResponse
from app.services.llm import generate_answer_with_citations
from app.worker import process_document
import os
import uuid

# In main.py, we will import this router
router = APIRouter()

@router.post("/upload", response_model=UploadResponse)
async def upload_file(file: UploadFile = File(...)):
    # Create storage dir if not exists
    os.makedirs("storage", exist_ok=True)
    
    file_path = f"storage/{uuid.uuid4()}_{file.filename}"
    with open(file_path, "wb") as f:
        f.write(await file.read())
    
    # Trigger the background Celery task
    task = process_document.delay(file_path)
    
    return {"task_id": task.id, "filename": file.filename}

@router.post("/query", response_model=QueryResponse)
async def query_rag(request: QueryRequest):
    # 1. Access the global state (initialized in main.py) --> avoid circular import crash
    from main import state
    
    # 2. Hybrid Search in Qdrant
    initial_chunks = await state.retriever.search(request.question, limit=request.top_k)
    
    if not initial_chunks:
        return {"answer": "I couldn't find any relevant information in your documents.", "sources": []}

    # 3. Rerank the results
    best_chunks = state.reranker.rerank(request.question, initial_chunks, top_n=3)
    
    # 4. Generate Answer with Citations using Ollama
    result = await generate_answer_with_citations(request.question, best_chunks)
    
    return result
