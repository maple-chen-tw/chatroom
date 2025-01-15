from app.models.db import Friend, User
from app.db.context import session_maker

def get_accepted_friends(user_id: int) -> list[User]:
    with session_maker() as session:
        result = session.query(
            Friend.friend_id,
            User.username,
            User.nickname,
            User.avatar_url
        ).join(Friend, 
            (Friend.user_id == User.user_id) | (Friend.friend_id == User.user_id)
        ).filter(
            ((Friend.user_id == user_id) | (Friend.friend_id == user_id)),
            Friend.status == 'accepted'
        ).all()
        
    return result

def get_pending_friend(user_id: int) -> list[User]:
    with session_maker() as session:
        result = session.query(
            Friend.friend_id,
            User.username,
            User.nickname,
            User.avatar_url
        ).join(Friend, 
            (Friend.user_id == User.user_id) | (Friend.friend_id == User.user_id)
        ).filter(
            ((Friend.user_id == user_id) | (Friend.friend_id == user_id)),
            Friend.status == 'pending'
        ).all()
    
    return result

def add_friend(user_id: int, friend_id: int):
    with session_maker.begin() as session:
        relationship = Friend()
        relationship.user_id = user_id
        relationship.friend_id = friend_id
        relationship.status = "pending"
        session.add(relationship)
        session.flush()
        #session.commit()
        session.refresh(relationship)
    return relationship


def get_search_by_username(username: str) -> User | None:
    with session_maker.begin() as session:
        result =  session.query(
            User.user_id,
            User.username,
            User.nickname,
            User.avatar_url
        ).where(
            User.username == username          
        ).first()
    return result