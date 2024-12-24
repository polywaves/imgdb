import requests
import json
from time import time
from fastapi import APIRouter
from app.utils.logger_util import logger
from app.utils import response_util

router = APIRouter()


@router.get("/restart_neuro", tags=["Restart neuro nodes"])
async def restart_neuro():
  start_time = time()

  url = "http://87.242.104.141:9000/api/auth"

  payload = json.dumps({
    "password": "62o0mFESlRtB",
    "username": "admin"
  })
  headers = {
    "Content-Type": "application/json"
  }

  response = requests.request("POST", url, headers=headers, data=payload)

  logger.debug(response.json())


  data = list()
  nodes = 6
  # for node in range(1, nodes + 1):
  #   data.append(docker.compose.restart(f"node{node}"))

  # logger.debug(data)

  return response_util.response({
    "result": 1,
    "data": data
  }, start_time=start_time)
