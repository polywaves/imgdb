from app.mongo import posts_collection, post_image_ids_collection, vector_hashes_collection
from app.utils.logger_util import logger
from app.utils.text_util import urldecode
from bson.objectid import ObjectId
from datetime import datetime, timedelta

## Make migrations
async def run():
  await fix()

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



async def fix():
  rows = await post_image_ids_collection.find({
    "created_at": None
  }).to_list()

  for row in rows:
    timestamp = row["_id"].generation_time.timestamp()
    id = row["id"]

    await post_image_ids_collection.update_one({
      "_id": row["_id"]
    }, {
      "$set": {
        "created_at": timestamp
      }
    })

    logger.info(f"timestamp {timestamp} for {id} updated")


