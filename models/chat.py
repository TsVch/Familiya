from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from database import Base


class Chat(Base):
    __tablename__ = "chats"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)

    users = relationship("ChatUser", back_populates="chat", cascade="all, delete-orphan")
    messages = relationship("Message", back_populates="chat", cascade="all, delete-orphan")
