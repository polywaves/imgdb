import hashlib
import json
from time import time
from datetime import datetime, timedelta
from fastapi import APIRouter, UploadFile, File
from app.providers import weaviate_provider
from app.models import vector_model
from app.utils import image_util
from app import mongo
from app.utils.logger_util import logger
from app.utils import response_util
from app.utils import text_util

router = APIRouter()


async def search_posts(image: str) -> dict:
  vectors = weaviate_provider.search_near_image(image=image, limit=150)

  ## Make distances and fix data
  data = dict()
  for vector in vectors.objects:
    distance = round(vector.metadata.distance, 6)
    post_id = vector.properties["post_id"]

    post = await mongo.posts_collection.find_one({
      "id": str(post_id)
    })

    if not post:
      continue

    post["distance"] = distance
    vendor_id = post["vendor_id"]
    price = post["price"]

    id = f"{distance}:{price}:{vendor_id}"

    if id not in data:
      data[id] = post

    ## Replace to greater fresh post
    if id in data and data[id]["creation_timestamp"] < post["creation_timestamp"]:
      data[id] = post


  data = dict(sorted(data.items()))

  response = list()
  count = 0
  for post in data.values():
    count += 1

    if count > 30:
      break

    # Fix post data
    del post["_id"]
    del post["creation_date"]
    del post["creation_timestamp"]
    del post["created_at"]

    if not post["video"]:
      del post["video"]
    
    response.append(post)

  return response
              

async def delete_posts(post_ids: list):
  deleted = list()
  for post_id in post_ids:
    post_id = post_id.strip()

    try:
      weaviate_provider.delete_images_by_post_id(post_id=int(post_id))

      await mongo.vector_hashes_collection.delete_many({
        "post_id": str(post_id)
      })
      await mongo.post_image_ids_collection.delete_many({
        "post_id": str(post_id)
      })
      await mongo.posts_collection.delete_many({
        "id": str(post_id)
      })

      deleted.append(post_id)
    except Exception as e:
      logger.error(e)

  return deleted


@router.get("/old_posts", tags=["Get old posts"])
async def old_posts(limit: int = 100, days: int = 23):
  start_time = time()

  items = await mongo.posts_collection.find({
    "creation_timestamp": {
      "$lt": (datetime.now() - timedelta(days=days)).timestamp()
    }
  }, {
    "id": 1,
    "creation_date": 1
  }).sort("creation_timestamp", 1).limit(limit).to_list()

  posts = list()
  for item in items:
    del item["_id"]

    posts.append(item)

  return response_util.response({
    "result": 1,
    "posts": posts
  }, start_time=start_time)


@router.get("/delete_posts_by_ids", tags=["Delete post and image vectors by post ids throught ,"])
async def delete_posts_by_ids(post_ids: str):
  start_time = time()

  deleted = await delete_posts(post_ids=post_ids.split(','))

  return response_util.response({
    "result": 1,
    "deleted": deleted
  }, start_time=start_time)
  

@router.post("/delete_posts_by_ids", tags=["Delete post and image vectors by post ids"])
async def delete_posts_by_ids(params: vector_model.DeletePostsByIds):
  start_time = time()

  deleted = await delete_posts(post_ids=params.post_ids)
  
  return response_util.response({
    "result": 1,
    "deleted": deleted
  }, start_time=start_time)


@router.post("/search_by_url", tags=["Search near vectors by existing url"])
async def search_by_url(url: str):
  start_time = time()

  posts = list()

  try:
    image = image_util.from_url_to_base64(url)
    posts = await search_posts(image=image)
  except Exception as e:
    logger.debug(e)

  return response_util.response({
    "result": 1,
    "posts": posts
  }, start_time=start_time)


@router.get("/search_by_img_id", tags=["Search near vectors by existing img id"])
async def search_by_img_id(img_id: int):
  start_time = time()

  post = await mongo.posts_collection.find_one({
    "images.img_id": int(img_id)
  })

  if not post:
    return response_util.response({
      "result": 1,
      "posts": []
    }, start_time=start_time)

  posts = list()
  for image in post["images"]:
    if image["img_id"] == img_id:
      try:
        image = image_util.from_url_to_base64(image["img"])
        posts = await search_posts(image=image)
      except Exception as e:
        logger.debug(e)

  return response_util.response({
    "result": 1,
    "posts": posts
  }, start_time=start_time)


@router.post("/search_by_upload", tags=["Search near vectors by uploading image"])
async def search_by_upload(image: UploadFile = File()):
  start_time = time()

  posts = list()

  try:
    image = image_util.to_base64(await image.read())
    posts = await search_posts(image=image)
  except Exception as e:
    logger.debug(e)

  return response_util.response({
    "result": 1,
    "posts": posts
  }, start_time=start_time)
  

@router.post("/training", tags=["Training by json"])
async def training_by_json(params: vector_model.TrainingByJson):
  start_time = time()

  items = list()
  images = list()
  for image in params.images:
    logger.info(image.img)

    items.append({
      "image": image_util.from_url_to_base64(image.img),
      "uid": int(image.img_id),
      "post_id": int(params.id)
    })

    options = dict()
    images.append({
      "img_id": image.img_id,
      "options": options
    })

  await delete_posts(post_ids=[params.id])

  ## Vectorize image
  failed_objects = weaviate_provider.create_image_vector(items=items)
  logger.info(failed_objects)

  ## Decode data
  params.vendor_capt = text_util.urldecode(params.vendor_capt)
  params.by = text_util.urldecode(params.by)
  params.item_name = text_util.urldecode(params.item_name)
  params.text = text_util.urldecode(params.text)

  options = list()
  for option in params.options:
    options.append(text_util.urldecode(option))
  params.options = options

  sizes = list()
  for size in params.sizes:
    sizes.append(text_util.urldecode(size))
  params.sizes = sizes

  post = params.model_dump()
  post["created_at"] = time()

  posted = post["posted"]
  creation_date = datetime.strptime(f"{posted}.{datetime.now().strftime('%y')}", "%d.%m.%y")
  post["creation_date"] = creation_date.strftime("%d.%m.%y")
  post["creation_timestamp"] = creation_date.timestamp()

  await mongo.posts_collection.insert_one(post)

  insert_image_ids = list()
  for image in post["images"]:
    insert_image_ids.append({
      "id": image["img_id"],
      "post_id": params.id,
      "created_at": time()
    })

  try:
    await mongo.post_image_ids_collection.insert_many(insert_image_ids)
  except Exception as e:
    logger.debug(e)

  vectors = weaviate_provider.get_image_vectors_by_post_id(post_id=int(params.id))

  hashes = list()
  for object in vectors.objects:
    vector = object.vector["default"]
    dump = json.dumps(vector).encode('utf-8')
    data_md5 = hashlib.md5(dump).hexdigest()
    uid = object.properties["uid"]
    post_id = object.properties["post_id"]

    hashes.append({
      "img_id": uid,
      "post_id": str(post_id),
      "hash": data_md5,
      "created_at": time()
    })
  
  try:
    await mongo.vector_hashes_collection.insert_many(hashes)
  except Exception as e:
    logger.debug(e)

  return response_util.response({
    "result": 1,
    "post_id": params.id,
    "images": images
  }, start_time=start_time)
