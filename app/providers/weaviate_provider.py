import os
import weaviate 
from weaviate.config import AdditionalConfig, Timeout
from weaviate.classes.config import Configure, DataType, Property
from weaviate.classes.query import MetadataQuery, Filter, Metrics
from weaviate.classes.aggregate import GroupByAggregate


collection_name = os.environ["WEAVIATE_COLLECTION_NAME"]


client = weaviate.connect_to_custom(
  http_host=os.environ["WEAVIATE_HOST"],
  http_port=os.environ["WEAVIATE_HTTP_PORT"],
  http_secure=os.environ["WEAVIATE_HTTP_SECURE"],
  grpc_host=os.environ["WEAVIATE_HOST"],
  grpc_port=os.environ["WEAVIATE_GRPC_PORT"],
  grpc_secure=os.environ["WEAVIATE_GRPC_SECURE"],
  additional_config=AdditionalConfig(
    timeout=Timeout(
      init=120, 
      query=60, 
      insert=120
    )
  )
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
      )
    ]
  )

  return collection



def create_image_vector(items: list) -> object:
  collection = client.collections.get(collection_name)

  with collection.batch.dynamic() as batch:
    for item in items:
      batch.add_object(item)

  return collection


def search_near_image(image, limit: int = 10) -> object:
  collection = client.collections.get(collection_name)
  response = collection.query.near_image(
    near_image=image,
    return_metadata=MetadataQuery(distance=True),
    limit=limit
  )

  return response.objects


def delete_image_by_uid(uid: int) -> object:
  collection = client.collections.get(collection_name)
  response = collection.data.delete_many(
    where=Filter.by_property("uid").contains_any([uid])
  )

  return response


def get_count_of_unique_uids():
  collection = client.collections.get(collection_name)
  response = collection.aggregate.over_all(
    group_by=GroupByAggregate(prop="uid")
  )

  return response.groups

