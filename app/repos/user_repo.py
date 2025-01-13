from sqlalchemy import Delete
from sqlalchemy import Update
from sqlalchemy.sql.functions import current_timestamp

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

def get(limit:int = 1000, offset: int = 0) -> list[User]:
    with session_maker() as session:
        return session.query(User).limit(limit).offset(offset).all()

def update(user_id: int, username: str, email: str, hashed_password: str) -> None:
    with session_maker.begin() as session:
        session.execute(Update(User).where(User.user_id == user_id).values({
            User.username: username,
            User.email: email,
            User.hashed_password: hashed_password,
            User.updated_at: current_timestamp()
        }))