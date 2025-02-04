from app.models.db import Chatroom, Participant
from app.db.context import session_maker
from app.models.db import User
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
                friend_name = friend.username if friend else None
            else:
                friend_name = None
            result.append({
                'chatroom_id': chatroom.chatroom_id,
                'chatroom_name': chatroom.chatroom_name or "private chatroom",
                'friend_name': friend_name
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
