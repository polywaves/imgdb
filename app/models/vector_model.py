from pydantic import BaseModel
from typing import List, Optional


class ImageSizes(BaseModel):
  n: str = None
  w: int = 0
  h: int = 0


class Images(BaseModel):
  img_id: int = None
  img: str = None
  sizes: Optional[List[ImageSizes]] = list()


class Video(BaseModel):
  poster: Optional[str] = None
  main: Optional[str] = None
  id_poster: Optional[str] = None
  id_main: Optional[str] = None


class TrainingByJson(BaseModel):
  id: str = None
  os: Optional[str] = None
  ds: Optional[str] = None
  of: Optional[str] = None
  ins: Optional[str] = None
  vendor_capt: Optional[str] = None
  vendor_id: Optional[str] = None
  point_id: Optional[str] = None
  vk_post: Optional[str] = None
  price: Optional[float] = None
  by: Optional[str] = None
  item_name: Optional[str] = None
  like: Optional[str] = None
  views: Optional[str] = None
  posted: Optional[str] = None
  text: Optional[str] = None
  images: List[Images] = list()
  video: Optional[Video] = Video
  sizes: Optional[List[str]] = list()
  options: Optional[List[str]] = list()


class DeletePostsByIds(BaseModel):
  post_ids: List[str]