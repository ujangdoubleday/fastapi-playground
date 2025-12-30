from fastapi import APIRouter
from app.api.v2.endpoints import auth, hello

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(hello.router, prefix="/hello", tags=["hello"])
