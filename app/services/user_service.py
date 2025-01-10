
from models import db
from repos import user_repo
from services import jwt_service
def get_by_username(username: int) -> db.User | None:
    return user_repo.get_by_username(username)

def create(username:str, password: str) -> db.User:
    hashed_password = jwt_service.get_password_hash(password)
    return user_repo.add(username, hashed_password)