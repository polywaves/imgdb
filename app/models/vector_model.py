from pydantic import BaseModel, Field
from typing import List


class ImageSizes(BaseModel):
  n: str = Field()
  w: int = Field()
  h: int = Field()


class Images(BaseModel):
  img_id: int = Field()
  img: str = Field()
  sizes: List[ImageSizes]


class Video(BaseModel):
  poster: str = Field()
  main: str = Field()
  id_poster: str = Field()
  id_main: str = Field()


class TrainingByJson(BaseModel):
  id: str = Field()
  os: str = Field()
  ds: str = Field()
  of: str = Field()
  ins: str = Field()
  vendor_capt: str = Field()
  vendor_id: str = Field()
  point_id: str = Field()
  vk_post: str = Field()
  price: float = Field()
  by: str = Field()
  item_name: str = Field()
  like: str = Field()
  views: str = Field()
  posted: str = Field()
  text: str = Field()
  images: List[Images]
  video: Video
  sizes: List[str]
  options: List[str]


class DeletePostsByIds(BaseModel):
  post_ids: List[str]