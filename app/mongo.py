import os
from motor import motor_asyncio
from pymongo import IndexModel, ASCENDING, DESCENDING

client = motor_asyncio.AsyncIOMotorClient(os.environ["MONGO_URL"])
db = client.get_database(os.environ["MONGO_DB"])

posts_collection = db.get_collection("posts")
post_image_ids_collection = db.get_collection("post_image_ids")
requests_collection = db.get_collection("requests")
vector_hashes_collection = db.get_collection("vector_hashes")

## Make migrations
async def migrate():
  await posts_collection.create_index("id")
  await posts_collection.create_index("images.img_id")

  await post_image_ids_collection.create_index("id", unique=True)
  await post_image_ids_collection.create_index("post_id")

  await vector_hashes_collection.create_index("hash", unique=True)
  await vector_hashes_collection.create_index("post_id")