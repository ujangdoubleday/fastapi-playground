from fastapi import APIRouter
from app.api.v3.endpoints import shapeshifter

api_router = APIRouter()
api_router.include_router(shapeshifter.router, prefix="/shapeshifter", tags=["shapeshifter"])
