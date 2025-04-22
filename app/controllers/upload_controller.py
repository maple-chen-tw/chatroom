
from fastapi import APIRouter, UploadFile, File, Request, HTTPException
import os
import uuid

router = APIRouter(
    prefix="/upload",
    tags=["Upload"]
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
    save_path = f"static/avatars/{file_name}"

    # 4. 儲存圖片
    os.makedirs("static/avatars", exist_ok=True)
    with open(save_path, "wb") as f:
        content = await file.read()
        f.write(content)

    # 5. 回傳可公開存取的 URL
    base_url = str(request.base_url)
    return {"url": f"{base_url}static/avatars/{file_name}"}

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
    save_path = f"static/message/{file_name}"

    # 4. 儲存圖片
    os.makedirs("static/message", exist_ok=True)
    with open(save_path, "wb") as f:
        content = await file.read()
        f.write(content)

    # 5. 回傳可公開存取的 URL
    base_url = str(request.base_url)
    file_type = allowed_extensions[file.content_type]
    file_url = f"{base_url}static/message/{file_name}"
    
    return {
        "url": file_url,
        "message_type": file_type
    }