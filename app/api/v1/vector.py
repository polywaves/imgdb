from fastapi import APIRouter, HTTPException, UploadFile, File
from app.providers import weaviate_provider
from app.models import vector_model
from app.utils import image_util
from app.mongo import db
from app.utils.logger_util import logger

router = APIRouter()


try:
  weaviate_provider.create_collection()
except Exception as e:
  logger.debug(e)


posts_collection = db.get_collection("posts")
# await posts_collection.create_index("user_id", unique=True)

async def search_posts(image: str) -> dict:
  vectors = weaviate_provider.search_near_image(image=image, limit=30)

  response = list()
  post_ids = []
  for vector in vectors:
    distance = vector.metadata.distance
    uid = vector.properties["uid"]

    post = await posts_collection.find_one({
      "images.img_id": uid
    })

    if post["id"] not in post_ids:
      post_ids.append(post["id"])

      images = list()
      for image in post["images"]:
        item = {
          "img_id": image["img_id"],
          "options": {
            "img": image["img"],
            "sizes": image["sizes"]
          }
        }

        images.append(item)

      response.append({
        "post_id": post["id"],
        "distance": distance,
        "images": images
      })

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
        weaviate_provider.delete_image_by_uid(uid=int(image["img_id"]))

      await posts_collection.delete_one({
        "id": post_id
      })

      deleted.append(post_id)
    except Exception as e:
      logger.error(e)

  return deleted


@router.get("/delete_posts_by_ids", tags=["Delete post and image vectors by post ids throught ,"])
async def delete_posts_by_ids(post_ids: str):
  deleted = await delete_posts(post_ids=post_ids.split(','))
  
  return {
    "deleted": deleted
  }
  

@router.post("/delete_posts_by_ids", tags=["Delete post and image vectors by post ids"])
async def delete_posts_by_ids(params: vector_model.DeletePostsByIds):
  deleted = await delete_posts(post_ids=params.post_ids)
  
  return {
    "deleted": deleted
  }


@router.get("/search", tags=["Search near vectors by url"])
async def search_by_url(url: str):
  image = image_util.from_url_to_base64(url)
  response = await search_posts(image=image)

  return {
    "data": response
  }


@router.post("/search", tags=["Search near vectors by uploading image"])
async def search_by_upload(image: UploadFile = File()):
  image = image_util.to_base64(await image.read())
  response = await search_posts(image=image)

  return {
    "data": response
  }
  

@router.post("/training", tags=["Training by json"])
async def training_by_json(params: vector_model.TrainingByJson):
  items = list()
  for image in params.images:
    items.append({
      "image": image_util.from_url_to_base64(image.img),
      "uid": int(image.img_id)
    })

  await posts_collection.insert_one(params.model_dump())

  weaviate_provider.create_image_vector(items=items)

  return {
    "detail": f"Image vector created successfully"
  }

