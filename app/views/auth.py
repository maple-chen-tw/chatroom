# app/views/auth.py
from fastapi import APIRouter
from app.controllers.auth import login_user
from app.models.user import User

router = APIRouter()

@router.post("/login")
async def login(request: User):
    user = login_user(request)
    return {"message": "Login successful", "username": user.username}
