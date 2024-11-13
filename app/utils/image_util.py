import base64
import requests

def load(url: str) -> bytearray:
  response = requests.get(url)
  
  return response.content

def to_base64(stream: bytearray) -> str:
  response = base64.b64encode(stream).decode('utf-8')

  return response

def from_url_to_base64(url: str) -> str:
  stream = load(url=url)
  response = to_base64(stream=stream)

  return response