import time
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.utils.logger_util import logger

from app.api import v1

app = FastAPI()

app.add_middleware(
  CORSMiddleware,
  allow_origins=["*"],
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)

# Whitelisted IPs
WHITELISTED_IPS = ["5.61.63.91", "46.138.188.236", "87.242.104.141", "0.0.0.0", "127.0.0.1", "192.168.65.1"]

@app.middleware("http")
async def add_process_time_header(request: Request, call_next) -> any:
  start_time = time.time()
  # Get client IP
  ip = str(request.client.host)
  logger.info(f"Client ip is {ip}")

  if ip not in WHITELISTED_IPS:
    raise HTTPException(status_code=500, detail=f"IP {ip} is not allowed to access this resource.")  

  response = await call_next(request)
  logger.info(f"Response time is {time.time() - start_time} sec")

  return response

app.include_router(v1.router, prefix='/api/v1')
