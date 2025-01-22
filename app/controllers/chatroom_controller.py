from fastapi import HTTPException, status, APIRouter
from fastapi import Path
from app.models import db
from app.models import dto
from app.services import friend_service
from utils import dependencies
router = APIRouter(
    prefix="/chatrooms",
    tags=["Chatrooms"],
)

@router.get("/chatrooms")
def get_chatrooms(user: dependencies.user_dependency):
    return

@router.post("/chatrooms", response_model=None)
def add_chatroom(chatroom_id: int, members_id: list[int], user: dependencies.user_dependency) -> None:
    return


@router.get("/chatrooms/{chatroom_id}", response_model=None)
def get_chatroom(chatroom_id:int, user: dependencies.user_dependency) -> None:
    return

@router.post("/chatrooms/{chatroom_id}", response_model=None)
def update_chatroom(chatroom_id:int, user: dependencies.user_dependency) -> None:
    return