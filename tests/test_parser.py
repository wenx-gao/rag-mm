import pytest
from app.services.parser import DocumentParser
from unittest.mock import MagicMock, patch

def test_excel_to_markdown_conversion(tmp_path):
    # Create a dummy CSV file
    d = tmp_path / "test.csv"
    d.write_text("name,age\nAlice,30\nBob,25")
    
    parser = DocumentParser()
    chunks = parser._parse_tabular(d)
    
    assert len(chunks) == 1
    assert "|" in chunks[0]["text"]  # Check if it's Markdown table format
    assert chunks[0]["metadata"]["type"] == "table"

@patch("app.services.parser.DocumentConverter")
def test_multimodal_pdf_parsing(mock_converter):
    # Mock Docling internal response
    parser = DocumentParser()
    # Logic to ensure it handles Docling elements...
    pass # In a real test, you'd verify iterate_items() is called
