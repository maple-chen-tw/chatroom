import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.sockets.sockets import sio_app
from app.controllers import auth_controller
from app.controllers import user_controller
from app.controllers import friend_controller
from app.controllers import chatroom_controller
from app.controllers import upload_controller
from fastapi import UploadFile, File, HTTPException
from fastapi.staticfiles import StaticFiles


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    # allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount('/ws', app=sio_app)

app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(upload_controller.router)

app.include_router(auth_controller.router)
app.include_router(user_controller.router)
app.include_router(friend_controller.router)
app.include_router(chatroom_controller.router)


@app.get('/')
async def home():
    return {'message': 'Hello👋 Developers💻'}


if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)