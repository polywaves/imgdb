import weaviate 
from weaviate.classes.config import Configure, DataType, Property
from weaviate.classes.query import MetadataQuery, Filter


collection_name = 'test1'


client = weaviate.connect_to_custom(
  http_host="weaviate",
  http_port=8080,
  http_secure=False,
  grpc_host="weaviate",
  grpc_port=50051,
  grpc_secure=False
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
        name="data",
        data_type=DataType.OBJECT,
        nested_properties=[
          Property(name="url", data_type=DataType.TEXT)
        ]
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
