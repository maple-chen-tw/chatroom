from sqlalchemy import create_engine
from app.models.db import Base
from constants import DB_CONNECTION_STRING

db_url = DB_CONNECTION_STRING
engine = create_engine(db_url)

def init_db():
    print("🔧 Creating tables...")
    Base.metadata.create_all(engine)
    print("✅ Tables created.")

if __name__ == "__main__":
    init_db()
