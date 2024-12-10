import os
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.openapi.docs import get_swagger_ui_html
from app import mongo
from app import task_manager
from app.utils.logger_util import logger


app = FastAPI(
  docs_url = None,
  redirect_slashes=False
)


if "TASK_MANAGER" in os.environ:
  @app.on_event("startup")
  async def startup_event():
    logger.debug("Task manager started")

    await task_manager.run()
else:
  from time import time
  from fastapi.middleware.cors import CORSMiddleware
  from app.api import v1
  from app.providers import weaviate_provider


  @app.on_event("startup")
  async def startup_event():
    # await mongo.migrate()
    # logger.debug("MongoDB has been migrated")

    # try:
    #   weaviate_provider.create_collection()
    #   logger.debug("Weaviate has been prepaired")
    # except Exception as e:
    #   logger.debug(e)

    logger.info("App started")


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
  async def http_processing(request: Request, call_next) -> any:
    url = str(request.url)
    client_ip = request.client.host
    if os.environ["MODE"] == 'production' and "x-real-ip" in request.headers:
      client_ip = request.headers["x-real-ip"]

      logger.info(f"REQUEST BY CLIENT IP: {client_ip}")

      ip_list = os.environ["API_ALLOW_IP_LIST"].split(',')
      route_list = os.environ["API_EXCLUDE_ROUTES"].split(',')

      if client_ip not in ip_list:
        found = False
        for route in route_list:
          if route in url:
            found = True

        if not found:
          return JSONResponse(content="Access denied", status_code=403)
    
    response = await call_next(request)

    ## Count requests
    if "_requests" not in url:
      await mongo.requests_collection.insert_one({
        "client_ip": client_ip,
        "url": url,
        "created_at": time()
      })

    return response


  app.include_router(v1.router, prefix='/api/v1')


  @app.get("/apidoc", include_in_schema=False)
  async def custom_swagger_ui_html():
    return get_swagger_ui_html(
      openapi_url=app.openapi_url,
      title=f"{app.title} - Swagger UI",
      # swagger_ui_dark.css raw url
      # swagger_css_url="/static/swagger_ui_dark.css"
    )


  @app.get("/health")
  def health_check():
    return {
      "status": "healthy"
    }
