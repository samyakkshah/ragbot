from fastapi import APIRouter, Request, Response
from uuid import uuid4
from db_manager import db_manager
from config import config
from services.container import get_vector_store

router = APIRouter()
SESSION_COOKIE_NAME = "sid"


@router.get("/health")
async def health():

    pg_ok = await db_manager.test_postgres()
    pc_ok = await get_vector_store().health_check()
    return {"status": "ok", "postgres": pg_ok, "pinecone": pc_ok}


@router.get("/me")
def me(request: Request, response: Response):
    sid = request.cookies.get(SESSION_COOKIE_NAME)
    if not sid:
        sid = str(uuid4())
        response.set_cookie(
            key=SESSION_COOKIE_NAME,
            value=sid,
            httponly=True,
            secure=config.HTTPS,  # set to True if HTTPS
            samesite="lax",
            max_age=60 * 60 * 24 * 30,  # 30 days
            path="/",
        )
    return {"sid": sid, "anonymous": True}
