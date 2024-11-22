from fastapi import APIRouter
from app.api.v1 import habits
api_router = APIRouter()
api_router.include_router(habits.router, prefix="/habits", tags=["habits"])
