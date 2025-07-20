from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URL = os.getenv("MONGO_URL")

# Ensure you enable TLS for Atlas
client = AsyncIOMotorClient(MONGO_URL, tls=True)
db = client["ecommerce"]
