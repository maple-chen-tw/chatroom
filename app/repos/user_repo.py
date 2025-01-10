from sqlalchemy import Delete
from sqlalchemy import Update
from sqlalchemy.sql.functions import current_timestamp

from models.db import User
from db.context import session_maker

def add(username: str, email:str, hashed_password: str)-> User:
    with session_maker.begin() as session:
        user = User()
        user.username = username
        user.email = email
        user.hashed_password = hashed_password
        session.add(user)
        session.flush()

        return user
    
def get_by_username(username: str) -> User | None:
    with session_maker.begin() as session:
        return session.query(User).where(
            User.username == username          
        ).first()