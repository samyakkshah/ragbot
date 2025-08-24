from typing import AsyncIterator, Callable, Awaitable, List
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from schemas.message import MessageCreate
from services.chat import add_message, get_messages
from services.rag_pipeline import RAGPipeline
from models import Message as MessageModel
from local_logs.logger import logger

DisconnectProbe = Callable[[], Awaitable[bool]]


class RAGService:
    """
    Orchestrates the RAG flow: persist user msg, fetch history, stream LLM,
    and persist assistant reply. Keeps routers thin.
    """

    def __init__(self, pipeline: RAGPipeline):
        self._pipeline = pipeline

    async def stream(
        self,
        db: AsyncSession,
        *,
        session_id,
        user_text: str,
        is_disconnected: DisconnectProbe | None = None,
    ) -> AsyncIterator[str]:
        """Stream an assistant response for the given user input.

        Persists the user message, obtains recent history, then streams the
        response from the underlying RAG pipeline. On completion or early
        termination, the concatenated assistant content is persisted.

        Args:
            db (AsyncSession): Active database session.
            session_id (UUID): Identifier of the chat session.
            user_text (str): The raw user query text.
            is_disconnected (Callable[[], Awaitable[bool]] | None): Probe that
                returns True if the client has disconnected during streaming.

        Yields:
            str: Assistant response chunks as they are generated.

        Raises:
            RuntimeError: If pipeline or persistence fails unexpectedly.
        """
        # Persist user message (best effort)
        try:
            await add_message(
                db, session_id, MessageCreate(role="user", content=user_text)
            )
        except Exception as e:
            logger.error("[RAGService] Failed to persist user message", exc=e)

        buffer = ""
        try:
            # History excluding the just‑persisted user message
            history: List[MessageModel] = list(await get_messages(db, session_id))[:-1]

            async for chunk in self._pipeline.stream(user_text, history):
                if is_disconnected:
                    try:
                        if await is_disconnected():
                            logger.warning(
                                "[RAGService] Client disconnected; stopping stream"
                            )
                            break
                    except Exception:
                        pass
                buffer += chunk
                yield chunk
        except Exception as e:
            logger.error("[RAGService] Stream failed", exc=e)
            from services.rag_pipeline import RAGPipeline as _RP

            # Surface a single fallback chunk
            fallback = _RP.FALLBACK_MESSAGE
            buffer = buffer or fallback
            yield fallback
        finally:
            if buffer:
                try:
                    await add_message(
                        db, session_id, MessageCreate(role="finbot", content=buffer)
                    )
                except Exception as e:
                    logger.error(
                        "[RAGService] Failed to persist assistant message", exc=e
                    )
