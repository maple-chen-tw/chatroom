from fastapi import HTTPException, status, APIRouter
from fastapi import Path
from app.models import db
from app.models import dto
from app.services import friend_service
from utils import dependencies
router = APIRouter(
    prefix="/friends",
    tags=["Friends"],
)
@router.get("/", response_model=list[dto.Friend])
def get_friends(user: dependencies.user_dependency) -> list[db.User]:
    friends = friend_service.get_friends(user.user_id)
    if not friends:
        return []
    return friends

@router.post("/request")
def sent_request(user_id: int, friend_id: int, user: dependencies.user_dependency) -> None:
    if user.user_id != user_id:
        raise HTTPException(status_code=403, detail="Forbidden")
    
    if user_id == friend_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You cannot add yourself as a friend."
        )
    friend_service.sent_request(user_id, friend_id)


# get pending requests
@router.get("/requests/pending", response_model=list[dto.Friend])
def get_received_requests(user_id: int, user: dependencies.user_dependency)-> db.User:
    if user.user_id != user_id:
        raise HTTPException(status_code=403, detail="Forbidden")

    pending_friend_requests = friend_service.get_received_requests(user_id)
    return pending_friend_requests 

# get sent requests
@router.get("/requests/sent", response_model=list[dto.Friend])
def get_sent_requests(user_id: int, user: dependencies.user_dependency) -> db.User:
    if user.user_id != user_id:
        raise HTTPException(status_code=403, detail="Forbidden")
    sent_requests = friend_service.get_sent_requests(user_id)
    return sent_requests

@router.post("/requests/accepted")
def accept_request(user_id: int, friend_id: int, user: dependencies.user_dependency) -> None:
    if user.user_id != user_id:
        raise HTTPException(status_code=403, detail="Forbidden")
    friend_service.accept_request(user_id, friend_id)

@router.delete("/requests/reject", status_code=204)
def reject_request(user_id: int, friend_id: int, user: dependencies.user_dependency) -> None:
    if user.user_id != user_id:
        raise HTTPException(status_code=403, detail="Forbidden")
    friend_service.reject_request(user_id, friend_id)

@router.get("/search", response_model = dto.Friend)
def get_search_by_username(username: str, user: dependencies.user_dependency)-> db.User | None:

    user = friend_service.get_search_by_username(username)
    if user is None:
        raise HTTPException(status_code=404, detail="User with username not found")
    
    return dto.Friend(
        user_id=user.user_id,
        username=user.username,
        nickname=user.nickname, 
        avatar_url=user.avatar_url
    )

@router.delete("/", status_code=204)
def delete_friend(user_id: int, friend_id: int, user: dependencies.user_dependency) -> None:
    if user.user_id != user_id:
        raise HTTPException(status_code=403, detail="Forbidden")
    friend_service.delete_friend(user_id, friend_id)
    