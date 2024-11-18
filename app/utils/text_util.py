from urllib.parse import unquote
from datetime import datetime


def urldecode(text: str) -> str:
  return unquote(text).replace("+", " ")


def dt_format(date: str = datetime.now()) -> str:
  return date.strftime("%d.%m.%y %H:%M:%S")


def rkey_format(date: str = datetime.now()) -> str:
  return date.strftime("%y%m%d%H%M%S")