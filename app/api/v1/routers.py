from fastapi import APIRouter

from app.api.v1.endpoints import yappi_router


router = APIRouter()
router.include_router(yappi_router, tags=["yappi"])
