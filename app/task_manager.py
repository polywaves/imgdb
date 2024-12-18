from app.mongo import posts_collection, post_image_ids_collection, vector_hashes_collection
from app.utils.logger_util import logger
from datetime import datetime

## Make migrations
async def run():
  await fix_posts()


async def fix_post_image_ids():
  rows = await post_image_ids_collection.find({
    "created_at": {
      "$exists": False
    }
  }, {
    "id": 1
  }).to_list()

  for row in rows:
    id = row["id"]
    created_at = row["_id"].generation_time

    await post_image_ids_collection.update_one({
      "_id": row["_id"]
    }, {
      "$set": {
        "created_at": created_at
      }
    })

    logger.info(f"created at {created_at} for post_image_ids id {id} updated")


async def fix_vector_hashes():
  rows = await vector_hashes_collection.find({
    "created_at": {
      "$exists": False
    }
  }, {
    "id": 1
  }).to_list()

  for row in rows:
    id = row["id"]
    created_at = row["_id"].generation_time

    await vector_hashes_collection.update_one({
      "_id": row["_id"]
    }, {
      "$set": {
        "created_at": created_at
      }
    })

    logger.info(f"created at {created_at} for vector_hashes id {id} updated")


async def fix_posts():
  rows = await posts_collection.find({
    "creation_timestamp": {
      "$exists": False
    }
  }, {
    "id": 1,
    "posted": 1
  }).to_list()

  for row in rows:
    id = row["id"]
    posted = row["posted"]
    creation_date = datetime.strptime(f"{posted}.{datetime.now().strftime('%y')}", "%d.%m.%y")
    creation_timestamp = creation_date.timestamp()
    created_at = row["_id"].generation_time

    await posts_collection.update_one({
      "_id": row["_id"]
    }, {
      "$set": {
        "creation_timestamp": creation_timestamp,
        "created_at": created_at
      }
    })

    logger.info(f"creation timestamp {creation_timestamp} and created at {created_at} for posts id {id} updated")


