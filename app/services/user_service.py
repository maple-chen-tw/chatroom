
from app.models import db
from app.repos import user_repo
from app.services import jwt_service
from app.models import dto
def get_by_username(username: int) -> db.User | None:
    return user_repo.get_by_username(username)

def create(username:str, password: str) -> db.User:
    hashed_password = jwt_service.get_password_hash(password)
    return user_repo.add(username, hashed_password)

def get(limit: int, offset: int) -> list[db.User]:
    return user_repo.get(limit=limit, offset=offset)

def get_by_user_id(user_id: int) -> db.User | None:
    return user_repo.get_by_user_id(user_id)


def update(user_id: int, user_data: dto.UpdateUser) -> db.User:
    return user_repo.update(
        user_id, 
        user_data.email, 
        user_data.nickname, 
        user_data.avatar_url, 
        user_data.status
    )
