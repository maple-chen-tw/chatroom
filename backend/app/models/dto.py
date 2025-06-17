# app/models/user.py
from enum import Enum
from pydantic import BaseModel
from datetime import datetime
from pydantic import Field
from typing import Optional

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None

class User(BaseModel):
    user_id: int 
    username: str
    email: str | None = None
    nickname: str | None = None 
    avatar_url: str | None = None 
    status: str | None = None
    created_at: datetime
    updated_at: datetime 

class UserInDB(User):
    hashed_password: str

class GetUser(BaseModel):
    user_id: int 
    username: str
    email: str | None = None
    nickname: str | None = None 
    avatar_url: str | None = None 
    status: str | None = None
    created_at: datetime
    updated_at: datetime

class CreateUser(BaseModel):
    username: str
    password: str = Field(..., min_length=4)
    email: str

class UpdateUser(BaseModel):
    nickname: str | None = None 
    avatar_url: str | None = None 
    status: str | None = None

class LoginUser(BaseModel):
    username: str
    password: str

class Friend(BaseModel):
    user_id: int
    username: str
    nickname: str | None = None
    avatar_url: str | None = None

class Chatroom(BaseModel):
    chatroom_id: str
    chatroom_name: str | None = None
    friend_name: str

    class Config:
        orm_mode = True

class CreateChatroom(BaseModel):
    chatroom_name: str = 'Default Chatroom'
    members_id: list[int]

class MessageType(str, Enum):
    text = 'text'
    image = 'image'
    audio = 'audio'
    file = 'file'
    video = 'video'

class ReadStatus(str, Enum):
    read = 'read'
    unread = 'unread'
    delivered = 'delivered'

class Message(BaseModel):
    chatroom_id: str
    user: Optional[dict] = None
    content:  str | None = None
    message_type: MessageType
    media_url:  str | None = None
    read_status: ReadStatus
    timestamp:  datetime | None = None
    class Config:
        orm_mode = True

class ChatroomWithFriend(BaseModel):
    chatroom_id: str
    chatroom_name: str | None = None
    user_id: int
    username: str 
    nickname: str| None = None
    avatar_url: str | None = None
    status: str| None = None

    class Config:
        orm_mode = True