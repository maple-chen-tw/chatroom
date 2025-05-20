import socketio
from log_config import get_logger
logger = get_logger(__name__)
from constants import ALLOWED_ORIGINS

sio = socketio.AsyncServer(
    async_mode="asgi",
    cors_allowed_origins=ALLOWED_ORIGINS,
    transports=["polling", "websocket"],
)

user_sockets = {}

sio_app = socketio.ASGIApp(sio, socketio_path="/ws/socket.io")


@sio.event
async def connect(sid, environ, auth):
    logger.info("User {sid} connected")

@sio.event
def set_user_id(sid, user_id):
    # Associate the socket ID with the user_id
    user_sockets[sid] = user_id
    logger.debug(f"User {user_id} is now connected with socket {sid}")

# 監聽使用者加入房間
@sio.event
async def join_room(sid, room_id):
    await sio.enter_room(sid, room_id)
    logger.info(f"User {sid} joined room {room_id}")

# 監聽使用者發送訊息
@sio.event
async def send_message(sid, data):
    chatroom_id = data.get("chatroom_id")
    message = data.get("content")
    timestamp = data.get("timestamp")
    user = data.get("user")
    message_type = data.get("message_type")
    is_sent_by_viewer = data.get("isSentByViewer")

    if not chatroom_id or not message:
        logger.warning("Invalid message data received")
        logger.debug(f"Room ID: {chatroom_id}, Message: {message}")

        return

    logger.info(f"User {sid} sent message to room {chatroom_id}: {message}")

    # 廣播訊息到該房間
    message_data = {
        "chatroom_id":chatroom_id,
        "content": message,
        "isSentByViewer": is_sent_by_viewer,
        "user": user,
        "timestamp": timestamp,
        "message_type": message_type,
        "img": "",
    }
 
    await sio.emit("receive_message", message_data, room=chatroom_id)

# 監聽使用者傳送一般訊息（非房間聊天）
@sio.event
async def message(sid, data):
    logger.debug(f"Received raw message from {sid}: {data}")
    await sio.emit("message", data)

# 監聽使用者斷線
@sio.event
async def disconnect(sid):
     logger.info(f"Socket disconnected: {sid}")
