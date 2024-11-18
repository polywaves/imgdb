import os
from time import time
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from app import mongo
from app.utils.logger_util import logger
from app.api import v1


app = FastAPI(
  redirect_slashes=False
)


@app.on_event("startup")
async def startup_event():
  await mongo.migrate()
  logger.debug("MongoDB has migrated")


if os.environ["MODE"] == 'development':
  logger.debug("Development mode")
  app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
  )


@app.middleware("http")
async def add_process_time_header(request: Request, call_next) -> any:
  logger.debug(await request.json())

  response = await call_next(request)

  client_ip = request.client.host
  if "X-Real-Ip" in request.headers:
    client_ip = request.headers["X-Real-Ip"]

  logger.info(f"Client ip: {client_ip}")

  ## Count requests
  mongo.requests_collection.insert_one({
    "client_ip": client_ip,
    "url": str(request.url),
    "created_at": time()
  })

  return response


app.include_router(v1.router, prefix='/api/v1')

@app.get("/health")
def health_check():
  return {
    "status": "healthy"
  }
