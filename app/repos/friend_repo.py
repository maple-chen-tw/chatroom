from app.models.db import Friend, User
from sqlalchemy import and_, or_
from app.db.context import session_maker
from fastapi import HTTPException, status
def get_friends(user_id: int) -> list[User]:
    with session_maker() as session:
        result = session.query(
            User.user_id,
            User.username,
            User.nickname,
            User.avatar_url
        ).join(Friend, 
            (Friend.user_id == User.user_id) | (Friend.friend_id == User.user_id)
        ).filter(
            ((Friend.user_id == user_id) | (Friend.friend_id == user_id)),
            Friend.status == 'accepted',
            User.user_id != user_id
        ).all()
        
    return result

def get_sent_requests(user_id: int) -> list[User]:
    with session_maker() as session:
        result = session.query(
            User.user_id,
            User.username,
            User.nickname,
            User.avatar_url
        ).join(
            Friend, Friend.friend_id == User.user_id
        ).filter(
            Friend.user_id == user_id,
            Friend.status == 'pending'
        ).all()
    
    return result

def get_received_requests(user_id: int) -> list[User]:
    with session_maker() as session:
        result = session.query(
            User.user_id,
            User.username,
            User.nickname,
            User.avatar_url
        ).join(
            Friend, Friend.user_id == User.user_id
        ).filter(
            Friend.friend_id == user_id,
            Friend.status == 'pending'
        ).all()
    
    return result

def sent_request(user_id: int, friend_id: int) -> None:

    with session_maker.begin() as session:
        existing_friendship = session.query(Friend).filter(
            ((Friend.user_id == user_id) & (Friend.friend_id == friend_id)) |
            ((Friend.user_id == friend_id) & (Friend.friend_id == user_id))
        ).first()

        if existing_friendship:
            if existing_friendship.status == "accepted":
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Already friends"
                )
            elif existing_friendship.status == "pending":
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Friend request already sent"
                )

        relationship = Friend()
        relationship.user_id = user_id
        relationship.friend_id = friend_id
        relationship.status = "pending"
        
        session.add(relationship)
        session.flush()
        session.refresh(relationship)
    return


def accept_request(user_id: int, friend_id: int) -> None:
    with session_maker.begin() as session:
        friendship = session.query(Friend).filter(
            Friend.user_id == friend_id,
            Friend.friend_id == user_id,
            Friend.status == 'pending'
        ).first()
        if not friendship:
            raise ValueError("Friend request not found or already processed.")
        
        friendship.status = 'accepted'



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

def delete_friend(user_id: int, friend_id: int) -> None:
    with session_maker.begin() as session:
        session.query(Friend).filter(
            Friend.status == "accepted",
            or_(
                and_(
                    Friend.user_id == user_id,
                    Friend.friend_id == friend_id
                ),
                and_(
                    Friend.user_id == friend_id,
                    Friend.friend_id == user_id
                )
            )
        ).delete(synchronize_session=False)

def reject_request(user_id: int, friend_id: int) -> None:
    with session_maker.begin() as session:
        session.query(Friend).filter(
            Friend.status == "pending",
            or_(
                and_(
                    Friend.user_id == user_id,
                    Friend.friend_id == friend_id
                ),
                and_(
                    Friend.user_id == friend_id,
                    Friend.friend_id == user_id
                )
            )
        ).delete(synchronize_session=False)
'''
def delete_friend(user_id: int, friend_id: int) -> None:
    with session_maker.begin() as session:
        session.execute(Delete(Friend).where(
            (Friend.status == "accepted") &
            ((Friend.user_id == user_id and Friend.friend_id == friend_id) | (Friend.user_id == friend_id and Friend.friend_id == user_id))
        ))

def reject_request(user_id: int, friend_id: int) -> None:
    with session_maker.begin() as session:
        session.execute(Delete(Friend).where(
            (Friend.status == "pending") & 
            ((Friend.user_id == user_id and Friend.friend_id == friend_id) | (Friend.user_id == friend_id and Friend.friend_id == user_id))
        ))
'''