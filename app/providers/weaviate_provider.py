import os
import weaviate
from weaviate.classes.config import Configure, DataType, Property
from weaviate.classes.query import MetadataQuery, Filter


collection_name = os.environ["WEAVIATE_COLLECTION_NAME"]


client = weaviate.connect_to_custom(
  http_host=os.environ["WEAVIATE_HOST"],
  http_port=os.environ["WEAVIATE_HTTP_PORT"],
  http_secure=os.environ["WEAVIATE_HTTP_SECURE"],
  grpc_host=os.environ["WEAVIATE_HOST"],
  grpc_port=os.environ["WEAVIATE_GRPC_PORT"],
  grpc_secure=os.environ["WEAVIATE_GRPC_SECURE"]
)


def get_collections() -> list:
  data = client.collections.list_all(simple=False)

  response = list()
  for item in data.values():
    response.append(item)

  return response


def delete_collection():
  client.collections.delete(collection_name)


def delete_all_collections():
  client.collections.delete_all()


def create_collection() -> object:
  collection = client.collections.create(
    name=collection_name,
    vectorizer_config=Configure.Vectorizer.img2vec_neural(
      image_fields=[
        "image"
      ]
    ),
    vector_index_config=Configure.VectorIndex.hnsw(),
    properties=[
      Property(
        name="image",
        data_type=DataType.BLOB
      ),
      Property(
        name="uid", 
        data_type=DataType.INT
      ),
      Property(
        name="post_id", 
        data_type=DataType.INT
      )
    ]
  )

  return collection



def create_image_vector(items: list):
  collection = client.collections.get(collection_name)

  with collection.batch.dynamic() as batch:
    for item in items:
      batch.add_object(item)

  # uuids = list()
  # for item in items:
  #   uuid = collection.data.insert(item)
  #   uuids.append(uuid)

  # return uuids


def get_image_vectors_by_post_id(post_id: int) -> object:
  collection = client.collections.get(collection_name)

  response = collection.query.fetch_objects(
    filters=Filter.by_property("post_id").contains_any([post_id]),
    include_vector=True
  )

  return response


def search_near_image(image, limit: int = 10) -> object:
  collection = client.collections.get(collection_name)
  response = collection.query.near_image(
    near_image=image,
    return_metadata=MetadataQuery(distance=True),
    limit=limit
  )

  return response


def delete_image_by_uid(uid: int) -> object:
  collection = client.collections.get(collection_name)
  response = collection.data.delete_many(
    where=Filter.by_property("uid").contains_any([uid])
  )

  return response


def delete_images_by_post_id(post_id: int) -> object:
  collection = client.collections.get(collection_name)
  response = collection.data.delete_many(
    where=Filter.by_property("post_id").contains_any([post_id])
  )

  return response

