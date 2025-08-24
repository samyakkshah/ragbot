from typing import List, AsyncIterator
from models import Message
from abc import ABC, abstractmethod


class LLMGenerator(ABC):
    @abstractmethod
    def stream(
        self, context_chunks: List[str], query: str, history: List[Message]
    ) -> AsyncIterator[str]:
        pass
