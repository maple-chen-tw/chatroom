from sqlalchemy import Delete
from sqlalchemy import Update
from sqlalchemy import func
from app.models.db import User
from app.db.context import session_maker

def add(username: str, hashed_password: str)-> User:
    with session_maker.begin() as session:
        user = User()
        user.username = username
        user.hashed_password = hashed_password
        session.add(user)
        session.flush()
        #session.commit()
        session.refresh(user)
        
        return user
    
def get_by_username(username: str) -> User | None:
    with session_maker.begin() as session:
        return session.query(User).where(
            User.username == username          
        ).first()
    
def get_by_user_id(user_id: int) -> User | None:
    with session_maker() as session:
        return session.query(User).where(
            User.user_id == user_id          
        ).first()

def get(limit:int = 1000, offset: int = 0) -> list[User]:
    with session_maker() as session:
        return session.query(User).limit(limit).offset(offset).all()

def update(user_id: int, email: str, nickname: str, avatar_url: str, status:str) -> User | None:
    update_data = {}
    if email not in [None, '']:
        update_data[User.email] = email
    if nickname is not None:
        update_data[User.nickname] = nickname
    if avatar_url is not None:
        update_data[User.avatar_url] = avatar_url
    if status is not None:
        update_data[User.status] = status
    update_data[User.updated_at] = func.current_timestamp()

    with session_maker.begin() as session:
        result  = session.execute(Update(User).where(User.user_id == user_id).values(update_data))
    
    if result.rowcount == 0:
        return None

    return get_by_user_id(user_id)  

def delete(user_id: int) -> None:
    with session_maker.begin() as session:
        session.execute(Delete(User).where(User.user_id == user_id))