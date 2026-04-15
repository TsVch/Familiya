from sqlalchemy import Column, ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import relationship

from database import Base


class ChatUser(Base):
    __tablename__ = "chat_users"
    __table_args__ = (UniqueConstraint("user_id", "chat_id", name="uq_user_chat"),)

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    chat_id = Column(Integer, ForeignKey("chats.id", ondelete="CASCADE"), nullable=False)

    user = relationship("User", back_populates="chats")
    chat = relationship("Chat", back_populates="users")
