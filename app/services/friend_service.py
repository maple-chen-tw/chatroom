
from app.models.db import User
from app.repos import friend_repo

def get_friends(user_id: int) ->list[User]:
    return friend_repo.get_friends(user_id)

def sent_request(user_id: int, friend_id: int):
    return friend_repo.sent_request(user_id, friend_id)

def get_requests(user_id: int) ->list[User]:
    return friend_repo.get_requests(user_id)

def get_search_by_username(username: str) -> User | None:
    return friend_repo.get_search_by_username(username)

def accept_request(user_id: int, friend_id: int):
    return friend_repo.accept_request(user_id, friend_id)