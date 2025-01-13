from fastapi import Depends
from fastapi import HTTPException, status
import jwt
from jwt.exceptions import InvalidTokenError
from app.services import user_service
from app.services.jwt_service import oauth2_scheme
from app.models import db
from typing import Annotated
from constants import SECRET_KEY, ALGORITHM
from app.models.dto import TokenData

def get_user(token: Annotated[str, Depends(oauth2_scheme)])->db.User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception
    
    user = user_service.get_by_username(token_data.username)
    if user is None:
        raise credentials_exception
    
    return user

user_dependency = Annotated[db.User, Depends(get_user)]