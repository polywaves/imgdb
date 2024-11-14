from time import time
from datetime import datetime
from fastapi import APIRouter, HTTPException
from app.mongo import db
from app.utils.logger_util import logger

router = APIRouter()


posts_collection = db.get_collection("posts")


@router.get("/uni_vectors", tags=["Get count of uniq vectors"])
async def uni_vectors():
  try:
    result = 0

    return {
      "data": [
        {
          "rkey": time(),
          "dt": datetime.now(),
          "val1": result
        }
      ],
      "result": 1, 
      "speed": 0
    }
  except Exception as e:
    logger.error(e)
    raise HTTPException(status_code=500, detail=str(e))
  

@router.get("/uni_ids", tags=["Get count of uniq image ids"])
async def uni_ids():
  result = 0

  return {
    "data": [
      {
        "rkey": time(),
        "dt": datetime.now(),
        "val1": result
      }
    ],
    "result": 1, 
    "speed": 0
  }
  

@router.get("/uni_posts", tags=["Get count of uniq post ids"])
async def uni_posts():
  result = await posts_collection.count_documents({})

  return {
    "data": [
      {
        "rkey": time(),
        "dt": datetime.now(),
        "val1": result
      }
    ],
    "result": 1, 
    "speed": 0
  }
  

@router.get("/day_requests", tags=["Get count of last 24h requests"])
async def day_requests():
  result = 0

  return {
    "data": [
      {
        "rkey": time(),
        "dt": datetime.now(),
        "val1": result
      }
    ],
    "result": 1, 
    "speed": 0
  }


@router.get("/usage", tags=["Get current usage of cpu and gpu"])
async def usage():
  result = 0

  return {
    "data": [
      {
        "rkey": time(),
        "dt": datetime.now(),
        "val1": result
      }
    ],
    "result": 1, 
    "speed": 0
  }
