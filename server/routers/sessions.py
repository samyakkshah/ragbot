from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import uuid4, UUID
from db_manager import db_manager
from models import Session
from schemas.session import SessionOut
from local_logs.logger import logger


router = APIRouter(prefix="/session", tags=["Session"])


@router.post("/", response_model=SessionOut, status_code=status.HTTP_201_CREATED)
async def create_session(
    request: Request, db: AsyncSession = Depends(db_manager.get_session)
):
    """
    Create a new chat session. Tied to user if authenticated, else anonymous.
    """
    try:
        session = Session(
            id=uuid4(), user_id=None  # Replace later when auth is integrated
        )
        db.add(session)
        await db.commit()
        await db.refresh(session)

        logger.info(f"[session] Created new session {session.id}")
        return session
    except Exception as e:
        logger.error(f"[session] Failed to create session: {e}")
        raise HTTPException(status_code=500, detail="Unable to create session")


@router.get("/{session_id}", response_model=SessionOut)
async def get_session_by_id(
    session_id: UUID, db: AsyncSession = Depends(db_manager.get_session)
):
    """
    Get basic metadata for a session.
    """
    session = await db.get(Session, session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return session
