from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Header
from services.container import get_supabase_client
from services.user import get_or_create_user
from jose import jwt, JWTError
from uuid import UUID
from config import config
from local_logs.logger import logger


class Auth:
    """Authenticated identity if present; otherwise None."""

    def __init__(self, user_id: UUID):
        self.user_id = user_id


async def get_auth_optional(
    authorization: Optional[str] = Header(None),
) -> Optional[Auth]:
    """
    Resolve identity from 'Authorization: Bearer <jwt>'.
    :param authorization: Optional bearer token header
    :return: Identity(user_id) or None if anonymous/invalid
    """
    if not authorization or not authorization.lower().startswith("bearer "):
        return None
    token = authorization.split(" ", 1)[1].strip()
    try:
        supabase = get_supabase_client()
        res = supabase.auth.get_user(token)
        if not res or not res.user or not res.user.id:
            return None
        return Auth(UUID(res.user.id))
    except JWTError as e:
        logger.warning("[auth] JWT verification failed", exc=e, basic=True)
        return None


async def signup_user(email: str, password: str):
    """
    Sign Up User with Email and Password

    Args:
        email: User Email
        password: User Password
    """
    supabase = get_supabase_client()
    return supabase.auth.sign_up({"email": email, "password": password})


async def login_user(email: str, password: str):
    """
    Sign Up User with Email and Password

    Args:
        email: User Email
        password: User Password
    """
    supabase = get_supabase_client()
    return supabase.auth.sign_in_with_password({"email": email, "password": password})


async def logout_user(access_token: str):
    """
    Logout User

    Invalidate JWT session
    """
    supabase = get_supabase_client()
    return supabase.auth.sign_out()


async def link_user_and_session(
    db: AsyncSession, user_id: str, cookie_session_id: Optional[str] = None
):
    """
    Ensure user exists in DB and create/resume a session.
    """
    from services.sessions import create_or_resolve_session

    user = await get_or_create_user(db, UUID(user_id))
    session, _ = await create_or_resolve_session(
        db=db, auth=Auth(UUID(user_id)), cookie_session_id=cookie_session_id
    )
    return user, session
