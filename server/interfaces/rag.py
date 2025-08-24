from typing import AsyncIterator, Protocol
from models import Message


class RAG(Protocol):
    """Abstract RAG contract."""

    async def stream(self, query: str, history: list[Message]) -> AsyncIterator[str]:
        """Stream generated response tokens given a query and conversation history."""
        ...
