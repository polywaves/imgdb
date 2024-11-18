from time import time
from fastapi import APIRouter
from app import mongo
from app.utils.logger_util import logger
from app.utils import response_util
from app.utils.text_util import date_format
from app.providers import weaviate_provider

router = APIRouter()


# logger.info(weaviate_provider.get_count_of_unique_uids())


@router.get("/uni_vectors", tags=["Get count of uniq vectors"])
async def uni_vectors():
  start_time = time()

  result = 0

  return response_util.response({
    "result": 1, 
    "data": [
      {
        "rkey": time(),
        "dt": date_format(),
        "val1": result
      }
    ]
  }, start_time=start_time)
  

@router.get("/uni_ids", tags=["Get count of uniq image ids"])
async def uni_ids():
  start_time = time()

  result = await mongo.post_image_ids_collection.count_documents({})

  return response_util.response({
    "result": 1,
    "data": [
      {
        "rkey": time(),
        "dt": date_format(),
        "val1": result
      }
    ]
  }, start_time=start_time)
  

@router.get("/uni_posts", tags=["Get count of uniq post ids"])
async def uni_posts():
  start_time = time()

  result = await mongo.posts_collection.count_documents({})

  return response_util.response({
    "result": 1,
    "data": [
      {
        "rkey": time(),
        "dt": date_format(),
        "val1": result
      }
    ]
  }, start_time=start_time)


@router.get("/hour_requests", tags=["Get count of last hour requests"])
async def hour_requests():
  start_time = time()

  result = await mongo.requests_collection.count_documents({
    "created_at": {
      "$gt": time() - (3600 * 1000)
    }
  })

  return response_util.response({
    "result": 1,
    "data": [
      {
        "rkey": time(),
        "dt": date_format(),
        "val1": result
      }
    ]
  }, start_time=start_time)
  

@router.get("/day_requests", tags=["Get count of last 24h requests"])
async def day_requests():
  start_time = time()

  result = await mongo.requests_collection.count_documents({
    "created_at": {
      "$gt": time() - (86400 * 1000)
    }
  })

  return response_util.response({
    "result": 1,
    "data": [
      {
        "rkey": time(),
        "dt": date_format(),
        "val1": result
      }
    ]
  }, start_time=start_time)


@router.get("/week_requests", tags=["Get count of last week requests"])
async def week_requests():
  start_time = time()

  result = await mongo.requests_collection.count_documents({
    "created_at": {
      "$gt": time() - (86400 * 7 * 1000)
    }
  })

  return response_util.response({
    "result": 1,
    "data": [
      {
        "rkey": time(),
        "dt": date_format(),
        "val1": result
      }
    ]
  }, start_time=start_time)


@router.get("/usage", tags=["Get current usage of cpu and gpu"])
async def usage():
  start_time = time()

  result = 0

  return response_util.response({
    "result": 1,
    "data": [
      {
        "rkey": time(),
        "dt": date_format(),
        "val1": result
      }
    ]
  }, start_time=start_time)
