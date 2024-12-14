from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from app.db.base import Base, engine
from app.api.v1.api import api_router
from app.core.config import settings
import logging
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

origins = [
    "http://localhost:8888",
    "http://127.0.0.1:8888"# Add your allowed domains
    "http://0.0.0.0",
]

app = FastAPI(title=settings.PROJECT_NAME, version=settings.VERSION)


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allow specific origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)
app.include_router(api_router)
Base.metadata.create_all(bind=engine)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
	exc_str = f'{exc}'.replace('\n', ' ').replace('   ', ' ')
	logging.error(f"{request}: {exc_str}")
	content = {'status_code': 10422, 'message': exc_str, 'data': None}
	return JSONResponse(content=content, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)

