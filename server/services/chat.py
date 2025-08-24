from typing import Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status
from models import Message, Session
from schemas.message import MessageCreate
from models import Message
from uuid import UUID, uuid4


from config import config
from local_logs.logger import logger


async def get_messages(session: AsyncSession, session_id: UUID) -> Sequence[Message]:
    """
    Retrieve all messages for a given session, ordered by time
    """
    try:
        result = await session.execute(
            select(Message)
            .where(Message.session_id == session_id)
            .order_by(Message.created_at)
        )
        messages = result.scalars().all()
        logger.info(
            f"[service:chat] Fetched {len(messages)} messages for session {session_id}"
        )
        return messages
    except SQLAlchemyError as e:
        logger.error(
            "[service:chat] Failed to fetch messages:", exc=e, once=config.DEBUG
        )
        raise HTTPException(status_code=500, detail="Could not fetch messages")


async def add_message(
    session: AsyncSession, session_id: UUID, msg: MessageCreate
) -> Message:
    """
    Create and persist a new message for session
    """
    try:
        message = Message(
            id=uuid4(),
            session_id=session_id,
            role=msg.role,
            content=msg.content,
        )
        session.add(message)
        await session.commit()
        await session.refresh(message)
        logger.info(f"[service:chat] Added new message to session: {session_id}")
        return message
    except SQLAlchemyError as e:
        logger.error("[service:chat] Failed to save message:", exc=e, once=config.DEBUG)
        await session.rollback()
        raise HTTPException(status_code=500, detail="Could not save message.")


async def clear_session(session: AsyncSession, session_id: UUID) -> None:
    try:
        await session.execute(
            Message.__table__.delete().where(Message.session_id == session_id)
        )
        await session.commit()
        logger.info(f"[service:chat] Cleared messages for session {session_id}")
    except SQLAlchemyError as e:
        logger.error(
            "[service:chat] Failed to clear messages:", exc=e, once=config.DEBUG
        )
        await session.rollback()
        raise HTTPException(status_code=500, detail="Could not clear message")
