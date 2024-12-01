import os
from time import time
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app import mongo
from app.utils.logger_util import logger
from app.api import v1
from starlette.concurrency import iterate_in_threadpool
from app.providers import weaviate_provider


app = FastAPI(
  redirect_slashes=False
)


@app.on_event("startup")
async def startup_event():
  await mongo.migrate()
  logger.debug("MongoDB has migrated")


@app.on_event("shutdown")
async def shutdown_event():
  weaviate_provider.client.close()


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
  url = str(request.url)
  client_ip = request.client.host
  if "x-real-ip" in request.headers and "x-forwarded-for" in request.headers:
    client_ip = request.headers["x-real-ip"]
    forwarded_ip = request.headers["x-forwarded-for"]

    logger.info(f"REQUEST BY CLIENT IP: {client_ip} FORWARDED {forwarded_ip}")

    ip_list = os.environ["API_ALLOW_IP_LIST"].split(',')
    route_list = os.environ["API_EXCLUDE_ROUTES"].split(',')

    if client_ip not in ip_list and forwarded_ip not in ip_list:
      found = False
      for route in route_list:
        if route in url:
          found = True

      if not found:
        raise HTTPException(status_code=403, detail="Access denied")

  response = await call_next(request)

  # response_body = [chunk async for chunk in response.body_iterator]
  # response.body_iterator = iterate_in_threadpool(iter(response_body))

  # logger.debug(f"RESPONSE: {response_body[0].decode()}")

  ## Count requests
  await mongo.requests_collection.insert_one({
    "client_ip": client_ip,
    "url": url,
    "created_at": time()
  })

  return response


app.include_router(v1.router, prefix='/api/v1')

@app.get("/health")
def health_check():
  return {
    "status": "healthy"
  }
