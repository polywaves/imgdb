import os
from logging import getLogger
from fastapi import FastAPI, Response, status
from vectorizer import ImageVectorizer, VectorImagePayload


app = FastAPI()
imgVec : ImageVectorizer
logger = getLogger('uvicorn')


@app.on_event("startup")
def startup_event():
  global imgVec

  cuda_env = os.getenv("ENABLE_CUDA")
  cuda_support = False
  cuda_core = ""

  if cuda_env is not None and cuda_env == "true" or cuda_env == "1":
    cuda_support = True
    cuda_core = os.getenv("CUDA_CORE")
    if cuda_core is None or cuda_core == "":
      cuda_core = "cuda:0"
    logger.info(f"CUDA_CORE set to {cuda_core}")
  else:
    logger.info("Running on CPU")

  imgVec = ImageVectorizer(cuda_support, cuda_core)


@app.get("/.well-known/live", response_class=Response)
@app.get("/.well-known/ready", response_class=Response)
def live_and_ready(response: Response):
  response.status_code = status.HTTP_204_NO_CONTENT


@app.post("/vectors")
@app.post("/vectors/")
def read_item(item: VectorImagePayload, response: Response):
  try:
    vector = imgVec.vectorize(item.id, item.image)

    return {
      "id": item.id, 
      "vector": vector.tolist(), 
      "dim": len(vector)
    }
  except Exception as e:
    logger.exception('Something went wrong while vectorizing data.')
    response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

    return {"error": str(e)}
