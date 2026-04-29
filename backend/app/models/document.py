from sqlalchemy import Column, Integer, String, TIMESTAMP
from app.db.database import Base
import datetime

class Document(Base):
    __tablename__ = "uploaded_documents"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String)
    path = Column(String)
    status = Column(String, default="uploaded")
    created_at = Column(TIMESTAMP, default=datetime.datetime.utcnow)
