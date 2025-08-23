from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from typing import List
from db_manager import db_manager
from services.chat import get_messages, add_message, clear_session
from schemas.message import MessageCreate, MessageResponse
from local_logs.logger import logger

router = APIRouter(prefix="/chat", tags=["Chat"])


@router.get("/{session_id}", response_model=List[MessageResponse])
async def get_chat_history(
    session_id: UUID, session: AsyncSession = Depends(db_manager.get_session)
):
    """
    Fetch all messages in given chat session, ordered by time
    """
    try:
        return await get_messages(session, session_id)
    except Exception as e:
        logger.error(f"[router:chat] Failed to get messages: {e}")
        raise HTTPException(status_code=500, detail="Unable to fetch messages")


@router.post(
    "/{session_id}", response_model=MessageResponse, status_code=status.HTTP_201_CREATED
)
async def post_message(
    session_id: UUID,
    message: MessageCreate,
    session: AsyncSession = Depends(db_manager.get_session),
):
    """
    Add new message (user | assistant) to a session
    """

    try:
        return await add_message(session, session_id, message)
    except Exception as e:
        logger.error(f"[router:chat] Failed to post message")
        raise HTTPException(status_code=500, detail="Unable to save message")


@router.delete("/{session_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_chat(
    session_id: UUID, session: AsyncSession = Depends(db_manager.get_session)
):
    """
    Remove all messages from a session.
    """
    try:
        await clear_session(session, session_id=session_id)
    except Exception as e:
        logger.error(f"[chat] Failed to clear messages: {e}")
    raise HTTPException(status_code=500, detail="Unable to clear messages")
