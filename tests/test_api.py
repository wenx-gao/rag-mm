def test_upload_endpoint(client, tmp_path):
    # Create a dummy file
    file_path = tmp_path / "test.pdf"
    file_path.write_text("dummy content")
    
    with open(file_path, "rb") as f:
        response = client.post("/upload", files={"file": ("test.pdf", f, "application/pdf")})
    
    assert response.status_code == 200
    assert "task_id" in response.json()
    assert response.json()["status"] == "processing"

def test_query_endpoint_structure(client):
    # Mock the LLM service to avoid calling real Ollama
    with patch("app.api.endpoints.generate_answer") as mock_gen:
        mock_gen.return_value = {
            "answer": "Tested answer [1]",
            "sources": [{"citation_id": 1, "document": "doc.pdf"}]
        }
        
        response = client.post("/query", params={"question": "test?"})
        
        assert response.status_code == 200
        data = response.json()
        assert "answer" in data
        assert "sources" in data
        assert isinstance(data["sources"], list)
