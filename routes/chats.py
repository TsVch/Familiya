from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from models import Chat, ChatUser
from utils.deps import get_current_user

router = APIRouter(tags=["chats"])


@router.get("/chats")
def get_chats(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    chats = (
        db.query(Chat)
        .join(ChatUser, Chat.id == ChatUser.chat_id)
        .filter(ChatUser.user_id == current_user.id)
        .order_by(Chat.id.asc())
        .all()
    )
    return [{"id": chat.id, "name": chat.name} for chat in chats]
