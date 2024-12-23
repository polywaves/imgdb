from time import time
from fastapi import APIRouter
from python_on_whales import DockerClient
from app.utils.logger_util import logger
from app.utils import response_util

router = APIRouter()


docker = DockerClient(
  compose_files=["docker-compose.prod.yml"],
  host="/var/run/docker.sock"
)


@router.get("/restart_neuro", tags=["Restart neuro nodes"])
async def restart_neuro():
  start_time = time()

  data = list()
  nodes = 6
  for node in range(1, nodes + 1):
    data.append(docker.compose.restart(f"node{node}"))

  logger.debug(data)

  return response_util.response({
    "result": 1,
    "data": data
  }, start_time=start_time)
