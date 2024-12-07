from app.mongo import posts_collection, post_image_ids_collection, vector_hashes_collection
from app.utils.logger_util import logger
from app.utils.text_util import urldecode
from bson.objectid import ObjectId
from datetime import datetime, timedelta

## Make migrations
async def run():
  await fix(posts_collection)
  await fix(post_image_ids_collection)
  await fix(vector_hashes_collection, id_key="img_id")

  # # Rewinding posts
  # posts = await posts_collection.find({
  #   "sizes": {
  #     "$regex": "%"
  #   }
  # }).to_list()

  # for post in posts:
  #   sizes = list()
  #   for size in post["sizes"]:
  #     sizes.append(urldecode(size))

  #   await posts_collection.update_one({
  #     "_id": post["_id"]
  #   }, {
  #     "$set": {
  #       "sizes": sizes
  #     }
  #   })

  #   logger.info(sizes)



async def fix(collection, id_key: str = "id"):
  rows = await collection.find({
    "created_at": {
      "$exists": False
    }
  }, {
    id_key: 1
  }).to_list()

  for row in rows:
    timestamp = row["_id"].generation_time.timestamp()
    id = row[id_key]

    await collection.update_one({
      "_id": row["_id"]
    }, {
      "$set": {
        "created_at": timestamp
      }
    })

    logger.info(f"timestamp {timestamp} for {id} updated")


