from app.mongo import posts_collection, post_image_ids_collection, vector_hashes_collection
from app.utils.logger_util import logger
from app.utils.text_util import urldecode
from bson.objectid import ObjectId
from datetime import datetime, timedelta

## Make migrations
async def run():
  await fix(posts_collection, repr={
    "id": 1,
    "posted": 1
  })



async def fix(collection, repr: dict):
  rows = await collection.find({
    "creation_date": {
      "$exists": False
    }
  }, repr).limit(10).to_list()

  for row in rows:
    posted = row["posted"]
    creation_date = datetime.strptime(f"{posted}.{datetime.now().strftime('%y')}", "%d.%m.%y")

    await collection.update_one({
      "_id": row["_id"]
    }, {
      "$set": {
        "creation_date": creation_date
      }
    })

    logger.info(f"creation date {creation_date} for {id} updated")


