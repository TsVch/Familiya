from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from database import get_db
from models import Chat, ChatUser, User
from utils.auth import create_access_token, hash_password, verify_password

router = APIRouter(tags=["auth"])


class AuthPayload(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=4, max_length=100)


@router.post("/register")
def register(payload: AuthPayload, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.username == payload.username).first()
    if existing:
        raise HTTPException(status_code=400, detail="Username already exists")

    user = User(
        username=payload.username,
        password_hash=hash_password(payload.password),
    )
    db.add(user)
    db.flush()

    default_chat = db.query(Chat).filter(Chat.name == "Family").first()
    if default_chat is None:
        default_chat = Chat(name="Family")
        db.add(default_chat)
        db.flush()

    membership = (
        db.query(ChatUser)
        .filter(ChatUser.user_id == user.id, ChatUser.chat_id == default_chat.id)
        .first()
    )
    if membership is None:
        db.add(ChatUser(user_id=user.id, chat_id=default_chat.id))

    db.commit()

    token = create_access_token({"sub": str(user.id)})
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {"id": user.id, "username": user.username},
    }


@router.post("/login")
def login(payload: AuthPayload, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == payload.username).first()
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )

    token = create_access_token({"sub": str(user.id)})
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {"id": user.id, "username": user.username},
    }
