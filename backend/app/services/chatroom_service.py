from datetime import datetime
from app.repos import chatroom_repo
from app.models import dto
def get_chatrooms(user_id: int):
    return chatroom_repo.get_chatrooms(user_id)

def get_chatroom(chatroom_id: str):
    return chatroom_repo.get_chatroom(chatroom_id)

def add_chatroom(members_id: list[int], chatroom_name: str = None):
    return chatroom_repo.add_chatroom(members_id, chatroom_name)

def get_messages(chatroom_id: str, limit: int, before: datetime | None = None):
    return chatroom_repo.get_messages(chatroom_id, limit, before)

def add_message(chatroom_id: str, message: dto.Message, user_id: int):
    return chatroom_repo.add_message(chatroom_id, message, user_id)