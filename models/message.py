from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from database import Base


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    chat_id = Column(Integer, ForeignKey("chats.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    text = Column(Text, nullable=True)
    file_path = Column(String, nullable=True)
    created_at = Column(DateTime, nullable=False)

    chat = relationship("Chat", back_populates="messages")
    user = relationship("User", back_populates="messages")
