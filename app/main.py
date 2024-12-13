from fastapi import FastAPI
from app.db.base import Base, engine
from app.api.v1.api import api_router
from app.core.config import settings

app = FastAPI(title=settings.PROJECT_NAME, version=settings.VERSION)

app.include_router(api_router)
Base.metadata.create_all(bind=engine)
