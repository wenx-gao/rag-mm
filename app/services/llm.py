# app/services/llm.py
import httpx
from app.core.config import settings

async def generate_answer_with_citations(question: str, best_chunks: list):
    """
    Sends the question and the best chunks to the local Ollama LLM.
    """
    context_str = ""
    source_map = {}
    
    # FIX: best_chunks is now a list of DICTIONARIES, not Objects
    for i, chunk in enumerate(best_chunks):
        cid = i + 1  # Citation ID (1, 2, 3...)
        
        # Use dictionary access ['text'] instead of .payload['text']
        text_content = chunk.get('text', 'No content')
        metadata = chunk.get('metadata', {})
        
        context_str += f"--- Source [{cid}] ---\n{text_content}\n\n"
        source_map[cid] = metadata

    # 2. Build the System Prompt
    system_prompt = (
        "You are a helpful assistant. Answer the question using ONLY the provided context. "
        "Every time you state a fact, you MUST cite the source number in brackets, e.g., [1]. "
        "If the answer is not in the context, say you don't know."
    )
    
    user_prompt = f"Context:\n{context_str}\n\nQuestion: {question}"

    # 3. Call local Ollama (inside the Docker network)
    url = f"{settings.OLLAMA_BASE_URL}/api/generate"
    
    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(
            url,
            json={
                "model": "llama3:8b", 
                "system": system_prompt,
                "prompt": user_prompt, 
                "stream": False
            }
        )
    
    raw_response = response.json()
    answer_text = raw_response.get("response", "No answer generated.")
    
    # 4. Map citations to actual metadata for the final response
    final_sources = []
    for cid, meta in source_map.items():
        if f"[{cid}]" in answer_text:
            final_sources.append({
                "citation_id": cid,
                "document": meta.get("source", "Unknown"),
                "page": meta.get("page_no"),
                "element_type": meta.get("type", "text")
            })

    return {"answer": answer_text, "sources": final_sources}
