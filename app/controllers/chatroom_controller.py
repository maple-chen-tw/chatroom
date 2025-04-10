from fastapi import HTTPException, status, APIRouter
from fastapi import Path
from app.models import db
from app.models import dto
from app.services import friend_service, chatroom_service, user_service
from utils import dependencies
import uuid
router = APIRouter(
    prefix="/chatrooms",
    tags=["Chatrooms"],
)

# Retrieves the list of chatrooms
@router.get("/", response_model=list[dto.ChatroomWithFriend])
def get_chatrooms(user: dependencies.user_dependency):
    chatrooms = chatroom_service.get_chatrooms(user.user_id)
    return chatrooms

@router.post("/", response_model=dto.Chatroom)
def add_chatroom(chatroom: dto.CreateChatroom ,user: dependencies.user_dependency) -> db.Chatroom:
    try:
        members_id = chatroom.members_id
        chatroom_name = chatroom.chatroom_name

        if not isinstance(members_id, list):
            raise HTTPException(status_code=400, detail="members_id must be a list")

        if not all(isinstance(mid, int) for mid in members_id):
            raise HTTPException(status_code=400, detail="Each member_id must be an integer")

        if user.user_id not in members_id:
            members_id.append(user.user_id)
            
        if len(members_id) < 2:
            raise HTTPException(status_code=400, detail="A chatroom must have at least 2 members")

        chatroom_id = chatroom_service.add_chatroom(members_id, chatroom_name)
        if len(members_id) == 2:
            friend_id = [mid for mid in members_id if mid != user.user_id][0]
            friend = user_service.get_by_user_id(friend_id)
            friend_name = friend.username
        else:
            friend_name = None
            
        return dto.Chatroom(
            chatroom_id=chatroom_id,
            chatroom_name=chatroom_name,
            friend_name=friend_name
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

# Retrieves the details of the chatroom
@router.get("/{chatroom_id}",response_model=dto.Chatroom)
def get_chatroom(chatroom_id: bytes, user: dependencies.user_dependency) -> db.Chatroom:
    chatroom = chatroom_service.get_chatroom(chatroom_id)
    return chatroom

# @router.post("/{chatroom_id}", response_model=None)
# def update_chatroom(chatroom_id: bytes, user: dependencies.user_dependency) -> None:
#     return

@router.get("/{chatroom_id}/messages", response_model = list[dto.Message])
def get_messages(chatroom_id: bytes, user: dependencies.user_dependency) -> list[db.Message]:
    messages = chatroom_service.get_messages(chatroom_id)
    return messages

@router.post("/{chatroom_id}/message", response_model = dto.Message)
def add_message(chatroom_id: bytes, message: dto.Message , user: dependencies.user_dependency) -> db.Message:
    message_id = chatroom_service.add_message(chatroom_id=chatroom_id, message=message, user_id = user.user_id)
    return message_id
