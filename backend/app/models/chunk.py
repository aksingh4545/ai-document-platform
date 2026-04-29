from sqlalchemy import Column, Integer, Text, ForeignKey
from app.db.database import Base

class DocumentChunk(Base):
    __tablename__ = "document_chunks"

    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey("uploaded_documents.id"))
    content = Column(Text)
