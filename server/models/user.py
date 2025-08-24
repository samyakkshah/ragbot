import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from .base import Base


class User(Base):
    """Represents an application user. Can be anonymous or registered."""

    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))

    sessions = relationship(
        "Session", back_populates="user", cascade="all, delete-orphan"
    )
