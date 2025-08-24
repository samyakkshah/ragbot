from typing import Optional
from fastapi import Header
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
        payload = jwt.decode(token, config.JWT_SECRET, algorithms=["HS256"])
        sub = payload.get("sub")
        if not sub:
            return None
        return Auth(UUID(sub))
    except JWTError as e:
        logger.warning("[auth] JWT verification failed", exc=e, basic=True)
        return None
