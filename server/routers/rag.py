from fastapi import APIRouter, status, Request, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession

from db_manager import db_manager
from schemas.rag import RAGQuery
from schemas.message import MessageCreate

from services.open_ai_embedder import OpenAIEmbedder
from services.pinecone_vectore_store import PineconeVectorStore
from services.open_ai_llm_generator import OpenAIChatGenerator
from services.rag_pipeline import RAGPipeline
from services.chat import add_message


from config import config
from local_logs.logger import logger

router = APIRouter(prefix="/rag", tags=["RAG"])

_embedder = OpenAIEmbedder()
_vector_store = PineconeVectorStore(embedder=_embedder, namespace="")
_llm_generator = OpenAIChatGenerator()
_rag_pipeline = RAGPipeline(_vector_store, _llm_generator, top_k=5)


@router.post("/query", status_code=status.HTTP_202_ACCEPTED)
async def rag_stream(
    query: RAGQuery,
    request: Request,
    db: AsyncSession = Depends(db_manager.get_session),
):
    """
    Stream a Retrieval‑Augmented Generation (RAG) response for the given query.

    :param query: RAGQuery containing session_id and user message.
    :param request: FastAPI Request (used to detect client disconnects).
    :param db: Async database session.
    :raises HTTPException: 500 on unrecoverable errors.
    :return: StreamingResponse yielding model tokens as plain text.
    """
    # Best‑effort: persist user message first
    try:
        await add_message(
            db, query.session_id, MessageCreate(role="user", content=query.message)
        )
    except Exception as e:
        logger.error(
            "[rag.stream] Failed to persist user message:", exc=e, once=config.DEBUG
        )

    async def token_generator():
        buffer = ""
        try:
            async for chunk in _rag_pipeline.stream(query.message):
                # Early client disconnect check (best‑effort)
                try:
                    if await request.is_disconnected():
                        logger.warning(
                            "[rag.stream] Client disconnected; stopping stream"
                        )
                        break
                except Exception:
                    pass

                buffer += chunk
                yield chunk
        except Exception as stream_error:
            logger.error(
                f"[rag.stream] Streaming failed: {stream_error}", exc=stream_error
            )
            # Surface a minimal message to client and still try to persist
            yield RAGPipeline.FALLBACK_MESSAGE
        finally:
            if buffer:
                try:
                    await add_message(
                        db,
                        query.session_id,
                        MessageCreate(role="finbot", content=buffer),
                    )
                except Exception as db_error:
                    logger.error(
                        f"[rag.stream] Failed to save finbot response: {db_error}",
                        exc=db_error,
                    )

    return StreamingResponse(token_generator(), media_type="text/plain; charset=utf-8")


@router.get("/health", status_code=status.HTTP_200_OK)
async def get_health():
    pc_ok = await _vector_store.health_check()
    return {"status": "ok", "postgres": pc_ok}
