from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from app.providers import weaviate_provider
from app.utils import image_util
from app.utils.logger_util import logger

router = APIRouter()


try:
  weaviate_provider.create_collection()
except Exception as e:
  logger.debug(e)


@router.get("/delete_by_uid", tags=["Delete image vector by uid"])
async def delete_by_uid(uid: int):
  try:
    weaviate_provider.delete_image_by_uid(uid=uid)

    return {
      "detail": f"Image vector deleted successfully"
    }
  except Exception as e:
    logger.error(e)
    raise HTTPException(status_code=500, detail=str(e))
  

@router.get("/search", tags=["Search near vectors by url"])
async def search_by_url(url: str):
  try:
    image = image_util.from_url_to_base64(url)
    response = weaviate_provider.search_near_image(image=image)

    return {
      "data": response
    }
  except Exception as e:
    logger.error(e)
    raise HTTPException(status_code=500, detail=str(e))
  

@router.post("/search", tags=["Search near vectors by uploading image"])
async def search_by_upload(image: UploadFile = File()):
  try:
    image = image_util.to_base64(await image.read())
    response = weaviate_provider.search_near_image(image=image)

    return {
      "data": response
    }
  except Exception as e:
    logger.error(e)
    raise HTTPException(status_code=500, detail=str(e))
  

@router.get("/training", tags=["Training by image url"])
async def training_by_url(url: str, uid: int):
  try:
    items = list()
    items.append({
      "image": image_util.from_url_to_base64(url),
      "uid": uid,
      "data": {
        "url": url
      }
    })

    weaviate_provider.create_image_vector(items=items)

    return {
      "detail": f"Image vector created successfully"
    }
  except Exception as e:
    logger.error(e)
    raise HTTPException(status_code=500, detail=str(e))
  

@router.post("/training", tags=["Training by uploading image"])
async def training_by_upload(
  uid: int = Form(),
  image: UploadFile = File()
):
  try:
    items = list()
    items.append({
      "image": image_util.to_base64(await image.read()),
      "uid": uid,
      "data": {
        "url": image.filename
      }
    })

    weaviate_provider.create_image_vector(items=items)

    return {
      "detail": f"Image vector created successfully"
    }
  except Exception as e:
    logger.error(e)
    raise HTTPException(status_code=500, detail=str(e))  
