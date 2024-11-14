import requests
import json
import pandas

# url = "http://0.0.0.0:8000/api/v1/image/training/"
url = "http://87.242.104.141:8000/api/v1/vector/training"
headers = {
  'Content-Type': 'application/json'
}

images = pandas.read_csv("./imgs_396k.csv", on_bad_lines="skip", sep=";", low_memory=False, names=["id", "uid", "img"])

for i, row in images.iterrows():
  if (i > 0):
    params = {
      "url": row["img"],
      "uid": int(row["uid"])
    }
    response = requests.request("GET", url, headers=headers, params=params)
    
    print(params)
    print(f"TOTAL: {i}")
    print(response.text)
  else:
    continue
