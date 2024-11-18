from urllib.parse import unquote


def urldecode(text: str) -> str:
  return unquote(text).replace("+", " ")