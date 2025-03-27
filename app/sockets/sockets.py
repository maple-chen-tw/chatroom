import socketio

# 創建 Socket.IO 伺服器
sio = socketio.AsyncServer(
    async_mode="asgi",
    cors_allowed_origins=["http://localhost:5173"],
    # cors_allowed_origins=["*"],
    transports=["polling", "websocket"],
)

# 創建 ASGI 應用程式
sio_app = socketio.ASGIApp(sio, socketio_path="/ws/socket.io")
# sio_app = socketio.ASGIApp(sio_server)

# 監聽使用者連線
@sio.event
async def connect(sid, environ, auth):
    print(f"User {sid} connected")

# 監聽使用者加入房間
@sio.event
async def join_room(sid, room_id):
    await sio.enter_room(sid, room_id)
    print(f"User {sid} joined room {room_id}")

# 監聽使用者發送訊息
@sio.event
async def send_message(sid, data):
    room_id = data.get("room")
    message = data.get("text")
    timestamp = data.get("timestamp")
    user = data.get("user")
    item_type = data.get("itemType")
    is_sent_by_viewer = data.get("isSentByViewer")

    if not room_id or not message:
        print(f"Invalid message data: {data}")
        return

    print(f"User {sid} sent message to room {room_id}: {message}")

    # 廣播訊息到該房間
    message_data = {
        # "utemId": "unique-id",
        "user": user,
        "timestamp": timestamp,
        "itemType": item_type,
        "isSentByViewer": is_sent_by_viewer,
        # "uqSeqId": 1,
        "text": message,
        "img": "",
        "reactions": []
    }
 
    await sio.emit("receive_message", message_data, room=room_id)

# 監聽使用者傳送一般訊息（非房間聊天）
@sio.event
async def message(sid, data):
    print(f"Received message from {sid}: {data}")
    await sio.emit("message", data)

# 監聽使用者斷線
@sio.event
async def disconnect(sid):
    print(f"User {sid} disconnected")
