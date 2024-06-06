from fastapi import APIRouter

from app.api.v1 import api_v1_router

router = APIRouter(prefix="/api")
router.include_router(api_v1_router, prefix="/v1")
