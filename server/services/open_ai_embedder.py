# services/openai_embedder.py
from typing import List
from openai import AsyncOpenAI
from config import config
from local_logs.logger import logger
from interfaces.embedder import Embedder


class OpenAIEmbedder(Embedder):
    """
    OpenAI embeddings provider.
    """

    def __init__(self) -> None:
        if not config.OPEN_AI_API_KEY:
            raise ValueError("OPEN_AI_API_KEY is not configured.")
        if not config.EMBED_MODEL:
            raise ValueError("EMBED_MODEL is not configured.")

        self._client = AsyncOpenAI(api_key=config.OPEN_AI_API_KEY)
        self._model = config.EMBED_MODEL
        self._dimension = config.EMBED_DIM

    @property
    def dimension(self) -> int:
        return self._dimension

    async def embed(self, text: str) -> List[float]:
        stripped_text = (text or "").strip()
        if not stripped_text:
            raise ValueError("No text to embed")

        try:
            resp = await self._client.embeddings.create(
                model=self._model,
                input=stripped_text,
                dimensions=self._dimension,
            )
            return resp.data[0].embedding
        except Exception as e:
            logger.error("[OpenAIEmbedder] Embedding failed", exc=e)
            raise e
