from fastapi import APIRouter, status, Request, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession

from db_manager import db_manager
from schemas.rag import RAGQuery

from services.container import get_rag_pipeline
from services.rag import RAGService


from config import config
from local_logs.logger import logger

router = APIRouter(prefix="/rag", tags=["RAG"])


def get_rag_service() -> RAGService:
    return RAGService(get_rag_pipeline())


@router.post("/query", status_code=status.HTTP_202_ACCEPTED)
async def rag_stream(
    query: RAGQuery,
    request: Request,
    db: AsyncSession = Depends(db_manager.get_session),
    rag_service: RAGService = Depends(get_rag_service),
):
    """Stream a retrieval-augmented response for the given user query.

    Persists the user message, threads recent chat history into the prompt,
    streams the assistant response chunk-by-chunk, and finally persists the
    full assistant message (best effort) even if the client disconnects.

    Args:
        query (RAGQuery): Pydantic payload containing session_id and message.
        request (Request): FastAPI request (used to detect disconnects).
        db (AsyncSession): Database session provided by dependency.
        svc (RAGService): Orchestrator that encapsulates RAG business logic.

    Returns:
        StreamingResponse: UTF-8 text stream containing assistant chunks.

    Raises:
        HTTPException: 400 on invalid input, 5xx on unexpected errors.
    """

    async def gen():
        async for chunk in rag_service.stream(
            db,
            session_id=query.session_id,
            user_text=query.message,
            is_disconnected=request.is_disconnected,
        ):
            yield chunk

    return StreamingResponse(
        gen(),
        media_type="text/plain; charset=utf-8",
        headers={"Cache-Control": "no-store"},
    )
