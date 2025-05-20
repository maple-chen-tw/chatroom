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
from fastapi.responses import StreamingResponse
from constants import ALLOWED_ORIGINS, HOST, PORT
import boto3
from constants import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION, S3_BUCKET_NAME
import os

app = FastAPI()

s3_client = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount('/ws', app=sio_app)

if os.getenv("APP_ENV") == "development":
    app.mount("/static", StaticFiles(directory="static"), name="static")
else:
    @app.get("/static/{file_path:path}")
    async def get_static_file(file_path: str):
        try:
            # 從 S3 下載檔案
            response = s3_client.get_object(Bucket=S3_BUCKET_NAME, Key=file_path)
            file_stream = response['Body']
            return StreamingResponse(file_stream, media_type="application/octet-stream")
        except s3_client.exceptions.NoSuchKey:
            return {"error": "File not found"}

app.include_router(upload_controller.router)
app.include_router(auth_controller.router)
app.include_router(user_controller.router)
app.include_router(friend_controller.router)
app.include_router(chatroom_controller.router)


@app.get('/')
async def home():
    return {'message': 'Hello👋 Developers💻'}


if __name__ == '__main__':
    if os.getenv("APP_ENV", "development") == "development":
        uvicorn.run("main:app", host=HOST, port=PORT, reload=True)
    else:
        uvicorn.run("main:app", host=HOST, port=PORT)