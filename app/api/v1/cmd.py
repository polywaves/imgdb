import subprocess
from time import time
from fastapi import APIRouter
from app.utils.logger_util import logger
from app.utils import response_util

router = APIRouter()


@router.get("/restart_neuro", tags=["Restart neuro nodes"])
async def restart_neuro():
  start_time = time()

  data = {
    "down": list(),
    "up": list()
  }
  nodes = 6
  for node in range(nodes):
    cmd = f"docker compose -f docker-compose.prod.yml down node{node}"
    data["down"].append(subprocess.call(cmd, shell=True))

  for node in range(nodes):
    cmd = f"docker compose -f docker-compose.prod.yml up -d node{node}"
    data["up"].append(subprocess.call(cmd, shell=True))

  logger.debug(data)

  return response_util.response({
    "result": 1,
    "data": data
  }, start_time=start_time)
