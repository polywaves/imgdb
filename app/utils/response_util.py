import time


def response(data: dict, start_time) -> dict:
  data["speed"] = int((time.time() - start_time) * 1000)

  return data