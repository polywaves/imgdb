import time
from app.utils.logger_util import logger


def response(data: dict, start_time) -> dict:
  speed = time.time() - start_time
  data["speed"] = int(speed * 1000)

  logger.debug(f"RESPONSE TIME: {speed}")

  return data