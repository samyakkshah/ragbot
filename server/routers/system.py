from fastapi import APIRouter, Request, Response
from services.sessions import set_cookie
from db_manager import db_manager
from config import config
from services.container import get_vector_store
from uuid import uuid4

router = APIRouter()


@router.get("/health")
async def health():

    pg_ok = await db_manager.test_postgres()
    pc_ok = await get_vector_store().health_check()
    return {"status": "ok", "postgres": pg_ok, "pinecone": pc_ok}


@router.get("/me")
def me(request: Request, response: Response):
    cookie = request.cookies.get(config.SESSION_COOKIE_NAME)
    if not cookie:
        cookie = str(uuid4())
    return set_cookie(cookie, response)
