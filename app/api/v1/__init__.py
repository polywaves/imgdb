from fastapi import APIRouter
from app.api.v1 import vector, graf



router = APIRouter()


router.include_router(vector.router, prefix='/vector')
router.include_router(graf.router, prefix='/graf')
router.include_router(graf.router, prefix='/cmd')