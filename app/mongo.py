import os
from motor import motor_asyncio

client = motor_asyncio.AsyncIOMotorClient(os.environ["MONGO_URL"])
db = client.get_database(os.environ["MONGO_DB"])