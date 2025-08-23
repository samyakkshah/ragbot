from pydantic import BaseModel, UUID4, EmailStr
from datetime import datetime
from typing import Optional


class UserOut(BaseModel):
    """Sanitized user for frontend or debug"""

    id: UUID4
    email: Optional[EmailStr] = None
    name: Optional[EmailStr] = None
    created_at: datetime

    class Config:
        from_attributes = True
