from typing import List
from abc import ABC, abstractmethod


class VectorStore(ABC):
    @abstractmethod
    async def get_relevant_chunks(self, query: str, top_k: int) -> List[str]:
        pass

    @abstractmethod
    async def health_check(self) -> bool:
        pass
