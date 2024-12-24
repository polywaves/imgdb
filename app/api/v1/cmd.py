import os
import requests
import json
from time import time
from fastapi import APIRouter
from app.utils.logger_util import logger
from app.utils import response_util

router = APIRouter()


def get_portainer_jwt() -> str:
  payload = json.dumps({
    "password": os.environ["PORTAINER_PASSWORD"],
    "username": os.environ["PORTAINER_USERNAME"]
  })
  headers = {
    "Content-Type": "application/json"
  }

  response = requests.request("POST", os.path.join(os.environ["PORTAINER_HOST"], "auth"), headers=headers, data=payload).json()

  return response["jwt"]


def get_portainer_containers(jwt: str, filter: str) -> str:
  payload = {
    "all": True,
    "filters": {
      "label": ["com.docker.compose.project=services"]
    }
  }
  headers = {
    "Content-Type": "application/json",
    "X-API-Key": jwt
  }

  containers = requests.request("GET", os.path.join(os.environ["PORTAINER_HOST"], "endpoints/1/docker/containers/json"), headers=headers, params=payload).json()
  logger.debug(containers)
  data = list()
  for container in containers:
    logger.debug(container)
    # if filter in container["Names"][0]:
    #   data.append(container)      

  return data


@router.get("/restart_neuro", tags=["Restart neuro nodes"])
async def restart_neuro():
  start_time = time()

  jwt = get_portainer_jwt()
  containers = get_portainer_containers(jwt=jwt, filter="node")

  logger.debug(containers)

  # http://87.242.104.141:9000/api/endpoints/1/docker/v1.41/containers/a84062a6e8f2f8ee28c62118219cf5b875adb13c7a81fea47278a7f91890809a/restart
  # http://87.242.104.141:9000/api/endpoints/1/docker/v1.41/containers/json?all=true&filters={"label":["com.docker.compose.project=services"]}


  data = list()
  nodes = 6
  # for node in range(1, nodes + 1):
  #   data.append(docker.compose.restart(f"node{node}"))

  # logger.debug(data)

  return response_util.response({
    "result": 1,
    "data": containers
  }, start_time=start_time)
