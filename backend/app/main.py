from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, UploadFile, File, Depends
from sqlalchemy.orm import Session
import logging
import os
import shutil

from app.db.database import engine, Base, SessionLocal
from app.models.document import Document
from app.models.chunk import DocumentChunk
from app.models.query_history import QueryHistory

from app.services.extractor import extract_text
from app.services.chunker import chunk_text
from app.services.embedder import generate_embedding
from app.services.faiss_service import add_embeddings, search
from app.services.llm import generate_answer


# ------------------ APP INIT ------------------
app = FastAPI()

# ------------------ LOGGING ------------------
LOG_DIR = "/opt/app/logs"
os.makedirs(LOG_DIR, exist_ok=True)

logging.basicConfig(
    filename=os.path.join(LOG_DIR, "app.log"),
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# ------------------ CORS ------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------ DB INIT ------------------
Base.metadata.create_all(bind=engine)


# ------------------ DB DEPENDENCY ------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ------------------ ROUTES ------------------

@app.get("/")
def home():
    return {"message": "Backend running"}


# ------------------ UPLOAD ------------------
@app.post("/upload")
def upload_file(file: UploadFile = File(...), db: Session = Depends(get_db)):
    try:
        file_path = f"/opt/app/uploads/{file.filename}"

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        logging.info(f"File saved: {file.filename}")

        doc = Document(filename=file.filename, path=file_path)

        db.add(doc)
        db.commit()
        db.refresh(doc)

        logging.info(f"Document stored in DB: ID={doc.id}")

        return {"id": doc.id, "filename": file.filename}

    except Exception as e:
        logging.error(f"Upload failed: {str(e)}")
        raise


# ------------------ PROCESS ------------------
@app.post("/process/{doc_id}")
def process_document(doc_id: int, db: Session = Depends(get_db)):
    doc = db.query(Document).filter(Document.id == doc_id).first()

    if not doc:
        return {"error": "Document not found"}

    text = extract_text(doc.path)
    chunks = chunk_text(text)

    for chunk in chunks:
        db_chunk = DocumentChunk(
            document_id=doc.id,
            content=chunk
        )
        db.add(db_chunk)

    doc.status = "processed"
    db.commit()

    logging.info(f"Processed document ID: {doc_id}")

    return {"message": "Document processed", "chunks": len(chunks)}


# ------------------ EMBEDDING ------------------
@app.post("/embed/{doc_id}")
def embed_document(doc_id: int, db: Session = Depends(get_db)):
    chunks = db.query(DocumentChunk).filter(
        DocumentChunk.document_id == doc_id
    ).all()

    texts = [chunk.content for chunk in chunks]
    embeddings = [generate_embedding(text) for text in texts]

    add_embeddings(embeddings, texts)

    logging.info(f"Embeddings created for doc ID: {doc_id}")

    return {"message": "Embeddings stored", "count": len(texts)}


# ------------------ SEARCH ------------------
@app.post("/search")
def semantic_search(query: str):
    query_embedding = generate_embedding(query)
    results = search(query_embedding)

    return {"results": results}


# ------------------ ASK ------------------
@app.post("/ask")
def ask_question(query: str, db: Session = Depends(get_db)):
    try:
        logging.info(f"User query: {query}")

        query_embedding = generate_embedding(query)
        results = search(query_embedding)

        if not results:
            return {"answer": "No relevant data found"}

        context = "\n".join(results)
        answer = generate_answer(context, query)

        new_query = QueryHistory(
            question=query,
            answer=answer
        )

        db.add(new_query)
        db.commit()

        return {
            "question": query,
            "answer": answer,
            "context": results
        }

    except Exception as e:
        logging.error(f"Ask API error: {str(e)}")
        raise


# ------------------ DASHBOARD ------------------
@app.get("/dashboard")
def get_dashboard(db: Session = Depends(get_db)):
    total_docs = db.query(Document).count()
    total_chunks = db.query(DocumentChunk).count()
    total_queries = db.query(QueryHistory).count()

    return {
        "total_documents": total_docs,
        "total_chunks": total_chunks,
        "total_queries": total_queries
    }
