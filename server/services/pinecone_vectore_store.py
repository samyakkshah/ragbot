from typing import List, Optional
from openai import AsyncOpenAI
from pinecone import Pinecone
from config import config
from local_logs.logger import logger
from interfaces.vector_store import VectorStore
from interfaces.embedder import Embedder


class PineconeVectorStore(VectorStore):
    """
    VectorStore backed by Pinecone.

    :param namespace: Pinecone namespace used for queries (default: "default").
    """

    def __init__(self, embedder: Embedder, *, namespace: Optional[str] = None):
        try:
            if not config.PINECONE_API_KEY:
                raise ValueError("PINECONE_API_KEY is not configured.")
            if not config.PINECONE_INDEX_HOST:
                raise ValueError("PINECONE_INDEX_NAME is not configured.")

            self._pc = Pinecone(api_key=config.PINECONE_API_KEY)
            self._index = self._pc.Index(host=config.PINECONE_INDEX_HOST)
            self._embedder = embedder
            self._namespace = namespace if namespace is not None else ""
        except Exception as e:
            logger.error("[PineconeVectorStore] Initialization failed:", exc=e)
            raise

    async def get_relevant_chunks(self, query: str, top_k: int = 5) -> List[str]:
        """
        Retrieve the top_k most relevant text chunks from Pinecone.

        :param query: User query string.
        :param top_k: Number of matches to return.
        :return: List of text chunks (may be empty on failure).
        """
        try:
            if not (query or "").strip():
                logger.warning("[PineconeVectorStore] Empty query provided")
                return []

            vector = await self._embedder.embed(query)
            if not vector:
                logger.warning("[PineconeVectorStore] Empty embedding; skipping query.")
                return []

            query_result = self._index.query(
                vector=vector,
                top_k=top_k,
                namespace=self._namespace,
                include_metadata=True,
            )

            matches = getattr(query_result, "matches", None)
            if matches is None and isinstance(query_result, dict):
                matches = query_result.get(
                    "matches", []  # pyright: ignore[reportCallIssue]
                )

            chunks: List[str] = []
            for match in matches or []:
                metadata = (
                    match.get("metadata")
                    if isinstance(match, dict)
                    else getattr(match, "metadata", {})
                )
                text = (
                    metadata.get("text")
                    if isinstance(metadata, dict)
                    else getattr(metadata, "text", None)
                )
                if text:
                    chunks.append(text)

            logger.info(
                f"[PineconeVectorStore] Retrieved {len(chunks)} chunk(s) for query."
            )
            return chunks
        except Exception as e:
            logger.error(
                "[PineconeVectorStore] Context retrieval failed:",
                exc=e,
                once=config.DEBUG,
            )
            raise

    async def health_check(self) -> bool:
        """
        Basic connectivity health check.

        :return: True if describe_index_stats succeeds; False otherwise.
        """
        try:
            stats = self._index.describe_index_stats()
            logger.info(f"[PineconeVectorStore] Health stats: {stats}")
            return True
        except Exception as e:
            logger.error(
                "[PineconeVectorStore] Health check failed:", exc=e, once=config.DEBUG
            )
            return False
