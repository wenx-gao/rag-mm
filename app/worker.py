# app/worker.py
from app.core.celery_app import celery_app
from app.services.parser import DocumentParser
from app.services.vector_store import RAGRetriever

# We define these as None first
_parser = None
_retriever = None

def get_parser():
    global _parser
    if _parser is None:
        _parser = DocumentParser()
    return _parser

def get_retriever():
    global _retriever
    if _retriever is None:
        _retriever = RAGRetriever()
    return _retriever

@celery_app.task(name="process_document")
def process_document(file_path: str):
    # These will only initialize the first time a task actually runs
    parser = get_parser()
    retriever = get_retriever()
    
    try:
        print(f"Starting to parse: {file_path}")
        chunks = parser.parse(file_path)
        retriever.index_documents(chunks)
        print(f"Successfully indexed {len(chunks)} chunks.")
        return {"status": "success", "chunks": len(chunks)}
    except Exception as e:
        print(f"Error processing document: {e}")
        return {"status": "error", "message": str(e)}
