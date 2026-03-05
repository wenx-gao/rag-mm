# app/models/schemas.py
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

# --- Document Processing Schemas ---

class UploadResponse(BaseModel):
    task_id: str
    filename: str
    status: str = "processing"

# --- RAG Query Schemas ---

class QueryRequest(BaseModel):
    question: str = Field(..., example="What are the technical capacities of the feeder?")
    top_k: int = Field(default=20, description="Chunks to retrieve")
    rerank: bool = Field(default=True)

class Citation(BaseModel):
    citation_id: int
    document: str
    page: Optional[int] = None
    # We use 'str' here instead of an Enum to allow Docling's specific types 
    # like ListItem, SectionHeader, TableItem, etc.
    element_type: str 
    snippet: Optional[str] = None

class QueryResponse(BaseModel):
    answer: str
    sources: List[Citation]


# from pydantic import BaseModel, Field
# from typing import List, Optional, Dict, Any
# from enum import Enum

# # --- Enums ---

# class ElementType(str, Enum):
#     TEXT = "text"
#     TABLE = "table"
#     IMAGE = "image"
#     CHART = "chart"

# # --- Document Processing Schemas (Async/Celery) ---

# class UploadResponse(BaseModel):
#     """Response returned immediately after file upload."""
#     task_id: str = Field(..., description="The ID of the background Celery task")
#     filename: str
#     status: str = "processing"

# class TaskStatus(BaseModel):
#     """Response for checking the status of a document ingestion task."""
#     task_id: str
#     status: str # PENDING, PROGRESS, SUCCESS, FAILURE
#     result: Optional[Dict[str, Any]] = None

# # --- RAG Query Schemas ---

# class QueryRequest(BaseModel):
#     """The user's question and optional parameters."""
# #    question: str = Field(..., example="What languages are listed in this document as skills?")
# #    question: str = Field(..., example="What was the total revenue in the Q3 excel sheet?")
#     question: str = Field(..., example="What is the Capacity and Motor power of the Lime stone Feeder?")

#     top_k: int = Field(default=15, description="Number of chunks to retrieve before reranking")
#     rerank: bool = Field(default=True, description="Whether to apply the local BGE reranker")

# # class Citation(BaseModel):
# #     """Requirement 7: Source attribution for the LLM's answer."""
# #     citation_id: int
# #     document: str = Field(..., description="Name of the source file")
# #     page: Optional[int] = Field(None, description="Page number from the PDF/Docx")
# #     element_type: ElementType = Field(..., description="The type of data cited (table, text, etc.)")
# #     snippet: Optional[str] = Field(None, description="A small snippet of the cited text")

# class Citation(BaseModel):
#     citation_id: int
#     document: str
#     page: Optional[int] = None
#     # CHANGE THIS LINE: Change ElementType to str
#     element_type: str = Field(..., description="The type of data cited") 
#     snippet: Optional[str] = None

# class QueryResponse(BaseModel):
#     """The final response sent back to the user."""
#     answer: str = Field(..., description="The generated answer from the local LLM")
#     sources: List[Citation] = Field(..., description="List of documents used to generate this answer")
#     tokens_used: Optional[int] = None

# # --- Internal Data Schemas (Parser to Vector Store) ---

# class DocumentChunk(BaseModel):
#     """Represents a structured chunk created by Docling."""
#     content: str
#     metadata: Dict[str, Any] = {
#         "source": "",
#         "page_no": None,
#         "element_type": ElementType.TEXT,
#     }

# # --- Evaluation Schemas (Ragas) ---

# class EvalResult(BaseModel):
#     """Requirement 6: Result of a Ragas evaluation run."""
#     faithfulness: float
#     answer_relevance: float
#     context_precision: float
#     average_score: float
