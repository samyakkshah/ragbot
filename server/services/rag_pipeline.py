from typing import List, AsyncIterator
from interfaces.vector_store import VectorStore
from interfaces.llm_generator import LLMGenerator
from models import Message

from local_logs.logger import logger


class RAGPipeline:
    """
    Orchestrates retrieval and generation.

    :param vector_store: VectorStore implementation for context retrieval.
    :param llm_generator: LLMGenerator implementation for text generation.
    :param top_k: Max number of chunks to retrieve.
    :param min_query_len: Minimum length for a valid query.
    """

    FALLBACK_MESSAGE: str = (
        "I'm not sure based on the available information. Please contact our support team."
    )

    def __init__(
        self,
        vector_store: VectorStore,
        llm_generator: LLMGenerator,
        *,
        top_k: int = 5,
        min_query_len: int = 1,
    ):
        self._vector_store = vector_store
        self._llm_generator = llm_generator
        self._top_k = top_k
        self._min_query_len = min_query_len

    @staticmethod
    def _is_query_weak(query: str, min_len: int) -> bool:
        """
        Determine whether the query is too weak to produce a useful answer.

        :param query: Raw user query.
        :param min_len: Minimum non-whitespace length allowed.
        :return: True if weak; otherwise False.
        """
        q = (query or "").lower().strip()
        condition = len(q) < min_len and q not in ("no", "yes") and not q.isdigit()
        return condition

    async def _retrieve(self, query: str) -> List[str]:
        """
        Retrieve relevant context snippets for the query.

        :param query: Raw user query.
        :return: List of context chunk strings.
        """
        try:
            chunks = await self._vector_store.get_relevant_chunks(
                query, top_k=self._top_k
            )
            chunks = [c for c in (chunks or []) if isinstance(c, str) and c.strip()]
            return chunks
        except Exception as e:
            logger.error("[RAG] Retrieval failed:", exc=e)
            raise

    async def stream(self, query: str, history: List[Message]) -> AsyncIterator[str]:
        """
        Stream the model answer token-by-token.

        :param query: User query string.
        :yield: Model token fragments as strings.
        """
        try:
            if self._is_query_weak(query, self._min_query_len):
                logger.warning("[RAG] Weak query detected. Sending fallback message.")
                yield self.FALLBACK_MESSAGE
                return

            chunks = await self._retrieve(query)
            if not chunks:
                logger.warning("[RAG] No context found")

            # History injection can be added later; default to empty list for now.
            async for token in self._llm_generator.stream_response(
                chunks, query, history
            ):
                yield token
        except Exception as e:
            logger.error("[RAG] Pipeline streaming error:", exc=e)
            yield self.FALLBACK_MESSAGE
