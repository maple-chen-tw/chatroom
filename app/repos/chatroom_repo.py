from app.models.db import Chatroom, Participant, Message, User
from app.db.context import session_maker
from app.models import dto
def get_chatrooms(user_id: int):
    with session_maker() as session:
        chatrooms = session.query(
            Chatroom
        ).join(
            Participant
        ).filter(
            Participant.user_id == user_id
        ).all()

        result = []

        for chatroom in chatrooms:
            participants = session.query(Participant).filter(Participant.chatroom_id == chatroom.chatroom_id).all()
            if len(participants) == 2:
                other_user_id = next(p.user_id for p in participants if p.user_id != user_id)
                friend = session.query(User).filter(User.user_id == other_user_id).first()
                friend_username = friend.username if friend else None
                friend_nickname = friend.nickname
                friend_avatar_url = friend.avatar_url 
            else:
                friend_username = None
            result.append({
                'chatroom_id': chatroom.chatroom_id,
                'chatroom_name': chatroom.chatroom_name or "private chatroom",
                'friend_username': friend_username,
                'friend_nickname': friend_nickname,
                'friend_avatar_url': friend_avatar_url,
            })

    return result

def get_chatroom(chatroom_id: int):
    with session_maker.begin() as session:
        return session.query(Chatroom).where(
            Chatroom.chatroom_id == chatroom_id
        ).first()

def add_chatroom(members_id: list[int], chatroom_name: str = None):
    with session_maker() as session:
        try:
            new_chatroom = Chatroom(chatroom_name=chatroom_name)
            session.add(new_chatroom)
            session.commit()

            chatroom_id = new_chatroom.chatroom_id

            participants = [Participant(chatroom_id=chatroom_id, user_id=user_id) for user_id in members_id]
            session.add_all(participants)
            session.commit()

            return chatroom_id

        except Exception as e:
            session.rollback()
            raise e


def get_messages(chatroom_id: bytes):

    return

def add_message(chatroom_id: bytes, message: dto.Message, user_id: int):

    with session_maker() as session:
        try:
            new_message = Message(
                chatroom_id=chatroom_id,
                user_id=user_id,
                content=message.content,
                message_type=message.message_type,
                media_url=message.media_url,
                read_status=message.read_status
            )
            
            session.add(new_message)
            session.commit()
            
            return new_message.message_id

        except Exception as e:
            session.rollback()
            raise e
