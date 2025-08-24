from pydantic import BaseModel, UUID4, Field
from typing import Literal
from datetime import datetime


class IntroMessage(BaseModel):
    role: Literal["finbot"] = "finbot"
    content: str


class MessageCreate(BaseModel):
    """Incoming message payload from the user or finbot."""

    role: Literal["user", "finbot"] = Field(..., description="Message author role")
    content: str = Field(
        ..., min_length=1, max_length=10000, description="Raw text message"
    )


class MessageResponse(BaseModel):
    """Message returned from the server with metadata."""

    id: UUID4
    session_id: UUID4
    role: str
    content: str
    created_at: datetime

    class Config:
        from_attributes = True
