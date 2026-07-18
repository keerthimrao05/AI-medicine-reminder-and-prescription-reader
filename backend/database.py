from pymongo import MongoClient
from config import Config

try:
    client = MongoClient(Config.MONGO_URI)

    # Test the connection
    client.admin.command("ping")

    print("✅ MongoDB Atlas Connected Successfully!")

    db = client[Config.DATABASE_NAME]

except Exception as e:
    print("❌ MongoDB Connection Failed")
    print(e)