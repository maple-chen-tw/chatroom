from app.repos import chatroom_repo

def get_chatrooms(user_id: int):
    return chatroom_repo.get_chatrooms(user_id)

def get_chatroom(chatroom_id: int):
    return chatroom_repo.get_chatroom(chatroom_id)

def add_chatroom(members_id: list[int], chatroom_name: str = None):
    return chatroom_repo.add_chatroom(members_id, chatroom_name)
