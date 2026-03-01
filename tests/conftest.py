import pytest
from fastapi.testclient import TestClient
from main import app  # Assuming your FastAPI app is in main.py

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def mock_docling_result():
    """Simulates what Docling returns after parsing."""
    return [
        {"text": "Revenue grew by 10%.", "metadata": {"source": "data.pdf", "page_no": 1, "type": "text"}},
        {"text": "| Q1 | Q2 |\n|----|----|", "metadata": {"source": "table.xlsx", "page_no": None, "type": "table"}}
    ]
