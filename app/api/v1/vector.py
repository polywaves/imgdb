import time
from urllib.parse import unquote
from fastapi import APIRouter, HTTPException, UploadFile, File
from app.providers import weaviate_provider
from app.models import vector_model
from app.utils import image_util
from app.mongo import db
from app.utils.logger_util import logger
from app.utils import response_util

router = APIRouter()


try:
  weaviate_provider.create_collection()
except Exception as e:
  logger.debug(e)


posts_collection = db.get_collection("posts")
# await posts_collection.create_index("user_id", unique=True)

# logger.info(weaviate_provider.get_count_of_unique_uids())

async def search_posts(image: str) -> dict:
  vectors = weaviate_provider.search_near_image(image=image, limit=30)

  response = list()
  post_ids = []
  for vector in vectors:
    distance = vector.metadata.distance
    uid = vector.properties["uid"]

    post = await posts_collection.find_one({
      "images.img_id": int(uid)
    })

    if not post:
      continue

    if post["id"] not in post_ids:
      post_ids.append(post["id"])

      del post["_id"]
      post["distance"] = round(distance, 6)
      response.append(post)

  return response


async def delete_posts(post_ids: list):
  deleted = []
  for post_id in post_ids:
    post_id = post_id.strip()

    try:
      post = await posts_collection.find_one({
        "id": post_id
      })

      for image in post["images"]:
        try:
          weaviate_provider.delete_image_by_uid(uid=int(image["img_id"]))
        except Exception:
          logger.debug(f"Vector uid {image.img_id} not found")

      await posts_collection.delete_one({
        "id": post_id
      })

      deleted.append(post_id)
    except Exception as e:
      logger.error(e)

  return deleted


@router.get("/delete_posts_by_ids", tags=["Delete post and image vectors by post ids throught ,"])
async def delete_posts_by_ids(post_ids: str):
  start_time = time.time()

  deleted = await delete_posts(post_ids=post_ids.split(','))

  return response_util.response({
    "status": 1,
    "deleted": deleted
  }, start_time=start_time)
  

@router.post("/delete_posts_by_ids", tags=["Delete post and image vectors by post ids"])
async def delete_posts_by_ids(params: vector_model.DeletePostsByIds):
  start_time = time.time()

  deleted = await delete_posts(post_ids=params.post_ids)
  
  return response_util.response({
    "status": 1,
    "deleted": deleted
  }, start_time=start_time)


@router.post("/search_by_url", tags=["Search near vectors by url"])
async def search_by_url(url: str):
  start_time = time.time()

  image = image_util.from_url_to_base64(url)
  posts = await search_posts(image=image)

  return response_util.response({
    "status": 1,
    "posts": posts
  }, start_time=start_time)


@router.get("/search_by_img_id", tags=["Search near vectors by existing img id"])
async def search_by_img_id(img_id: int):
  start_time = time.time()

  post = await posts_collection.find_one({
    "images.img_id": int(img_id)
  })

  if not post:
    return response_util.response({
      "status": 1,
      "posts": []
    }, start_time=start_time)

  posts = list()
  for image in post["images"]:
    if image["img_id"] == img_id:
      image = image_util.from_url_to_base64(image["img"])
      posts = await search_posts(image=image)

  return response_util.response({
    "status": 1,
    "posts": posts
  }, start_time=start_time)


@router.post("/search_by_upload", tags=["Search near vectors by uploading image"])
async def search_by_upload(image: UploadFile = File()):
  start_time = time.time()

  image = image_util.to_base64(await image.read())
  posts = await search_posts(image=image)

  return response_util.response({
    "status": 1,
    "posts": posts
  }, start_time=start_time)
  

@router.post("/training", tags=["Training by json"])
async def training_by_json(params: vector_model.TrainingByJson):
  start_time = time.time()

  items = list()
  images = list()
  for image in params.images:
    try:
      weaviate_provider.delete_image_by_uid(uid=int(image.img_id))
    except Exception:
      logger.debug(f"Vector uid {image.img_id} not found")

    items.append({
      "image": image_util.from_url_to_base64(image.img),
      "uid": int(image.img_id)
    })

    options = dict()
    images.append({
      "img_id": image.img_id,
      "options": options
    })

  await posts_collection.delete_one({
    "id": params.id
  })

  ## Decode texts
  params.by = unquote(params.by)
  params.item_name = unquote(params.item_name)
  params.text = unquote(params.text)

  options = list()
  for option in params.options:
    options.append(unquote(option))
  params.options = options

  post = params.model_dump()

  await posts_collection.insert_one(post)
  weaviate_provider.create_image_vector(items=items)

  return response_util.response({
    "status": 1,
    "post_id": params.id,
    "images": images
  }, start_time=start_time)

