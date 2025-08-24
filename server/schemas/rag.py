from pydantic import BaseModel, UUID4, Field
from datetime import datetime


class RAGQuery(BaseModel):
    """User RAG message request"""

    session_id: UUID4 = Field(..., description="Active chat session")
    message: str = Field(..., min_length=1, max_length=10000, description="User input")


class RAGResponse(BaseModel):
    """RAG response message"""

    session_id: UUID4
    user_message: str
    bot_message: str
    message_id: UUID4
    created_at: datetime
