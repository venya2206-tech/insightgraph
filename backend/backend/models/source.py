import uuid
from datetime import datetime
from sqlalchemy import Column, String, Text, Float, Boolean, DateTime, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.core.database import Base


class Source(Base):
    __tablename__ = "sources"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    research_id = Column(UUID(as_uuid=True), ForeignKey("research_projects.id"), nullable=False)
    source_type = Column(String(50))  # url, pdf, text, search
    original_input = Column(Text)
    title = Column(Text)
    url = Column(String(2000))
    file_path = Column(String(500))
    raw_text = Column(Text)
    credibility_score = Column(Float)
    processed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    research = relationship("ResearchProject", back_populates="sources")
    chunks = relationship("Chunk", back_populates="source", cascade="all, delete-orphan")


class Chunk(Base):
    __tablename__ = "chunks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    source_id = Column(UUID(as_uuid=True), ForeignKey("sources.id"), nullable=False)
    chunk_index = Column(Integer)
    text = Column(Text, nullable=False)
    section_title = Column(String(500))
    embedding_id = Column(String(100))
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    source = relationship("Source", back_populates="chunks")
    claims = relationship("Claim", back_populates="chunk", cascade="all, delete-orphan")