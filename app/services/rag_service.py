"""Main RAG service that coordinates document processing and retrieval."""
from __future__ import annotations
import uuid
import asyncio
from typing import BinaryIO, Dict, Any, List
from datetime import datetime

from app.models.document import Document, DocumentStatus
from app.rag.loaders.factory import get_loader_factory
from app.rag.chunking.strategies import ChunkingFactory
from app.rag.embeddings.service import get_embedding_service
from app.rag.vectorstore.factory import get_vector_store
from app.rag.retrieval.service import get_retrieval_service
from app.schemas.rag import (
    DocumentUploadResponse, 
    DocumentIndexResponse,
    DocumentSearchResponse,
    DocumentListResponse,
    DocumentDeleteResponse
)


class RAGService:
    """Main RAG service for document management and retrieval."""
    
    def __init__(self):
        """Initialize RAG service with all components."""
        self.loader_factory = get_loader_factory()
        self.embedding_service = get_embedding_service()
        self.vector_store = get_vector_store()
        self.retrieval_service = get_retrieval_service()
        
        # In-memory document storage (in production, use a database)
        self._documents: Dict[str, Document] = {}
    
    async def upload_document(
        self,
        file_content: BinaryIO,
        filename: str,
        tags: List[str] = None,
        custom_metadata: Dict[str, Any] = None
    ) -> DocumentUploadResponse:
        """Upload and store a document.
        
        Args:
            file_content: File content as binary IO
            filename: Name of the file
            tags: Optional tags for the document
            custom_metadata: Optional custom metadata
            
        Returns:
            Upload response with document ID and status
        """
        try:
            # Load document using appropriate loader
            document = await self.loader_factory.load_document(
                file_content=file_content,
                filename=filename,
                metadata={
                    "tags": tags or [],
                    **(custom_metadata or {})
                }
            )
            
            # Store document
            self._documents[document.id] = document
            
            return DocumentUploadResponse(
                document_id=document.id,
                filename=filename,
                status=document.status,
                message="Document uploaded successfully"
            )
            
        except Exception as e:
            return DocumentUploadResponse(
                document_id="",
                filename=filename,
                status=DocumentStatus.FAILED,
                message=f"Failed to upload document: {str(e)}"
            )
    
    async def index_document(
        self,
        document_id: str,
        chunk_size: int = 1000,
        chunk_overlap: int = 200,
        chunking_strategy: str = "recursive",
        force_reindex: bool = False
    ) -> DocumentIndexResponse:
        """Index a document for search.
        
        Args:
            document_id: ID of the document to index
            chunk_size: Size of text chunks
            chunk_overlap: Overlap between chunks
            chunking_strategy: Strategy for chunking ("fixed_size", "sentence", "recursive")
            force_reindex: Whether to force re-indexing if already indexed
            
        Returns:
            Indexing response with status and chunk count
        """
        start_time = datetime.utcnow()
        
        try:
            # Get document
            document = self._documents.get(document_id)
            if not document:
                return DocumentIndexResponse(
                    document_id=document_id,
                    chunks_created=0,
                    status=DocumentStatus.FAILED,
                    processing_time_seconds=0
                )
            
            # Check if already indexed
            if document.status == DocumentStatus.INDEXED and not force_reindex:
                return DocumentIndexResponse(
                    document_id=document_id,
                    chunks_created=len(document.chunks),
                    status=DocumentStatus.INDEXED,
                    processing_time_seconds=0
                )
            
            # Update status
            document.status = DocumentStatus.PROCESSING
            
            # Create chunking strategy
            chunker = ChunkingFactory.create_strategy(
                strategy_type=chunking_strategy,
                chunk_size=chunk_size,
                chunk_overlap=chunk_overlap
            )
            
            # Chunk the document
            chunks = chunker.chunk_text(
                text=document.content,
                document_id=document_id,
                metadata=document.metadata.custom_metadata
            )
            
            # Generate embeddings for chunks
            chunk_texts = [chunk.content for chunk in chunks]
            embeddings = await self.embedding_service.embed_batch(chunk_texts)
            
            # Add embeddings to chunks
            for chunk, embedding in zip(chunks, embeddings):
                chunk.embedding = embedding
            
            # Store chunks in vector store
            await self.vector_store.add_chunks(chunks)
            
            # Update document
            document.chunks = chunks
            document.status = DocumentStatus.INDEXED
            document.metadata.processed_at = datetime.utcnow()
            
            processing_time = (datetime.utcnow() - start_time).total_seconds()
            
            return DocumentIndexResponse(
                document_id=document_id,
                chunks_created=len(chunks),
                status=DocumentStatus.INDEXED,
                processing_time_seconds=processing_time
            )
            
        except Exception as e:
            # Update document status on failure
            if document_id in self._documents:
                self._documents[document_id].status = DocumentStatus.FAILED
            
            processing_time = (datetime.utcnow() - start_time).total_seconds()
            
            return DocumentIndexResponse(
                document_id=document_id,
                chunks_created=0,
                status=DocumentStatus.FAILED,
                processing_time_seconds=processing_time
            )
    
    async def search_documents(
        self,
        query: str,
        max_results: int = 5,
        min_score: float = 0.3,
        filter_metadata: Dict[str, Any] = None
    ) -> DocumentSearchResponse:
        """Search for relevant documents.
        
        Args:
            query: Search query
            max_results: Maximum number of results
            min_score: Minimum relevance score
            filter_metadata: Optional metadata filters
            
        Returns:
            Search response with results
        """
        start_time = datetime.utcnow()
        
        try:
            results = await self.retrieval_service.search(
                query=query,
                max_results=max_results,
                min_score=min_score,
                filter_metadata=filter_metadata
            )
            
            search_time = (datetime.utcnow() - start_time).total_seconds()
            
            return DocumentSearchResponse(
                query=query,
                results=results,
                total_results=len(results),
                search_time_seconds=search_time
            )
            
        except Exception as e:
            search_time = (datetime.utcnow() - start_time).total_seconds()
            
            return DocumentSearchResponse(
                query=query,
                results=[],
                total_results=0,
                search_time_seconds=search_time
            )
    
    async def list_documents(
        self,
        page: int = 1,
        page_size: int = 20
    ) -> DocumentListResponse:
        """List all documents with pagination.
        
        Args:
            page: Page number (1-based)
            page_size: Number of documents per page
            
        Returns:
            List of documents with pagination info
        """
        documents = list(self._documents.values())
        total_count = len(documents)
        
        # Calculate pagination
        start_idx = (page - 1) * page_size
        end_idx = start_idx + page_size
        page_documents = documents[start_idx:end_idx]
        
        # Convert to dict representation
        doc_dicts = []
        for doc in page_documents:
            doc_dict = {
                "id": doc.id,
                "filename": doc.metadata.filename,
                "status": doc.status,
                "uploaded_at": doc.metadata.uploaded_at.isoformat(),
                "processed_at": doc.metadata.processed_at.isoformat() if doc.metadata.processed_at else None,
                "file_size": doc.metadata.file_size,
                "content_type": doc.metadata.content_type,
                "tags": doc.metadata.tags,
                "chunk_count": len(doc.chunks)
            }
            doc_dicts.append(doc_dict)
        
        return DocumentListResponse(
            documents=doc_dicts,
            total_count=total_count,
            page=page,
            page_size=page_size
        )
    
    async def delete_document(self, document_id: str) -> DocumentDeleteResponse:
        """Delete a document and its chunks.
        
        Args:
            document_id: ID of the document to delete
            
        Returns:
            Deletion response
        """
        try:
            # Check if document exists
            if document_id not in self._documents:
                return DocumentDeleteResponse(
                    document_id=document_id,
                    deleted=False,
                    message="Document not found"
                )
            
            # Delete from vector store
            await self.vector_store.delete_document(document_id)
            
            # Delete from memory storage
            del self._documents[document_id]
            
            return DocumentDeleteResponse(
                document_id=document_id,
                deleted=True,
                message="Document deleted successfully"
            )
            
        except Exception as e:
            return DocumentDeleteResponse(
                document_id=document_id,
                deleted=False,
                message=f"Failed to delete document: {str(e)}"
            )
    
    async def get_document(self, document_id: str) -> Document:
        """Get a document by ID."""
        return self._documents.get(document_id)
    
    async def get_stats(self) -> Dict[str, Any]:
        """Get RAG service statistics."""
        vector_stats = await self.vector_store.get_stats()
        retrieval_stats = await self.retrieval_service.get_stats()
        
        status_counts = {}
        for doc in self._documents.values():
            status = doc.status.value
            status_counts[status] = status_counts.get(status, 0) + 1
        
        return {
            "total_documents": len(self._documents),
            "documents_by_status": status_counts,
            "supported_file_types": self.loader_factory.get_supported_extensions(),
            "vector_store": vector_stats,
            "retrieval": retrieval_stats
        }


# Global RAG service instance
_rag_service = None


def get_rag_service() -> RAGService:
    """Get the global RAG service instance."""
    global _rag_service
    if _rag_service is None:
        _rag_service = RAGService()
    return _rag_service