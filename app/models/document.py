"""Document models for RAG system."""
from __future__ import annotations
from datetime import datetime
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from enum import Enum


class DocumentStatus(str, Enum):
    """Document processing status."""
    PENDING = "pending"
    PROCESSING = "processing"
    INDEXED = "indexed"
    FAILED = "failed"


class DocumentMetadata(BaseModel):
    """Document metadata."""
    filename: str
    file_size: int
    content_type: str
    uploaded_at: datetime
    processed_at: Optional[datetime] = None
    source_path: Optional[str] = None
    tags: List[str] = Field(default_factory=list)
    custom_metadata: Dict[str, Any] = Field(default_factory=dict)


class Document(BaseModel):
    """Document model."""
    id: str
    content: str
    metadata: DocumentMetadata
    status: DocumentStatus = DocumentStatus.PENDING
    chunks: List["DocumentChunk"] = Field(default_factory=list)
    
    class Config:
        from_attributes = True


class DocumentChunk(BaseModel):
    """Document chunk model for text splitting."""
    id: str
    document_id: str
    content: str
    chunk_index: int
    start_char: int
    end_char: int
    token_count: Optional[int] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)
    embedding: Optional[List[float]] = None
    
    class Config:
        from_attributes = True


class QueryEmbedding(BaseModel):
    """Query embedding model."""
    query: str
    embedding: List[float]
    created_at: datetime = Field(default_factory=datetime.utcnow)


class SearchResult(BaseModel):
    """Search result from vector store."""
    chunk_id: str
    document_id: str
    content: str
    score: float
    metadata: Dict[str, Any] = Field(default_factory=dict)


# Forward reference resolution
Document.model_rebuild()