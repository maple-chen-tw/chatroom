# app/controllers/auth.py
from fastapi import HTTPException, status, APIRouter
from app.models import db
from app.models import dto
from passlib.context import CryptContext
from app.fake_db import fake_users_db
from app.services.jwt_service import *
from app.services import user_service
from constants import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES


router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)


@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=dto.GetUser)
async def register(user: dto.CreateUser):

    if not user.username:
        raise HTTPException(
            detail="Username can not be empty",
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY
        )
    if not user.password:
        raise HTTPException(
            detail="Password can not be empty",
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY
        )
    exist_user = user_service.get_by_username(user.username)
    if exist_user:
        raise HTTPException(
            detail=f"User '{user.username}' exist",
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY
        )
    return user_service.create(
        user.username,
        user.password
    )
    
# login
@router.post("/token", status_code=status.HTTP_200_OK)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    
    user = user_service.get_by_username(form_data.username)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
            )
    
    if not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Incorrect password",
            headers={"WWW-Authenticate": "Bearer"},)
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")

@router.post("/logout", status_code=status.HTTP_200_OK)
async def logout(token: str = Depends(oauth2_scheme)):
    # add logic to check if token valid
    # let client delete token from local 
    return {"msg": "Successfully logged out"}


@router.get("/users/me/", response_model=dto.GetUser)
async def read_users_me(
    current_user: Annotated[dto.GetUser, Depends(get_current_user)],
):
    return current_user


@router.get("/users/me/items/")
async def read_own_items(
    current_user: Annotated[dto.GetUser, Depends(get_current_user)],
):
    return [{"item_id": "Foo", "owner": current_user.username}]
