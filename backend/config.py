import os
from dotenv import load_dotenv

load_dotenv()

class Config:

    MONGO_URI = os.getenv("MONGO_URI")

    DATABASE_NAME = os.getenv("DATABASE_NAME")

    JWT_SECRET = os.getenv("JWT_SECRET")

    UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER")