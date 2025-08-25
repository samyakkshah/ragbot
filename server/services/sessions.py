from typing import Optional, Tuple
from uuid import uuid4, UUID
from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, Response
from models import Session
from schemas.message import IntroMessage, MessageCreate
from services.chat import add_message
from services.user import get_or_create_user
from services.auth import Auth
from config import config
from local_logs.logger import logger


INTRO_MESSAGE = (
    f"Hi! I'm your assistant for {config.COMPANY_NAME}. "
    "What can I help you with today?"
)


async def create_session(db: AsyncSession, user_id: Optional[UUID] = None) -> Session:
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
        session = Session(id=uuid4(), user_id=user_id)
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
    return {f"{config.SESSION_COOKIE_NAME}": cookie, "authenticated": False}


async def create_or_resolve_session(
    db: AsyncSession, auth: Optional[Auth], cookie_session_id: Optional[str]
) -> Tuple[Session, bool]:
    """
    Single Source of truth to resolve a session based for the current request.

    Workflow:
    - If JWT present -> ensure User exists -> get latest session for user with user id or return session of cookie
    - Else, if cookie is present, and cookie session id exists -> return that session
    - Else, create new anonymous session

    Returns:
        (session, should_set_cookie)
        - should_set_cookie = True when we created a new session or when no valid cookie existed
    """

    if auth is not None and getattr(auth, "user_id", None):
        user = await get_or_create_user(db, auth.user_id)
        if cookie_session_id:
            try:
                cookie_sess = await get_session(db, UUID(cookie_session_id))
                if cookie_sess.user_id is None:
                    cookie_sess.user_id = user.id
                    await db.commit()
                    await db.refresh(cookie_sess)
                    return cookie_sess, False
            except Exception:
                logger.warning("Could not set user id")
                pass
        existing = await get_latest_session_for_user(db, user.id)  # type: ignore
        if existing:
            logger.info(
                f"[service:session] Resumed session {existing.id} for user {user.id}"
            )
            return existing, False
        session = await create_session(db, user.id)  # type: ignore
        return session, True

    if cookie_session_id:
        try:
            session = await get_session(db, UUID(cookie_session_id))
            return session, False
        except Exception:
            pass

    session = await create_session(db, None)
    return session, True
