from fastapi import APIRouter
from app.api.v1 import habits, user

api_router = APIRouter()
api_router.include_router(habits.router, prefix="/habits", tags=["habits"])
api_router.include_router(user.router, prefix="/user", tags=["user"])
