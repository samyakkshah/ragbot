from fastapi import APIRouter, Depends, status, Request
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from db_manager import db_manager
from schemas.message import IntroMessage
from schemas.session import SessionOut

from services.auth import Auth, get_auth_optional
from services.sessions import (
    create_or_resume_user_session,
    get_session as svc_get_session,
    create_intro_message,
)
from services.user import get_or_create_user


router = APIRouter(prefix="/session", tags=["Session"])


@router.post("/", response_model=SessionOut, status_code=status.HTTP_201_CREATED)
async def create_or_resume_session(
    request: Request,
    db: AsyncSession = Depends(db_manager.get_session),
    auth: Auth | None = Depends(get_auth_optional),
):
    """
    Create a new session (anonymous) or return the existing one if user is authenticated.
    """
    if auth:
        user = await get_or_create_user(db, auth.user_id)
        return await create_or_resume_user_session(db, user.id._value)
    sid = request.cookies.get("sid")
    if sid:
        try:
            return await svc_get_session(db, UUID(sid))
        except Exception:
            pass
    return await create_or_resume_user_session(db)


@router.get("/{session_id}", response_model=SessionOut)
async def get_session_by_id(
    session_id: UUID, db: AsyncSession = Depends(db_manager.get_session)
):
    """
    Persist a new message in a session.

    Args:
        session_id (UUID): Chat session UUID.
        db (Session): Get session.

    Returns:
        Session

    Raises:
        HTTPException: 500 on failure to get.
    """
    return await svc_get_session(db, session_id)


@router.get("/{session_id}/intro", response_model=IntroMessage)
async def get_intro_message(
    session_id: UUID, db: AsyncSession = Depends(db_manager.get_session)
):
    """
    Get basic intro message
    """
    return await create_intro_message(db, session_id)
