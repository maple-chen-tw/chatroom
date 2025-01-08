import socketio

sio_server = socketio.AsyncServer(
    async_mode='asgi',
    cors_allowed_origins=[]
)

sio_app = socketio.ASGIApp(
    socketio_server=sio_server,
    socketio_path='sockets/socket.io'
)


@sio_server.event
async def connect(sid, environ, auth):
    print(f'{sid}: connected')
    await sio_server.emit('join', {'sid': sid})

@sio_server.event
async def message(sid, data):
    print(f"Received message from {sid}: {data}")
    # Broadcast the message to all clients
    await sio_server.emit('message', {
        'client': data['client'],
        'message': data['content'],
        'timestamp': data['timestamp']
    })


@sio_server.event
async def chat(sid, message):
    await sio_server.emit('chat', {'sid': sid, 'message': message})


@sio_server.event
async def disconnect(sid):
    print(f'{sid}: disconnected')