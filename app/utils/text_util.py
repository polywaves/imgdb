from urllib.parse import unquote
from datetime import datetime


def urldecode(text: str) -> str:
  return unquote(text).replace("+", " ")


def dt_format() -> str:
  return datetime.now().strftime("%d.%m.%y %H:%M:%S")


def rkey_format() -> str:
  return datetime.now().strftime("%y%m%d%H%M%S")