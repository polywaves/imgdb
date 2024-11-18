from urllib.parse import unquote
from datetime import datetime


def urldecode(text: str) -> str:
  return unquote(text).replace("+", " ")


def date_format(date: str = datetime.now()) -> str:
  return date.strftime("%d.%m.%y%H:%M:%S")