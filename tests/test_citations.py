from app.services.llm import generate_answer_with_citations
import pytest
from unittest.mock import AsyncMock, patch

@pytest.mark.asyncio
async def test_citation_mapping_logic():
    # Setup: 1 retrieved chunk
    mock_chunks = [
        MagicMock(payload={
            "text": "The sky is blue.", 
            "metadata": {"source": "nature.pdf", "page_no": 5}
        })
    ]
    
    # Mocking the Ollama HTTP response
    mock_ollama_resp = {
        "response": "The sky is blue [1]."
    }

    with patch("httpx.AsyncClient.post") as mock_post:
        mock_post.return_value = MagicMock(status_code=200, json=lambda: mock_ollama_resp)
        
        result = await generate_answer_with_citations("Color of sky?", mock_chunks)
        
        # Verify citation was correctly mapped
        assert len(result["sources"]) == 1
        assert result["sources"][0]["document"] == "nature.pdf"
        assert result["sources"][0]["page"] == 5
        assert "[1]" in result["answer"]
