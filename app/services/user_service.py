
from app.models.db import User
from app.repos import user_repo
from app.services import jwt_service
from app.models import dto
from typing import Optional


def create(username:str, password: str) -> User:
    hashed_password = jwt_service.get_password_hash(password)
    return user_repo.add(username, hashed_password)

def get(limit: int, offset: int) -> list[User]:
    return user_repo.get(limit=limit, offset=offset)

def get_by_user_id(user_id: int) -> User | None:
    return user_repo.get_by_user_id(user_id)

def get_by_username(username: int) -> User | None:
    return user_repo.get_by_username(username)

def update(user_id: int, user_data: dto.UpdateUser) -> User:
    return user_repo.update(
        user_id, 
        user_data.nickname, 
        user_data.avatar_url, 
        user_data.status
    )

def delete(user_id: int) -> None:
    user_repo.delete(user_id)
