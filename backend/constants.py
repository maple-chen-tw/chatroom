import os
from dotenv import load_dotenv

env = os.getenv("APP_ENV", "development")
env_file = f".env.{env}"
print(f"[ENV] Loading environment from {env_file}")
load_dotenv(dotenv_path=env_file)

# APP settings
HOST = os.getenv("HOST", "127.0.0.1")
PORT = int(os.getenv("PORT", "8000"))

# CORS origins
ALLOWED_ORIGINS = [origin.strip() for origin in os.getenv("ALLOWED_ORIGINS", "").split(",")]

# JWT & Security
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "120"))

# DB
DB_CONNECTION_STRING = os.getenv("DB_CONNECTION_STRING")

# AWS s3 bucket for static
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION")
S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")