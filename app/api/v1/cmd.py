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
    if filter in container["Names"][0]:
      data.append(container)  

  response = list(reversed(data))
  logger.debug(response)    

  return response


def stop_container(jwt: str, id: str) -> str:
  headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {jwt}"
  }

  response = requests.request("POST", os.path.join(os.environ["PORTAINER_HOST"], f"endpoints/1/docker/containers/{id}/stop"), headers=headers).text

  return response


def start_container(jwt: str, id: str) -> str:
  headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {jwt}"
  }

  response = requests.request("POST", os.path.join(os.environ["PORTAINER_HOST"], f"endpoints/1/docker/containers/{id}/start"), headers=headers).text

  return response


@router.get("/restart_neuro", tags=["Restart neuro nodes"])
async def restart_neuro():
  start_time = time()

  jwt = get_jwt()
  containers = get_containers(jwt=jwt, filter="node")

  for container in containers:
    stop = stop_container(jwt=jwt, id=container["Id"])
    logger.debug(stop)

  for container in containers:
    start = start_container(jwt=jwt, id=container["Id"])
    logger.debug(start)

  return response_util.response({
    "result": 1
  }, start_time=start_time)
