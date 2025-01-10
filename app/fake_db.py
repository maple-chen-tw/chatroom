# app/db.py
from datetime import datetime
fake_users_db = {
    "johndoe": {
        "user_id": 1,
        "username": "johndoe",
        "email": "johndoe@example.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "nickname": "John",
        "avatar_url":"",
        "status": "Living the dream",
        "created_at": datetime(2020, 1, 1, 12, 0, 0), 
        "updated_at": datetime(2023, 1, 1, 12, 0, 0),
    }
}
