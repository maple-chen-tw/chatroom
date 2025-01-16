from fastapi import HTTPException, status, APIRouter
from fastapi import Path
from app.models import db
from app.models import dto
from app.services import friend_service
from utils import dependencies
router = APIRouter(
    prefix="/user",
    tags=["Friends"],
)
@router.get("/{user_id}/friends", response_model=list[dto.Friend])
def get_friends(user_id: int, user: dependencies.user_dependency):
    if user.user_id != user_id:
        raise HTTPException(status_code=403, detail="Forbidden")
    friends = friend_service.get_friends(user_id)
    return friends

@router.post("/{user_id}/friends/request")
def sent_request(user_id: int, friend_id: int, user: dependencies.user_dependency):
    if user.user_id != user_id:
        raise HTTPException(status_code=403, detail="Forbidden")
    
    if user_id == friend_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You cannot add yourself as a friend."
        )
    friend_service.sent_request(user_id, friend_id)
    #return {"message": "Friendship request sent successfully."}

# get friend requests
@router.get("/{user_id}/friends/requests", response_model=list[dto.Friend])
def get_requests(user_id: int, user: dependencies.user_dependency):
    if user.user_id != user_id:
        raise HTTPException(status_code=403, detail="Forbidden")

    pending_friend_requests = friend_service.get_requests(user_id)
    return pending_friend_requests 

@router.post("/{user_id}/friends/requests/accept")
def accept_request(user_id: int, friend_id: int, user: dependencies.user_dependency):
    if user.user_id != user_id:
        raise HTTPException(status_code=403, detail="Forbidden")
    friend_service.accept_request(user_id, friend_id)


@router.get("/{user_id}/search", response_model = dto.Friend)
def get_search_by_username(user_id: int,username: str, user: dependencies.user_dependency)-> db.User | None:
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    if user.user_id != user_id:
        raise HTTPException(status_code=403, detail="Forbidden")

    user = friend_service.get_search_by_username(username)
    if user is None:
        raise HTTPException(status_code=404, detail="User with username not found")
    return dto.Friend(
        friend_id=user.user_id,
        username=user.username,
        nickname=user.nickname, 
        avatar_url=user.avatar_url
    )

