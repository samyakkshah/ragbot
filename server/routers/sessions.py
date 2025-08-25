from typing import Optional
from fastapi import APIRouter, Depends, status, Request, Response
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from db_manager import db_manager
from schemas.message import IntroMessage
from schemas.session import SessionOut

from services.auth import Auth, get_auth_optional
from services.sessions import (
    get_session as svc_get_session,
    create_intro_message,
    set_cookie,
    create_or_resolve_session,
)

from config import config

router = APIRouter(prefix="/session", tags=["Session"])


@router.post("/", response_model=SessionOut, status_code=status.HTTP_201_CREATED)
async def create_or_resume_session(
    request: Request,
    response: Response,
    db: AsyncSession = Depends(db_manager.get_session),
    auth: Optional[Auth] = Depends(get_auth_optional),
):
    """
    Create a new session (anonymous) or return the existing one if user is authenticated, or already cookie is set.
    """
    cookie = request.cookies.get(config.SESSION_COOKIE_NAME)
    session, should_set_cookie = await create_or_resolve_session(db, auth, cookie)
    if should_set_cookie:
        set_cookie(str(session.id), response)
    return session


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
