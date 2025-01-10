
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import Float
from sqlalchemy import String
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy.sql.functions import current_timestamp

from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
class User(Base):
    __tablename__ = 'users'
    id = Column("id", Integer(), primary_key=True, autoincrement=True)
    username = Column("username", String(32))
    email = Column("email", String(256), unique=True)
    hashed_password = Column("hashed_password", String(256))
    nickname = Column("nickname", String(32))
    avatar_url = Column("avatar_url", String(256))
    status = Column("status", String(256))
    created_at = Column("created_at", DateTime(), default=current_timestamp())
    updated_at = Column("updated_at", DateTime(), default=current_timestamp())