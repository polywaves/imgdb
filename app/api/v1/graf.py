from fastapi import APIRouter, HTTPException
from app.utils.logger_util import logger

router = APIRouter()


@router.get("/uni_vectors", tags=["Get count of uniq vectors"])
async def uni_vectors():
  try:
    pass
  except Exception as e:
    logger.error(e)
    raise HTTPException(status_code=500, detail=str(e))
  

@router.get("/uni_ids", tags=["Get count of uniq image ids"])
async def uni_ids():
  try:
    pass
  except Exception as e:
    logger.error(e)
    raise HTTPException(status_code=500, detail=str(e))
  

@router.get("/uni_posts", tags=["Get count of uniq post ids"])
async def uni_posts():
  try:
    pass
  except Exception as e:
    logger.error(e)
    raise HTTPException(status_code=500, detail=str(e))
  

@router.get("/day_requests", tags=["Get count of last 24h requests"])
async def day_requests():
  try:
    pass
  except Exception as e:
    logger.error(e)
    raise HTTPException(status_code=500, detail=str(e))


@router.get("/usage", tags=["Get current usage of cpu and gpu"])
async def day_requests():
  try:
    pass
  except Exception as e:
    logger.error(e)
    raise HTTPException(status_code=500, detail=str(e))
