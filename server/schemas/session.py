from pydantic import BaseModel, UUID4
from datetime import datetime


class SessionOut(BaseModel):
    """Minimal session info for frontend or audit."""

    id: UUID4
    created_at: datetime

    class Config:
        from_attributes = True
