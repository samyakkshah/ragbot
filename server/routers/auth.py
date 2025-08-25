from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from config import config
from schemas.auth import AuthRequest
from sqlalchemy.ext.asyncio import AsyncSession

from db_manager import db_manager
from services import auth as auth_service
from services.sessions import set_cookie

from local_logs.logger import logger

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/signup")
async def signup(
    payload: AuthRequest,
    response: Response,
):

    if not payload.email or not payload.password:
        raise HTTPException(status_code=400, detail="Email and Passowrd are required")
    try:
        resp = await auth_service.signup_user(payload.email, payload.password)
        if not resp.user:
            raise HTTPException(status_code=400, detail="Signup failed")
        return {"message": "Signup successful. Please check your email to verify."}
    except Exception as e:
        logger.error("Issue while signing up", exc=e, once=config.DEBUG)
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/login")
async def login(
    payload: AuthRequest,
    request: Request,
    response: Response,
    db: AsyncSession = Depends(db_manager.get_session),
):
    try:
        resp = await auth_service.login_user(payload.email, payload.password)
        if not resp.user:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        cookie_session_id = request.cookies.get(config.SESSION_COOKIE_NAME)
        user_id = resp.user.id
        user, session = await auth_service.link_user_and_session(
            db, user_id, cookie_session_id
        )
        set_cookie(str(session.id), response)
        if not resp.session:
            raise HTTPException(
                status_code=500, detail="Unkown issue occured during login"
            )
        return {
            "jwt_user_token": resp.session.access_token,
            "session_id": str(session.id),
            "user_id": str(user.id),
        }
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))


@router.post("/logout")
async def logout(response: Response):
    try:
        await auth_service.logout_user("token-not-needed")
        response.delete_cookie(config.SESSION_COOKIE_NAME)
        return {"success": True}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
