from fastapi import HTTPException, status, APIRouter
from fastapi import Path
from app.models import db
from app.models import dto
from app.services import friend_service, chatroom_service, user_service
from utils import dependencies
router = APIRouter(
    prefix="/chatrooms",
    tags=["Chatrooms"],
)

# Retrieves the list of chatrooms
@router.get("/chatrooms", response_model=list[dto.Chatroom])
def get_chatrooms(user_id: int, user: dependencies.user_dependency) -> list[db.Chatroom]:
    if user.user_id != user_id:
        raise HTTPException(status_code=403, detail="Forbidden")
    chatrooms = chatroom_service.get_chatrooms(user_id)
    return chatrooms

@router.post("/chatrooms", response_model=dto.Chatroom)
def add_chatroom(user_id: int, members_id: list[int], user: dependencies.user_dependency, chatroom_name: str = None) -> db.Chatroom:
    if user.user_id != user_id:
        raise HTTPException(status_code=403, detail="Forbidden")
    if user_id not in members_id:
        members_id.append(user_id)
    if len(members_id) < 2:
        raise HTTPException(status_code=400, detail="A chatroom must have at least 2 members")
    
    chatroom_id = chatroom_service.add_chatroom(members_id, chatroom_name)

    if len(members_id) == 2:
        friend_id = [mid for mid in members_id if mid != user_id][0]
        friend = user_service.get_by_user_id(friend_id)
        friend_name = friend.username
    else:
        friend_name = None
    return dto.Chatroom(
        chatroom_id=chatroom_id,
        chatroom_name=chatroom_name,
        friend_name=friend_name
    )

# Retrieves the details of the chatroom
@router.get("/chatrooms/{chatroom_id}",response_model=dto.Chatroom)
def get_chatroom(user_id: int, chatroom_id: int, user: dependencies.user_dependency) -> db.Chatroom:
    if user.user_id != user_id:
        raise HTTPException(status_code=403, detail="Forbidden")
    chatroom = chatroom_service.get_chatroom(chatroom_id)
    return chatroom

@router.post("/chatrooms/{chatroom_id}", response_model=None)
def update_chatroom(chatroom_id: int, user: dependencies.user_dependency) -> None:
    return