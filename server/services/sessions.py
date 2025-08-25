from typing import Optional
from uuid import uuid4, UUID
from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, Response
from models import Session
from schemas.message import IntroMessage, MessageCreate
from services.chat import add_message

from config import config
from local_logs.logger import logger


INTRO_MESSAGE = (
    f"Hi! I'm your assistant for {config.COMPANY_NAME}. "
    "What can I help you with today?"
)


async def create_session(db: AsyncSession) -> Session:
    """
    Create a new anonymous chat session and seed a persisted intro message.

    Args:
        db: Active async DB session.
    Returns:
        Newly created Session ORM object.
    Raises:
        HTTPException: 500 on failure.
    """
    try:
        session = Session(id=uuid4(), user_id=None)
        db.add(session)
        await db.commit()
        await db.refresh(session)
        logger.info(f"[service:session] Created new session {session.id}")
        return session
    except Exception as e:
        logger.error(
            "[service:session] Failed to create session", exc=e, once=config.DEBUG
        )
        await db.rollback()
        raise HTTPException(status_code=500, detail="Unable to create session")


async def get_latest_session_for_user(
    db: AsyncSession, user_id: UUID
) -> Optional[Session]:
    q = (
        select(Session)
        .where(Session.user_id == user_id)
        .order_by(desc(Session.created_at))
        .limit(1)
    )
    r = await db.execute(q)
    return r.scalar_one_or_none()


async def create_or_resume_user_session(
    db: AsyncSession, user_id: UUID | None = None
) -> Session:
    """
    Creates a new session or resumes existing session for a user.

    Args:
        db: Database session
        user_id: Optional user ID. If None, creates anonymous session
    Returns:
        Session: New or existing session
    """
    try:
        if user_id:
            existing = await get_latest_session_for_user(db, user_id)
            if existing:
                logger.info(
                    f"[service:session] Resumed session {existing.id} for user {user_id}"
                )
                return existing

            session = Session(id=uuid4(), user_id=user_id)
            db.add(session)
            await db.commit()
            await db.refresh(session)
            logger.info(
                f"[service:session] Created new session {session.id} for user {user_id}"
            )
            return session

        return await create_session(db)

    except Exception as e:
        logger.error(
            "[service:session] Failed to create/resume session",
            exc=e,
            once=config.DEBUG,
        )
        await db.rollback()
        raise HTTPException(
            status_code=500, detail="Unable to create or resume session"
        )


async def get_session(db: AsyncSession, session_id: UUID) -> Session:
    session = await db.get(Session, session_id)
    if not session:
        logger.warning(f"[service:session] Session {session_id} not found in DB")
        raise HTTPException(status_code=404, detail="Session not found")
    return session


async def create_intro_message(session: AsyncSession, session_id: UUID) -> IntroMessage:
    """
    Fetch a session by id.

    Args:
        db: Active async DB session.
        session_id: Target session UUID.

    Returns:
        Session ORM object.
    Raises:
        HTTPException: 404 if not found.
    TODO: Replace with actual intro creation
    """
    try:
        message = MessageCreate(role="finbot", content=INTRO_MESSAGE)
        await add_message(session, session_id, message)
        return IntroMessage(content=INTRO_MESSAGE)
    except Exception as e:
        logger.error(
            f"[service:intro_message] Failed to generate Intro message for session {session_id}",
            once=config.DEBUG,
        )
        await session.rollback()
        raise HTTPException(status_code=500, detail="Could not generate Intro message")


def set_cookie(cookie: str, response: Response):
    try:
        response.set_cookie(
            key=config.SESSION_COOKIE_NAME,
            value=cookie,
            httponly=True,
            secure=config.HTTPS,  # set to True if HTTPS
            samesite="lax",
            max_age=60 * 60 * 24 * 30,  # 30 days
        )
    except Exception as e:
        logger.error("[cookie] Failed to Set cookie", exc=e, once=config.DEBUG)
        raise e
    return {f"{config.SESSION_COOKIE_NAME}": cookie, "anonymous": True}
