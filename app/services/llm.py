import httpx
from app.core.config import settings

async def call_ollama(prompt: str):
    # settings.OLLAMA_BASE_URL will be "http://ollama:11434" inside Docker
    url = f"{settings.OLLAMA_BASE_URL}/api/generate"
    
    async with httpx.AsyncClient() as client:
        response = await client.post(
            url,
            json={"model": "llama3:8b", "prompt": prompt}
        )
        return response.json()

async def generate_answer(question: str, context: list):
    # Requirement 4: Local Ollama Request
    prompt = f"Context: {context}\n\nQuestion: {question}\nAnswer with citations:"
    
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://localhost:11434/api/generate",
            json={"model": "llama3:8b-q4_K_M", "prompt": prompt, "stream": False}
        )# app/services/llm.py (Update)

async def generate_answer_with_citations(question: str, retrieved_chunks: list):
    # 1. Prepare the Context with IDs
    context_str = ""
    source_map = {}
    
    for i, chunk in enumerate(retrieved_chunks):
        cid = i + 1  # Citation ID
        context_str += f"--- Source [{cid}] ---\n{chunk.payload['text']}\n\n"
        source_map[cid] = chunk.payload['metadata']

    # 2. Build the System Prompt
    system_prompt = (
        "You are a helpful assistant. Answer the question using ONLY the provided context. "
        "Every time you state a fact, you MUST cite the source number in brackets, e.g., [1]. "
        "If a source is a table or diagram, mention that specifically."
    )
    
    user_prompt = f"Context:\n{context_str}\n\nQuestion: {question}"

    # 3. Call local Ollama
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3:8b-q4_K_M", 
                "system": system_prompt,
                "prompt": user_prompt, 
                "stream": False
            }
        )
    
    answer_text = response.json()["response"]
    
    # 4. Map the used citations back to actual metadata
    final_sources = []
    for cid, meta in source_map.items():
        if f"[{cid}]" in answer_text:
            final_sources.append({
                "citation_id": cid,
                "document": meta["source"],
                "page": meta.get("page_no"),
                "type": meta.get("type")
            })

    return {"answer": answer_text, "sources": final_sources}
    return response.json()
