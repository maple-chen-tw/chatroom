from sqlalchemy.sql import func
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
class User(Base):
    __tablename__ = 'users'
    user_id = Column("user_id", Integer(), primary_key=True, autoincrement=True)
    username = Column("username", String(32), unique=True, nullable=False)
    email = Column("email", String(256), unique=True)
    hashed_password = Column("hashed_password", String(256), nullable=False)
    nickname = Column("nickname", String(32))
    avatar_url = Column("avatar_url", String(256))
    status = Column("status", String(256))
    created_at = Column("created_at", DateTime(), default=func.current_timestamp())
    updated_at = Column("updated_at", DateTime(), default=func.current_timestamp(), onupdate=func.current_timestamp())

class Friend(Base):
    __tablename__ = 'friends'

    user_id = Column(Integer, ForeignKey('users.user_id', ondelete='CASCADE'), primary_key=True)  
    friend_id = Column(Integer, ForeignKey('users.user_id', ondelete='CASCADE'), primary_key=True)
    status = Column(String(50), nullable=False)  # friends relationship status: pending, accepted, rejected, deleted
    created_at = Column(DateTime, default=func.current_timestamp())

    user = relationship("User", foreign_keys=[user_id])
    friend = relationship("User", foreign_keys=[friend_id])

class Chatroom(Base):
    __tablename__ = 'chatrooms'
    
    chatroom_id = Column(Integer, primary_key=True, autoincrement=True)
    chatroom_name = Column(String(32), nullable=True)  # Name of the chatroom (null for private chats)
    created_at = Column(DateTime, default=func.current_timestamp())

class Participant(Base):
    __tablename__ = 'participants'
    
    chatroom_id = Column(Integer, ForeignKey('chatrooms.chatroom_id', ondelete='CASCADE'), primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id', ondelete='CASCADE'), primary_key=True)
    
    chatroom = relationship('Chatroom', back_populates='participants')
    user = relationship('User', back_populates='participants')