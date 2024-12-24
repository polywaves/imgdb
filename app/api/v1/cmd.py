import os
import requests
import json
from time import time
from fastapi import APIRouter
from app.utils.logger_util import logger
from app.utils import response_util

router = APIRouter()


def get_jwt() -> str:
  payload = json.dumps({
    "password": os.environ["PORTAINER_PASSWORD"],
    "username": os.environ["PORTAINER_USERNAME"]
  })
  headers = {
    "Content-Type": "application/json"
  }

  response = requests.request("POST", os.path.join(os.environ["PORTAINER_HOST"], "auth"), headers=headers, data=payload).json()

  return response["jwt"]


def get_containers(jwt: str, filter: str) -> str:
  headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {jwt}"
  }

  containers = requests.request("GET", os.path.join(os.environ["PORTAINER_HOST"], 'endpoints/1/docker/containers/json?all=true&filters={"label":["com.docker.compose.project=services"]}'), headers=headers).json()
  data = list()
  for container in containers:
    logger.debug(container["Names"])
    if filter in container["Names"]:
      data.append(container)      

  return data.reverse()


def restart_container(jwt: str, id: str) -> str:
  headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {jwt}"
  }

  response = requests.request("POST", os.path.join(os.environ["PORTAINER_HOST"], f"endpoints/1/docker/containers/{id}/restart"), headers=headers).json()  

  return response


@router.get("/restart_neuro", tags=["Restart neuro nodes"])
async def restart_neuro():
  start_time = time()

  jwt = get_jwt()
  containers = get_containers(jwt=jwt, filter="node")

  for container in containers:
    logger.debug(container)

    # restart = restart_container(jwt=jwt, id=container["Id"])

    # logger.debug(restart)

  return response_util.response({
    "result": 1,
    "data": containers
  }, start_time=start_time)
