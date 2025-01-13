from fastapi import HTTPException, status, APIRouter
from fastapi import Path
from app.models import db
from app.models import dto
from app.services import user_service
from utils import dependencies
router = APIRouter(
    prefix="/user",
    tags=["Users"]
)

@router.get("/{user_id}", response_model=dto.GetUser)
def get_by_user_id(user_id: int, user: dependencies.user_dependency) -> db.User:

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    if user.user_id != user_id:
        raise HTTPException(status_code=403, detail="Forbidden")
    return user


@router.patch("/{user_id}", response_model=dto.GetUser)
def patch_user(user_id: int, user_data: dto.UpdateUser, user: dependencies.user_dependency) -> db.User:
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    if user.user_id != user_id:
        raise HTTPException(status_code=403, detail="Forbidden")
    
    updated_user = user_service.update(user_id, user_data)
    return updated_user


@router.delete("/{user_id}", status_code=204)
def delete_user(user_id: int, user: dependencies.user_dependency):
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    if user.user_id != user_id:
        raise HTTPException(status_code=403, detail="Forbidden")
    
    user_service.delete_user(user_id)
    return None
