from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from typing import List
from db_manager import db_manager
from services.chat import get_messages, add_message, clear_session
from schemas.message import MessageResponse


from config import config
from local_logs.logger import logger

router = APIRouter(prefix="/chat", tags=["Chat"])


@router.get("/{session_id}", response_model=List[MessageResponse])
async def get_chat_history(
    session_id: UUID, session: AsyncSession = Depends(db_manager.get_session)
):
    """
    Fetch all messages in given chat session, ordered by time
    """
    return await get_messages(session, session_id)


@router.delete("/{session_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_chat(
    session_id: UUID, session: AsyncSession = Depends(db_manager.get_session)
):
    """
    Remove all messages from a session.
    """
    await clear_session(session, session_id=session_id)
