# app/models/user.py
from pydantic import BaseModel, EmailStr
from datetime import datetime
from pydantic import Field

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

class UpdateUser(BaseModel):
    email: str | None = None
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
    chatroom_id: int
    chatroom_name: str | None = None
    friend_name: str