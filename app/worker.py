# app/worker.py
from app.core.celery_app import celery_app
from app.services.parser import DocumentParser
from app.services.vector_store import RAGRetriever

# Initialize services
parser = DocumentParser()
# retriever = RAGRetriever() # Uncomment when vector_store is ready

@celery_app.task(name="process_document")
def process_document(file_path: str):
    try:
        chunks = parser.parse(file_path)
        # retriever.index_documents(chunks)
        return {"status": "success", "chunks": len(chunks)}
    except Exception as e:
        return {"status": "error", "message": str(e)}
