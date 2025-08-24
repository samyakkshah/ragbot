# interfaces/embedder.py
from abc import ABC, abstractmethod
from typing import List


class Embedder(ABC):
    """
    Abstract base class for embedding providers.
    Implementations must convert text to a vector (list of floats).
    """

    @abstractmethod
    async def embed(self, text: str) -> List[float]:
        """
        Generate an embedding vector for the given text.

        :param text: Input text to embed.
        :return: Embedding vector as list of floats.
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def dimension(self) -> int:
        """
        Return the dimensionality of the embeddings produced by this embedder.
        """
        raise NotImplementedError
