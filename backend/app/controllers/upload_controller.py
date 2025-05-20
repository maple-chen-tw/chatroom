
from fastapi import APIRouter, UploadFile, File, Request, HTTPException
import os
import uuid
import boto3
from constants import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION, S3_BUCKET_NAME

router = APIRouter(
    prefix="/upload",
    tags=["Upload"]
)

# 初始化 S3 客戶端
s3_client = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION
)

@router.post("/upload-avatar")
async def upload_avatar(request: Request, file: UploadFile = File(...)):
    # 允許的副檔名
    allowed_extensions = ["image/jpeg", "image/png", "image/webp"]
    if file.content_type not in allowed_extensions:
        raise HTTPException(status_code=400, detail="Unsupported file type")

    # 3. 隨機檔名避免衝突
    file_ext = file.filename.split(".")[-1]
    file_name = f"{uuid.uuid4()}.{file_ext}"

    # 4. 儲存圖片
    if os.getenv("APP_ENV") == "development":
        save_path = f"static/avatars/{file_name}"
        os.makedirs("static/avatars", exist_ok=True)
        with open(save_path, "wb") as f:
            content = await file.read()
            f.write(content)
        file_url = f"{str(request.base_url)}static/avatars/{file_name}"
    else:
        # 生產環境：儲存到 AWS S3
        save_path = file_name  # 不需要路徑，S3 本身會管理結構
        s3_client.upload_fileobj(file.file, S3_BUCKET_NAME, save_path)
        file_url = f"https://{S3_BUCKET_NAME}.s3.{AWS_REGION}.amazonaws.com/{save_path}"

    # 5. 回傳可公開存取的 URL
    return {"url": file_url}

@router.post("/upload-message-file")
async def upload_chatroom(request: Request, file: UploadFile = File(...)):
    # 允許的副檔名
    allowed_extensions = {
        "image/jpeg": "image",
        "image/png": "image",
        "image/webp": "image",
        "audio/mpeg": "audio",
        "audio/mp3": "audio",
        "application/pdf": "file",
        "video/mp4": "video"
    }
    if file.content_type not in allowed_extensions:
        raise HTTPException(status_code=400, detail="Unsupported file type")

    # 3. 隨機檔名避免衝突
    file_ext = file.filename.split(".")[-1]
    file_name = f"{uuid.uuid4()}.{file_ext}"
    

    # 4. 儲存圖片
    if os.getenv("APP_ENV") == "development":
        save_path = f"static/message/{file_name}"
        os.makedirs("static/message", exist_ok=True)
        with open(save_path, "wb") as f:
            content = await file.read()
            f.write(content)
        file_url = f"{str(request.base_url)}static/message/{file_name}"
    else:
        # 生產環境：儲存到 AWS S3
        save_path = file_name
        s3_client.upload_fileobj(file.file, S3_BUCKET_NAME, save_path)
        file_url = f"https://{S3_BUCKET_NAME}.s3.{AWS_REGION}.amazonaws.com/{save_path}"

    # 5. 回傳可公開存取的 URL
    file_type = allowed_extensions[file.content_type]
    return {
        "url": file_url,
        "message_type": file_type
    }