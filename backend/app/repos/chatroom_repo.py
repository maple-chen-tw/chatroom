from app.models.db import Chatroom, Participant, Message, User
from app.db.context import session_maker
from app.models import dto
from datetime import datetime
from sqlalchemy import select, func
import uuid

def get_chatrooms(user_id: int):
    with session_maker() as session:
        chatrooms = session.query(Chatroom).join(
            Participant
        ).filter(
            Participant.user_id == user_id
        ).all()

        result = []

        for chatroom in chatrooms:
            participants = session.query(Participant).filter(
                Participant.chatroom_id == chatroom.chatroom_id
            ).all()

            if len(participants) == 2:
                other_user_id = next(p.user_id for p in participants if p.user_id != user_id)
                friend = session.query(User).filter(User.user_id == other_user_id).first()
                friend_user_id = friend.user_id
                friend_username = friend.username
                friend_nickname = friend.nickname
                friend_avatar_url = friend.avatar_url
                friend_status = friend.status
            else:
                friend_user_id = None
                friend_username = None
                friend_nickname = None
                friend_avatar_url = None
                friend_status = None

            result.append({
                'chatroom_id': chatroom.chatroom_id,
                'chatroom_name': chatroom.chatroom_name or "private chatroom",
                'user_id': friend_user_id,
                'username': friend_username,
                'nickname': friend_nickname,
                'avatar_url': friend_avatar_url,
                'status': friend_status,
            })

    return result

def get_chatroom(chatroom_id: str):
    with session_maker.begin() as session:
        return session.query(Chatroom).where(
            Chatroom.chatroom_id == chatroom_id
        ).first()

def add_chatroom(members_id: list[int], chatroom_name: str = None):
    user1, user2 = members_id
    with session_maker() as session:
        try:
            subquery = (
                session.query(Participant.chatroom_id)
                .filter(Participant.user_id.in_([user1, user2]))
                .group_by(Participant.chatroom_id)
                .having(func.count(Participant.user_id) == 2)
            )

            existing_chatroom_id = subquery.first()
            if existing_chatroom_id:
                return existing_chatroom_id[0]  # 已是 str，不用轉

            # 建立新聊天室
            new_chatroom = Chatroom(chatroom_name=chatroom_name)
            session.add(new_chatroom)
            session.commit()  # 確保 chatroom_id 被生成

            chatroom_id = new_chatroom.chatroom_id

            participants = [
                Participant(chatroom_id=chatroom_id, user_id=user_id)
                for user_id in members_id
            ]
            session.add_all(participants)
            session.commit()

            return chatroom_id

        except Exception as e:
            session.rollback()
            raise e

def get_messages(chatroom_id: str, limit: int, before: datetime | None = None):
    with session_maker() as session:
        query = session.query(Message).filter(Message.chatroom_id == chatroom_id)

        if before:
            query = query.filter(Message.timestamp < before)

        query = query.order_by(Message.timestamp.desc()).limit(limit)
        messages = query.all()

        sender_ids = list({message.sender_id for message in messages})
        users = session.query(User).filter(User.user_id.in_(sender_ids)).all()
        user_map = {user.user_id: user for user in users}

        result = []
        for message in messages:
            sender = user_map.get(message.sender_id)
            message_dict = {
                "chatroom_id": message.chatroom_id,
                "content": message.content,
                "message_type": message.message_type,
                "media_url": message.media_url,
                "read_status": message.read_status,
                "timestamp": message.timestamp,
                "user": {
                    'id': sender.user_id,
                    'nickname': sender.nickname,
                    'username': sender.username,
                    'profilePictureUrl': sender.avatar_url,
                }
            }
            result.append(dto.Message(**message_dict))
        return result[::-1]

def add_message(chatroom_id: str, message: dto.Message, user_id: int):
    with session_maker() as session:
        try:
            new_message = Message(
                chatroom_id=chatroom_id,
                sender_id=user_id,
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
