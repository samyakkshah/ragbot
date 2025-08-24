from typing import List
from openai import AsyncOpenAI
from config import config
from local_logs.logger import logger

_client = AsyncOpenAI(api_key=config.OPEN_AI_API_KEY)
MAX_INPUT_CHARS: int = 8000


async def get_query_embedding(text: str) -> List[float]:
    """
    Generates an embedding vector for user query

    Args:
        text: The query text to embed

    Returns:
        A list of floats representing the embedding vector
    """

    if not text.strip():
        raise ValueError("text must be a non empty string")

    if not config.EMBED_MODEL:
        raise ValueError("Embedding Model is not configured")

    payload = text.strip()

    if len(payload) > MAX_INPUT_CHARS:
        logger.warning(
            f"[services:embedding] Query text length {len(payload)} exceeds {MAX_INPUT_CHARS} chars; truncating."
        )
        payload = payload[:MAX_INPUT_CHARS]

    try:
        resp = await _client.embeddings.create(model=config.EMBED_MODEL, input=payload)
        vec = resp.data[0].embedding

        if not isinstance(vec, list) or not vec:
            raise RuntimeError("Received empty or invalid embedding vector")

        return vec

    except Exception as e:
        logger.error("[services:embedding] Failed to generate embedding", exc=e)
        raise
