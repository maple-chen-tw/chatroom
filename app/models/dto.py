# app/models/user.py
from pydantic import BaseModel, EmailStr
from datetime import datetime

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class User(BaseModel):
    user_id: int 
    username: str
    email: str | None = None
    disabled: bool | None = None
    nickname: str | None = None 
    avatar_url: str | None = None 
    status: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None 


class UserInDB(User):
    hashed_password: str
