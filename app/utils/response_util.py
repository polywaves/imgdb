import time
from app.utils.logger_util import logger


def response(data: dict, start_time) -> dict:
  speed = int(time.time() - start_time)
  data["speed"] = speed * 1000

  logger.debug(f"RESPONSE TIME: {speed}")

  return data