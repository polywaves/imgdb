from fastapi import APIRouter
from app.api.v1 import vector

router = APIRouter()


router.include_router(vector.router, prefix='/vector')