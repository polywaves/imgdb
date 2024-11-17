import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.utils.logger_util import logger

from app.api import v1

app = FastAPI(
  redirect_slashes=False
)

if os.environ["MODE"] == 'development':
  logger.debug("Development mode")
  app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
  )

app.include_router(v1.router, prefix='/api/v1')

@app.get("/health")
def health_check():
  return {
    "status": "healthy"
  }
