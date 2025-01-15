
from app.models.db import User
from app.repos import friend_repo
def get_accepted_friends(user_id: int) ->list[User]:
    return friend_repo.get_accepted_friends(user_id)

def add_friend(user_id: int, friend_id: int):
    return friend_repo.add_friend(user_id, friend_id)

def get_pending_friend(user_id: int) ->list[User]:
    return friend_repo.get_pending_friend(user_id)

def get_search_by_username(username: str) -> User | None:
    return friend_repo.get_search_by_username(username)