import os
from motor import motor_asyncio
from pymongo import IndexModel, ASCENDING, DESCENDING

client = motor_asyncio.AsyncIOMotorClient(os.environ["MONGO_URL"])
db = client.get_database(os.environ["MONGO_DB"])

posts_collection = db.get_collection("posts")
post_image_ids_collection = db.get_collection("post_image_ids")
requests_collection = db.get_collection("requests")

## Make migrations
async def migrate():
  posts_indexes = [
    IndexModel([("id", DESCENDING)]),
    IndexModel([("images.img_id", DESCENDING)])
  ]

  await posts_collection.create_indexes(posts_indexes)
  await post_image_ids_collection.create_index("id", unique=True)