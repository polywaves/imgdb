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
    "creation_date": {
      "$exists": False
    }
  }, {
    "id": 1,
    "posted": 1
  }).to_list()

  for row in rows:
    id = row["id"]
    posted = row["posted"]
    creation_date = datetime.strptime(f"{posted}.{datetime.now().strftime('%y')}", "%d.%m.%y").strftime("%d.%m.%y")

    await posts_collection.update_one({
      "_id": row["_id"]
    }, {
      "$set": {
        "creation_date": creation_date
      }
    })

    logger.info(f"creation date {creation_date} for post id {id} updated")


