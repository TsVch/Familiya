from datetime import datetime, timezone
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database import get_db
from models import ChatUser, Message, User
from utils.deps import get_current_user

router = APIRouter(tags=["messages"])


class MessagePayload(BaseModel):
    chat_id: int
    text: Optional[str] = None
    file_path: Optional[str] = None


@router.get("/messages")
def get_messages(
    chat_id: int,
    since_id: int | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    membership = (
        db.query(ChatUser)
        .filter(ChatUser.user_id == current_user.id, ChatUser.chat_id == chat_id)
        .first()
    )
    if not membership:
        raise HTTPException(status_code=403, detail="Access denied to this chat")

    query = db.query(Message).filter(Message.chat_id == chat_id)
    if since_id is not None:
        query = query.filter(Message.id > since_id)

    messages = query.order_by(Message.created_at.asc(), Message.id.asc()).all()
    return [
        {
            "id": msg.id,
            "chat_id": msg.chat_id,
            "user_id": msg.user_id,
            "username": msg.user.username,
            "text": msg.text,
            "file_path": msg.file_path,
            "created_at": msg.created_at.isoformat(),
        }
        for msg in messages
    ]


@router.post("/messages")
def send_message(
    payload: MessagePayload,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    membership = (
        db.query(ChatUser)
        .filter(ChatUser.user_id == current_user.id, ChatUser.chat_id == payload.chat_id)
        .first()
    )
    if not membership:
        raise HTTPException(status_code=403, detail="Access denied to this chat")

    if not payload.text and not payload.file_path:
        raise HTTPException(status_code=400, detail="Message text or file is required")

    message = Message(
        chat_id=payload.chat_id,
        user_id=current_user.id,
        text=payload.text,
        file_path=payload.file_path,
        created_at=datetime.now(timezone.utc),
    )
    db.add(message)
    db.commit()
    db.refresh(message)

    return {
        "id": message.id,
        "chat_id": message.chat_id,
        "user_id": message.user_id,
        "username": current_user.username,
        "text": message.text,
        "file_path": message.file_path,
        "created_at": message.created_at.isoformat(),
    }
