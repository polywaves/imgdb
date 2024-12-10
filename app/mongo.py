import os
from motor import motor_asyncio
from pymongo import IndexModel, ASCENDING, DESCENDING
from app.utils.logger_util import logger

client = motor_asyncio.AsyncIOMotorClient(os.environ["MONGO_URL"])
db = client.get_database(os.environ["MONGO_DB"])

posts_collection = db.get_collection("posts")
post_image_ids_collection = db.get_collection("post_image_ids")
requests_collection = db.get_collection("requests")
vector_hashes_collection = db.get_collection("vector_hashes")

## Make migrations
async def migrate():
  try:
    posts_indexes = [
      IndexModel([("id", ASCENDING)]),
      IndexModel([("images.img_id", ASCENDING)]),
      IndexModel([("images.img", ASCENDING)]),
      IndexModel([("created_at", ASCENDING)]),
      IndexModel([("creation_date", ASCENDING)]),
      IndexModel([("creation_timestamp", ASCENDING)]),
    ]
    await posts_collection.create_indexes(posts_indexes)

    await post_image_ids_collection.create_index("id", unique=True)
    await post_image_ids_collection.create_index("post_id")
    await post_image_ids_collection.create_index("created_at")

    await vector_hashes_collection.create_index("hash", unique=True)
    await vector_hashes_collection.create_index("post_id")
    await vector_hashes_collection.create_index("img_id")
    await vector_hashes_collection.create_index("created_at")

    await requests_collection.create_index("url")
    await requests_collection.create_index("created_at")
  except Exception as e:
    logger.debug(e)


