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

from log_config import get_logger
logger = get_logger(__name__)

def get_user(token: Annotated[str, Depends(oauth2_scheme)])->db.User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        logger.debug(f"Attempting to decode token: {token}")
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            logger.warning("Token payload does not contain 'sub'")
            raise credentials_exception
        logger.debug(f"Token decoded successfully. Username: {username}")       
        token_data = TokenData(username=username)

        user = user_service.get_by_username(token_data.username)
        if user is None:
            logger.warning(f"User not found in database: {username}")
            raise credentials_exception
        
        logger.info(f"Authenticated user: {user.username} (id={user.user_id})")
        
    except InvalidTokenError as e:
        logger.warning(f"Invalid token: {e}")
        raise credentials_exception

    return user

user_dependency = Annotated[db.User, Depends(get_user)]