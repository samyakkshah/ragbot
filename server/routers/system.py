from typing import Optional
from fastapi import APIRouter, Request, Response, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from services.sessions import set_cookie, create_or_resolve_session
from services.auth import Auth, get_auth_optional
from services.container import get_vector_store

from db_manager import db_manager

from config import config

router = APIRouter()


@router.get("/health")
async def health():

    pg_ok = await db_manager.test_postgres()
    pc_ok = await get_vector_store().health_check()
    return {"status": "ok", "postgres": pg_ok, "pinecone": pc_ok}


# Redundant route - Could be refactored later
# @router.get("/me")
# async def me(
#     request: Request,
#     response: Response,
#     db: AsyncSession = Depends(db_manager.get_session),
#     auth: Optional[Auth] = Depends(get_auth_optional),
# ):
#     cookie = request.cookies.get(config.SESSION_COOKIE_NAME)
#     session, should_set_cookie = await create_or_resolve_session(db, auth, cookie)
#     if should_set_cookie:
#         set_cookie(str(session.id), response)
#     return {"session_id": str(session.id), "anonymous": session.user_id is None}
