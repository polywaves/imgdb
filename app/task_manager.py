from app.mongo import posts_collection
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
  posts = await posts_collection.find().limit(100).to_list()

  for post in posts:
    # await posts_collection.update_one({
    #   "_id": post["_id"]
    # }, {
    #   "$set": {
    #     "sizes": sizes
    #   }
    # })

    logger.info(post["_id"].generation_time.timestamp())


