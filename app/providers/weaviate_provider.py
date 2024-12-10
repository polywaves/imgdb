import os
import weaviate
from datetime import datetime, timedelta
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

collection = client.collections.get(collection_name)


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


def create_collection():
  client.collections.create(
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

  global collection
  collection = client.collections.get(collection_name)



def create_image_vector(items: list):
  with collection.batch.dynamic() as batch:
    for item in items:
      batch.add_object(item)

    try:
      failed_objects = batch.failed_objects
    except Exception:
      failed_objects = None
    
    return failed_objects


def get_image_vectors_by_post_id(post_id: int) -> object:
  response = collection.query.fetch_objects(
    filters=Filter.by_property("post_id").equal(post_id),
    include_vector=True
  )

  return response


def search_near_image(image, days: int = 23, limit: int = 30) -> object:
  filter = datetime.now() - timedelta(days=days)

  response = collection.query.near_image(
    near_image=image,
    return_metadata=MetadataQuery(distance=True, creation_time=True),
    limit=limit,
    # filters=Filter.by_creation_time().greater_than(filter)
  )

  return response


def delete_image_by_uid(uid: int) -> object:
  response = collection.data.delete_many(
    where=Filter.by_property("uid").equal(uid)
  )

  return response


def delete_images_by_post_id(post_id: int) -> object:
  response = collection.data.delete_many(
    where=Filter.by_property("post_id").equal(post_id)
  )

  return response

