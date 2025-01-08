# app/controllers/auth.py
from fastapi import HTTPException, status
from app.models.user import User
from app.db import fake_users_db

def authenticate_user(username: str, password: str):
    user = fake_users_db.get(username)
    if user and user["password"] == password:
        return User(username=user["username"], password=user["password"])
    return None

def login_user(user: User):
    authenticated_user = authenticate_user(user.username, user.password)
    if not authenticated_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return authenticated_user
