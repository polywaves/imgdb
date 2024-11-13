import requests
import json
import pandas

url = "http://0.0.0.0:8000/api/v1/image/training/"
headers = {
  'Content-Type': 'application/json'
}
collection_name="test1"

images = pandas.read_csv("./imgs_396k.csv", on_bad_lines="skip", sep=";", low_memory=False, names=["id", "uid", "img"])

for i, row in images.iterrows():
  if (i > 3732):
    payload = json.dumps({
      # "collection_name": collection_name,
      "url": row["img"],
      "uid": int(row["uid"])
    })
    response = requests.request("PUT", url, headers=headers, data=payload)
    
    print(f"TOTAL: {i}")
    print(response.text)
  else:
    continue
