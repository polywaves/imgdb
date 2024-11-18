from time import time
from datetime import datetime, timedelta
from fastapi import APIRouter
from app import mongo
from app.utils.logger_util import logger
from app.utils import response_util
from app.utils.text_util import dt_format, rkey_format
from app.providers import weaviate_provider
from app.utils import usage_util

router = APIRouter()


# logger.info(weaviate_provider.get_count_of_unique_uids())


@router.get("/uni_vectors", tags=["Get count of unique vectors"])
async def uni_vectors():
  start_time = time()

  val1 = await mongo.vector_hashes_collection.count_documents({})

  return response_util.response({
    "result": 1, 
    "data": [
      {
        "rkey": rkey_format(),
        "dt": dt_format(),
        "val1": str(val1)
      }
    ]
  }, start_time=start_time)
  

@router.get("/uni_ids", tags=["Get count of unique image ids"])
async def uni_ids():
  start_time = time()

  val1 = await mongo.post_image_ids_collection.count_documents({})

  return response_util.response({
    "result": 1,
    "data": [
      {
        "rkey": rkey_format(),
        "dt": dt_format(),
        "val1": str(val1)
      }
    ]
  }, start_time=start_time)
  

@router.get("/uni_posts", tags=["Get count of unique post ids"])
async def uni_posts():
  start_time = time()

  val1 = await mongo.posts_collection.count_documents({})

  return response_util.response({
    "result": 1,
    "data": [
      {
        "rkey": rkey_format(),
        "dt": dt_format(),
        "val1": str(val1)
      }
    ]
  }, start_time=start_time)


@router.get("/minute_requests", 
            tags=["Get count of last minute requests."], 
            description="Use filter query parameter for count by matches in stored request url. \
                         Example: http://domain/api/v1/graf/minute_requests?filter=training")
async def minute_requests(filter: str = None):
  start_time = time()

  query = {
    "created_at": {
      "$gt": (datetime.now() - timedelta(minutes=1)).timestamp()
    }
  }
  if filter:
    query["url"] = {
      "$regex": filter
    }

  val1 = await mongo.requests_collection.count_documents(query)

  return response_util.response({
    "result": 1,
    "data": [
      {
        "rkey": rkey_format(),
        "dt": dt_format(),
        "val1": str(val1)
      }
    ]
  }, start_time=start_time)


@router.get("/hour_requests", 
            tags=["Get count of last hour requests."], 
            description="Use filter query parameter for count by matches in stored request url. \
                         Example: http://domain/api/v1/graf/hour_requests?filter=training")
async def hour_requests(filter: str = None):
  start_time = time()

  query = {
    "created_at": {
      "$gt": (datetime.now() - timedelta(hours=1)).timestamp()
    }
  }
  if filter:
    query["url"] = {
      "$regex": filter
    }

  val1 = await mongo.requests_collection.count_documents(query)

  return response_util.response({
    "result": 1,
    "data": [
      {
        "rkey": rkey_format(),
        "dt": dt_format(),
        "val1": str(val1)
      }
    ]
  }, start_time=start_time)
  

@router.get("/day_requests", 
            tags=["Get count of last 24h requests."], 
            description="Use filter query parameter for count by matches in stored request url. \
                         Example: http://domain/api/v1/graf/day_requests?filter=training")
async def day_requests(filter: str = None):
  start_time = time()

  query = {
    "created_at": {
      "$gt": (datetime.now() - timedelta(days=1)).timestamp()
    }
  }
  if filter:
    query["url"] = {
      "$regex": filter
    }

  val1 = await mongo.requests_collection.count_documents(query)

  return response_util.response({
    "result": 1,
    "data": [
      {
        "rkey": rkey_format(),
        "dt": dt_format(),
        "val1": str(val1)
      }
    ]
  }, start_time=start_time)


@router.get("/week_requests", 
            tags=["Get count of last week requests."], 
            description="Use filter query parameter for count by matches in stored request url. \
                         Example: http://domain/api/v1/graf/week_requests?filter=training")
async def week_requests(filter: str = None):
  start_time = time()

  query = {
    "created_at": {
      "$gt": (datetime.now() - timedelta(weeks=1)).timestamp()
    }
  }
  if filter:
    query["url"] = {
      "$regex": filter
    }

  val1 = await mongo.requests_collection.count_documents(query)

  return response_util.response({
    "result": 1,
    "data": [
      {
        "rkey": rkey_format(),
        "dt": dt_format(),
        "val1": str(val1)
      }
    ]
  }, start_time=start_time)


@router.get("/cpu_usage", tags=["Get current usage of cpu"])
async def usage():
  start_time = time()

  val1 = usage_util.get_cpu_usage()

  return response_util.response({
    "result": 1,
    "data": [
      {
        "rkey": rkey_format(),
        "dt": dt_format(),
        "val1": str(val1)
      }
    ]
  }, start_time=start_time)


@router.get("/gpu_usage", tags=["Get current usage of gpu"])
async def usage():
  start_time = time()

  val1 = usage_util.get_gpu_usage()

  return response_util.response({
    "result": 1,
    "data": [
      {
        "rkey": rkey_format(),
        "dt": dt_format(),
        "val1": str(val1)
      }
    ]
  }, start_time=start_time)


@router.get("/memory_usage", tags=["Get current usage of memory"])
async def usage():
  start_time = time()

  val1 = usage_util.get_memory_usage()

  return response_util.response({
    "result": 1,
    "data": [
      {
        "rkey": rkey_format(),
        "dt": dt_format(),
        "val1": str(val1)
      }
    ]
  }, start_time=start_time)


@router.get("/disk_usage", tags=["Get current usage of disk"])
async def usage():
  start_time = time()

  val1 = usage_util.get_disk_usage()

  return response_util.response({
    "result": 1,
    "data": [
      {
        "rkey": rkey_format(),
        "dt": dt_format(),
        "val1": str(val1)
      }
    ]
  }, start_time=start_time)
