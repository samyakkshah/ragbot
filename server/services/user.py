from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from uuid import UUID
from models import User
from local_logs.logger import logger


async def get_or_create_user(db: AsyncSession, user_id: UUID) -> User:
    """
    Ensure a User row exists with this id.
    :param db: DB session
    :param user_id: External/user auth id (UUID)
    :return: User row
    """
    try:
        result = await db.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()
        if user:
            return user
        user = User(id=user_id)
        db.add(user)
        await db.commit()
        await db.refresh(user)
        logger.info(f"[user] created {user.id}")
        return user
    except Exception as e:
        logger.error("[user] get_or_create failed", exc=e, basic=True)
        await db.rollback()
        raise HTTPException(status_code=500, detail="Unable to resolve user")
