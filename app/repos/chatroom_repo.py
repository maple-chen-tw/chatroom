from app.models.db import Chatroom, Participant
from app.db.context import session_maker

def get_chatrooms(user_id: int):
    with session_maker() as session:
        result = session.query(
            Chatroom
        ).join(
            Participant
        ).filter(
            Participant.user_id == user_id
        ).all()
        
    return result