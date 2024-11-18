import time


def response(data: dict, start_time) -> dict:
  data["speed"] = round(time.time() - start_time, 6)

  return data