from time import time
from fastapi import APIRouter
from python_on_whales import DockerClient
from app.utils.logger_util import logger
from app.utils import response_util

router = APIRouter()


docker = DockerClient(
  compose_files=["./docker-compose.prod.yml"]
)


@router.get("/restart_neuro", tags=["Restart neuro nodes"])
async def restart_neuro():
  start_time = time()

  data = {
    "down": list(),
    "up": list()
  }
  nodes = 6
  for node in range(nodes):
    data["down"].append(docker.compose.down(f"node{node}"))

  for node in range(nodes):
    data["up"].append(docker.compose.up(f"node{node}"))

  logger.debug(data)

  return response_util.response({
    "result": 1,
    "data": data
  }, start_time=start_time)
