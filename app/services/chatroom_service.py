from app.repos import chatroom_repo

def get_chatrooms(user_id: int):
    return chatroom_repo.get_chatrooms(user_id)