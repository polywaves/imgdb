from app.mongo import posts_collection, post_image_ids_collection, vector_hashes_collection
from app.utils.logger_util import logger
from app.utils.text_util import urldecode
from bson.objectid import ObjectId
from datetime import datetime, timedelta

## Make migrations
async def run():
  await fix_posts()


async def fix_posts():
  rows = await posts_collection.find({
    "creation_timestamp": {
      "$exists": False
    }
  }, {
    "id": 1,
    "creation_date": 1
  }).to_list()

  for row in rows:
    id = row["id"]
    creation_timestamp = datetime.strptime(row["creation_date"], "%d.%m.%y").timestamp()

    await posts_collection.update_one({
      "_id": row["_id"]
    }, {
      "$set": {
        "creation_timestamp": creation_timestamp
      }
    })

    logger.info(f"creation timestamp {creation_timestamp} for post id {id} updated")


